"""
Kayit Modulu - Yeni musteri kaydı formu
Autocomplete, validasyon ve kayit islemi
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QDateEdit, QDoubleSpinBox,
    QFrame, QListWidget, QListWidgetItem, QScrollArea, QMessageBox,
    QCompleter, QSizePolicy
)
from PyQt5.QtCore import Qt, QDate, pyqtSignal, QStringListModel, QSortFilterProxyModel
from PyQt5.QtGui import QFont
import re


class AutocompleteLineEdit(QLineEdit):
    """Autocomplete ozelligi olan arama alani"""
    oneri_secildi = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._popup = QListWidget()
        self._popup.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self._popup.setFocusPolicy(Qt.NoFocus)
        self._popup.setMouseTracking(True)
        self._popup.itemClicked.connect(self._on_item_selected)
        self._popup.setMaximumHeight(200)
        self._data = []
        self.textChanged.connect(self._on_text_changed)

    def set_data(self, data):
        """data: [{'tc':..., 'isim':..., 'soyisim':..., 'oda':...}]"""
        self._data = data

    def _on_text_changed(self, text):
        if len(text) < 2:
            self._popup.hide()
            return

        text_lower = text.lower()
        matches = []
        for item in self._data:
            full_name = f"{item.get('isim','')} {item.get('soyisim','')}".lower()
            tc = str(item.get('tc', '')).lower()
            if text_lower in full_name or text_lower in tc:
                matches.append(item)

        if not matches:
            self._popup.hide()
            return

        self._popup.clear()
        for m in matches[:8]:
            display = f"{m.get('isim','')} {m.get('soyisim','')}  |  TC: {m.get('tc','')}  |  Son Oda: {m.get('oda','')}"
            item = QListWidgetItem(display)
            item.setData(Qt.UserRole, m)
            self._popup.addItem(item)

        pos = self.mapToGlobal(self.rect().bottomLeft())
        self._popup.move(pos)
        self._popup.setFixedWidth(max(self.width(), 450))
        self._popup.show()

    def _on_item_selected(self, item):
        self._popup.hide()
        data = item.data(Qt.UserRole)
        if data:
            self.oneri_secildi.emit(data)

    def focusOutEvent(self, event):
        if not self._popup.underMouse():
            self._popup.hide()
        super().focusOutEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self._popup.hide()
        elif event.key() in (Qt.Key_Down, Qt.Key_Up):
            if self._popup.isVisible():
                self._popup.setFocus()
                return
        super().keyPressEvent(event)

    def hideEvent(self, event):
        self._popup.hide()
        super().hideEvent(event)


class KayitModulu(QWidget):
    kayit_yapildi = pyqtSignal()

    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.dm = data_manager
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Kart cercevesi
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setObjectName("kayitKart")
        card.setStyleSheet("""
            QFrame#kayitKart {
                background: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 16, 20, 20)
        card_layout.setSpacing(10)
        main_layout.addWidget(card)

        # Baslik
        baslik = QLabel("📋  Yeni Misafir Kaydı")
        baslik.setObjectName("panelTitle")
        card_layout.addWidget(baslik)

        # Ayirici
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #e2e8f0;")
        card_layout.addWidget(sep)

        # Form alanlari
        self._add_form_fields(card_layout)

        # Butonlar
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_kaydet = QPushButton("✔  Kaydet")
        self.btn_kaydet.setObjectName("btnKaydet")
        self.btn_kaydet.clicked.connect(self._on_kaydet)
        btn_layout.addWidget(self.btn_kaydet)

        self.btn_temizle = QPushButton("↺  Temizle")
        self.btn_temizle.setObjectName("btnTemizle")
        self.btn_temizle.clicked.connect(self._temizle)
        btn_layout.addWidget(self.btn_temizle)

        card_layout.addLayout(btn_layout)
        card_layout.addStretch()

    def _add_form_row(self, layout, label_text, widget, zorunlu=True):
        """Form satiri ekle: etiket + alan"""
        row = QHBoxLayout()
        row.setSpacing(8)
        lbl = QLabel(label_text)
        lbl.setFixedWidth(130)
        lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        if zorunlu:
            lbl.setText(f"<span style='color:#dc2626'>*</span> {label_text}")
        row.addWidget(lbl)
        row.addWidget(widget)
        layout.addLayout(row)
        return widget

    def _add_form_fields(self, layout):
        # TC Kimlik No
        self.tc_edit = AutocompleteLineEdit()
        self.tc_edit.setPlaceholderText("11 haneli TC Kimlik No")
        self.tc_edit.setMaxLength(11)
        self.tc_edit.oneri_secildi.connect(self._fill_from_suggestion)
        self._add_form_row(layout, "T.C. Kimlik No", self.tc_edit)

        # Isim
        self.isim_edit = AutocompleteLineEdit()
        self.isim_edit.setPlaceholderText("Misafirin adı")
        self.isim_edit.oneri_secildi.connect(self._fill_from_suggestion)
        self._add_form_row(layout, "İsim", self.isim_edit)

        # Soyisim
        self.soyisim_edit = AutocompleteLineEdit()
        self.soyisim_edit.setPlaceholderText("Misafirin soyadı")
        self.soyisim_edit.oneri_secildi.connect(self._fill_from_suggestion)
        self._add_form_row(layout, "Soyisim", self.soyisim_edit)

        # Oda
        self.oda_combo = QComboBox()
        self.oda_combo.setPlaceholderText("Müsait oda seçin")
        self._add_form_row(layout, "Oda Numarası", self.oda_combo)

        # Giris tarihi
        self.giris_date = QDateEdit()
        self.giris_date.setCalendarPopup(True)
        self.giris_date.setDate(QDate.currentDate())
        self.giris_date.setDisplayFormat("dd/MM/yyyy")
        self._add_form_row(layout, "Giriş Tarihi", self.giris_date)

        # Cikis tarihi
        self.cikis_date = QDateEdit()
        self.cikis_date.setCalendarPopup(True)
        self.cikis_date.setDate(QDate.currentDate().addDays(1))
        self.cikis_date.setDisplayFormat("dd/MM/yyyy")
        self._add_form_row(layout, "Çıkış Tarihi", self.cikis_date, zorunlu=False)

        # Odeme yontemi
        self.odeme_combo = QComboBox()
        self.odeme_combo.addItems(["Nakit", "Kredi Kartı", "Banka Kartı"])
        self._add_form_row(layout, "Ödeme Yöntemi", self.odeme_combo)

        # Odeme tutari
        self.odeme_spin = QDoubleSpinBox()
        self.odeme_spin.setRange(0, 999999.99)
        self.odeme_spin.setSpecialValueText("Boş (ödeme alınmadı)")
        self.odeme_spin.setValue(0)
        self.odeme_spin.setSuffix(" ₺")
        self.odeme_spin.setDecimals(2)
        self._add_form_row(layout, "Ödeme Tutarı", self.odeme_spin, zorunlu=False)

    def _load_data(self):
        # Autocomplete verisini yukle
        ac_data = self.dm.get_autocomplete_data()
        for edit in [self.tc_edit, self.isim_edit, self.soyisim_edit]:
            edit.set_data(ac_data)
        # Musait odalari yukle
        self.refresh_oda_listesi()

    def refresh_oda_listesi(self):
        self.oda_combo.clear()
        musait = self.dm.get_musait_odalar()
        if musait:
            for oda in sorted(musait, key=lambda x: int(x) if x.isdigit() else x):
                self.oda_combo.addItem(f"Oda {oda}", oda)
        else:
            self.oda_combo.addItem("Müsait oda yok", "")

    def _fill_from_suggestion(self, data):
        """Autocomplete onerisi secildiginde alanlari doldur"""
        self.tc_edit.blockSignals(True)
        self.isim_edit.blockSignals(True)
        self.soyisim_edit.blockSignals(True)

        self.tc_edit.setText(str(data.get("tc", "")))
        self.isim_edit.setText(str(data.get("isim", "")))
        self.soyisim_edit.setText(str(data.get("soyisim", "")))

        # Son kalinan odayi sec (musaitse)
        son_oda = str(data.get("oda", ""))
        if son_oda:
            for i in range(self.oda_combo.count()):
                if str(self.oda_combo.itemData(i)) == son_oda:
                    self.oda_combo.setCurrentIndex(i)
                    break

        self.tc_edit.blockSignals(False)
        self.isim_edit.blockSignals(False)
        self.soyisim_edit.blockSignals(False)

    def _validate(self):
        errors = []
        tc = self.tc_edit.text().strip()
        if not tc:
            errors.append("T.C. Kimlik No zorunludur.")
        elif not tc.isdigit() or len(tc) != 11:
            errors.append("T.C. Kimlik No 11 haneli sayı olmalıdır.")

        if not self.isim_edit.text().strip():
            errors.append("İsim zorunludur.")

        if not self.soyisim_edit.text().strip():
            errors.append("Soyisim zorunludur.")

        oda = self.oda_combo.currentData()
        if not oda:
            errors.append("Lütfen müsait bir oda seçin.")

        return errors

    def _on_kaydet(self):
        errors = self._validate()
        if errors:
            QMessageBox.warning(self, "Eksik Bilgi", "\n".join(errors))
            return

        tc = self.tc_edit.text().strip()
        isim = self.isim_edit.text().strip().upper()
        soyisim = self.soyisim_edit.text().strip().upper()
        oda = self.oda_combo.currentData()
        giris = self.giris_date.date().toPyDate()
        cikis = self.cikis_date.date().toPyDate()
        odeme_yon = self.odeme_combo.currentText()
        odeme_tut = self.odeme_spin.value() if self.odeme_spin.value() > 0 else None

        try:
            kayit_id = self.dm.kayit_ekle(tc, isim, soyisim, oda, giris, cikis, odeme_yon, odeme_tut)
            QMessageBox.information(
                self, "Başarılı",
                f"✅ Kayıt başarıyla oluşturuldu!\n\nKayıt ID: {kayit_id}\n"
                f"Misafir: {isim} {soyisim}\nOda: {oda}"
            )
            self._temizle()
            self.kayit_yapildi.emit()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kayıt sırasında hata oluştu:\n{str(e)}")

    def _temizle(self):
        self.tc_edit.clear()
        self.isim_edit.clear()
        self.soyisim_edit.clear()
        self.giris_date.setDate(QDate.currentDate())
        self.cikis_date.setDate(QDate.currentDate().addDays(1))
        self.odeme_combo.setCurrentIndex(0)
        self.odeme_spin.setValue(0)
        self.refresh_oda_listesi()
        # Autocomplete verisini guncelle
        ac_data = self.dm.get_autocomplete_data()
        for edit in [self.tc_edit, self.isim_edit, self.soyisim_edit]:
            edit.set_data(ac_data)

    def refresh(self):
        self._load_data()
