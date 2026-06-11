"""
Kayit Modulu - v0.4
Yeni: Rezerve Et, Sirket Ismi, Blacklist kontrolu
"""

from custom_dialog import show_info, show_warning, show_error, show_question
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QDateEdit, QDoubleSpinBox,
    QFrame, QListWidget, QListWidgetItem, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QDate, pyqtSignal, QPoint, QTimer


_CAL_STYLE = """
    QDateEdit::drop-down { border: none; width: 28px; }
    QDateEdit::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid #38bdf8;
        margin-right: 8px;
    }
    QCalendarWidget { background-color: #ffffff; color: #1e293b; }
    QCalendarWidget QWidget { background-color: #ffffff; color: #1e293b; alternate-background-color: #f8fafc; }
    QCalendarWidget QAbstractItemView { background-color: #ffffff; color: #1e293b; selection-background-color: #eff6ff; selection-color: #1e293b; }
    QCalendarWidget QAbstractItemView:enabled { background-color: #ffffff; color: #1e293b; }
    QCalendarWidget QAbstractItemView:disabled { color: #cbd5e1; }
    QCalendarWidget QToolButton { background-color: #ffffff; color: #1e293b; border: none; padding: 4px 8px; font-weight: bold; }
    QCalendarWidget QToolButton:hover { background-color: #f1f5f9; border-radius: 4px; }
    QCalendarWidget QMenu { background-color: #ffffff; color: #1e293b; }
    QCalendarWidget QSpinBox { background-color: #ffffff; color: #1e293b; border: 1px solid #e2e8f0; }
    QCalendarWidget QWidget#qt_calendar_navigationbar { background-color: #f8fafc; border-bottom: 1px solid #e2e8f0; }
"""

_COMBO_STYLE = """
    QComboBox::drop-down { border: none; width: 28px; }
    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid #38bdf8;
        margin-right: 8px;
    }
    QComboBox QAbstractItemView {
        background-color: #ffffff; border: 1.5px solid #e2e8f0;
        color: #1e293b; selection-background-color: #f1f5f9;
        selection-color: #0f172a; outline: none;
    }
    QComboBox QAbstractItemView::item {
        background-color: #ffffff; color: #1e293b; padding: 9px 14px; min-height: 20px;
    }
    QComboBox QAbstractItemView::item:hover { background-color: #f1f5f9; color: #0f172a; }
    QComboBox QAbstractItemView::item:selected { background-color: #f1f5f9; color: #0f172a; }
"""


class AutocompleteLineEdit(QLineEdit):
    oneri_secildi = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = []
        self._popup = QListWidget(None)
        self._popup.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self._popup.setFocusPolicy(Qt.NoFocus)
        self._popup.setMouseTracking(True)
        self._popup.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._popup.setStyleSheet("""
            QListWidget { border: 1.5px solid #3a3a50; border-radius: 8px; background: #252538; font-size: 10pt; }
            QListWidget::item { padding: 9px 14px; border-bottom: 1px solid #2a2a3e; color: #e2e8f0; }
            QListWidget::item:hover, QListWidget::item:selected { background: #2a2a3e; color: #22c55e; }
        """)
        self._popup.itemClicked.connect(self._on_item_selected)
        self.textChanged.connect(self._on_text_changed)

    def set_data(self, data):
        self._data = data

    def _show_popup(self, matches):
        self._popup.clear()
        for m in matches[:8]:
            display = f"{m.get('isim','')} {m.get('soyisim','')}   |   TC: {m.get('tc','')}   |   Son Oda: {m.get('oda','')}"
            item = QListWidgetItem(display)
            item.setData(Qt.UserRole, m)
            self._popup.addItem(item)
        pos = self.mapToGlobal(QPoint(0, self.height()))
        self._popup.move(pos)
        self._popup.setFixedWidth(max(self.width(), 480))
        self._popup.setFixedHeight(min(len(matches), 8) * 38 + 4)
        self._popup.show()
        self._popup.raise_()

    def _on_text_changed(self, text):
        if len(text) < 2:
            self._popup.hide()
            return
        tl = text.lower()
        matches = [i for i in self._data if
                   tl in f"{i.get('isim','')} {i.get('soyisim','')}".lower() or
                   tl in str(i.get('tc','')).lower()]
        if not matches:
            self._popup.hide()
            return
        self._show_popup(matches)

    def _on_item_selected(self, item):
        self._popup.hide()
        data = item.data(Qt.UserRole)
        if data:
            self.oneri_secildi.emit(data)

    def focusOutEvent(self, event):
        QTimer.singleShot(150, self._popup.hide)
        super().focusOutEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self._popup.hide()
        elif event.key() == Qt.Key_Down and self._popup.isVisible():
            self._popup.setCurrentRow(0)
        elif event.key() == Qt.Key_Return and self._popup.isVisible():
            cur = self._popup.currentItem()
            if cur:
                self._on_item_selected(cur)
        else:
            super().keyPressEvent(event)

    def hideEvent(self, event):
        self._popup.hide()
        super().hideEvent(event)


class KayitModulu(QWidget):
    kayit_yapildi = pyqtSignal()
    rezervasyon_yapildi = pyqtSignal()

    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.dm = data_manager
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setObjectName("mainCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 24, 28, 28)
        card_layout.setSpacing(0)
        main_layout.addWidget(card)

        title = QLabel("Yeni Misafir Kaydı")
        title.setObjectName("panelTitle")
        card_layout.addWidget(title)

        subtitle = QLabel("Yeni kayıt için aşağıdaki formu doldurunuz.")
        subtitle.setObjectName("panelSubtitle")
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(20)

        self._add_form_fields(card_layout)
        card_layout.addSpacing(20)

        # Butonlar: Kaydet | Rezerve Et | Temizle
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.btn_kaydet = QPushButton("Kaydet")
        self.btn_kaydet.setObjectName("btnKaydet")
        self.btn_kaydet.clicked.connect(self._on_kaydet)
        self.btn_kaydet.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn_layout.addWidget(self.btn_kaydet)

        self.btn_rezerve = QPushButton("Rezerve Et")
        self.btn_rezerve.setObjectName("btnRezarve")
        self.btn_rezerve.clicked.connect(self._on_rezerve)
        self.btn_rezerve.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn_layout.addWidget(self.btn_rezerve)

        self.btn_temizle = QPushButton("Temizle")
        self.btn_temizle.setObjectName("btnTemizle")
        self.btn_temizle.clicked.connect(self._temizle)
        self.btn_temizle.setFixedWidth(100)
        btn_layout.addWidget(self.btn_temizle)

        card_layout.addLayout(btn_layout)
        card_layout.addStretch()

    def _lbl(self, text):
        l = QLabel(text)
        l.setObjectName("formLabel")
        return l

    def _add_form_fields(self, layout):
        # TC
        layout.addWidget(self._lbl("T.C. KIMLIK NUMARASI *"))
        self.tc_edit = AutocompleteLineEdit()
        self.tc_edit.setPlaceholderText("11 haneli kimlik numarası")
        self.tc_edit.setMaxLength(11)
        self.tc_edit.oneri_secildi.connect(self._fill_from_suggestion)
        layout.addWidget(self.tc_edit)
        layout.addSpacing(10)

        # Ad | Soyad
        row1 = QHBoxLayout()
        row1.setSpacing(10)

        c1 = QVBoxLayout(); c1.setSpacing(4)
        c1.addWidget(self._lbl("AD *"))
        self.isim_edit = AutocompleteLineEdit()
        self.isim_edit.setPlaceholderText("Misafir adı")
        self.isim_edit.oneri_secildi.connect(self._fill_from_suggestion)
        c1.addWidget(self.isim_edit)
        row1.addLayout(c1)

        c2 = QVBoxLayout(); c2.setSpacing(4)
        c2.addWidget(self._lbl("SOYAD *"))
        self.soyisim_edit = AutocompleteLineEdit()
        self.soyisim_edit.setPlaceholderText("Misafir soyadı")
        self.soyisim_edit.oneri_secildi.connect(self._fill_from_suggestion)
        c2.addWidget(self.soyisim_edit)
        row1.addLayout(c2)

        layout.addLayout(row1)
        layout.addSpacing(10)

        # Sirket ismi (tam genislik)
        layout.addWidget(self._lbl("SIRKET ISMI"))
        self.sirket_edit = QLineEdit()
        self.sirket_edit.setPlaceholderText("Şirket ismi (opsiyonel)")
        layout.addWidget(self.sirket_edit)
        layout.addSpacing(10)

        # Oda | Odeme yontemi
        row2 = QHBoxLayout(); row2.setSpacing(10)

        c3 = QVBoxLayout(); c3.setSpacing(4)
        c3.addWidget(self._lbl("ODA NUMARASI *"))
        self.oda_combo = QComboBox()
        self.oda_combo.setStyleSheet(_COMBO_STYLE)
        c3.addWidget(self.oda_combo)
        row2.addLayout(c3)

        c4 = QVBoxLayout(); c4.setSpacing(4)
        c4.addWidget(self._lbl("ODEME YONTEMI"))
        self.odeme_combo = QComboBox()
        self.odeme_combo.addItems(["Nakit", "Kredi Karti", "Banka Karti"])
        self.odeme_combo.setStyleSheet(_COMBO_STYLE)
        c4.addWidget(self.odeme_combo)
        row2.addLayout(c4)

        layout.addLayout(row2)
        layout.addSpacing(10)

        # Giris | Cikis tarihi
        row3 = QHBoxLayout(); row3.setSpacing(10)

        c5 = QVBoxLayout(); c5.setSpacing(4)
        c5.addWidget(self._lbl("GIRIŞ TARIHI *"))
        self.giris_date = QDateEdit()
        self.giris_date.setCalendarPopup(True)
        self.giris_date.setDate(QDate.currentDate())
        self.giris_date.setDisplayFormat("dd/MM/yyyy")
        self.giris_date.setStyleSheet(_CAL_STYLE)
        c5.addWidget(self.giris_date)
        row3.addLayout(c5)

        c6 = QVBoxLayout(); c6.setSpacing(4)
        c6.addWidget(self._lbl("CIKIŞ TARIHI"))
        self.cikis_date = QDateEdit()
        self.cikis_date.setCalendarPopup(True)
        self.cikis_date.setDate(QDate.currentDate().addDays(1))
        self.cikis_date.setDisplayFormat("dd/MM/yyyy")
        self.cikis_date.setStyleSheet(_CAL_STYLE)
        c6.addWidget(self.cikis_date)
        row3.addLayout(c6)

        layout.addLayout(row3)
        layout.addSpacing(10)

        # Tutar
        layout.addWidget(self._lbl("TOPLAM TUTAR (TL)"))
        self.odeme_spin = QDoubleSpinBox()
        self.odeme_spin.setRange(0, 999999.99)
        self.odeme_spin.setSpecialValueText("0.00")
        self.odeme_spin.setValue(0)
        self.odeme_spin.setPrefix("TL  ")
        self.odeme_spin.setDecimals(2)
        layout.addWidget(self.odeme_spin)

    def _load_data(self):
        ac_data = self.dm.get_autocomplete_data()
        for edit in [self.tc_edit, self.isim_edit, self.soyisim_edit]:
            edit.set_data(ac_data)
        self.refresh_oda_listesi()

    def refresh_oda_listesi(self):
        self.oda_combo.clear()
        musait = self.dm.get_musait_odalar()
        if musait:
            for oda in sorted(musait, key=lambda x: int(x) if x.isdigit() else x):
                self.oda_combo.addItem(f"Oda {oda}", oda)
        else:
            self.oda_combo.addItem("Musait oda yok", "")

    def _fill_from_suggestion(self, data):
        for e in [self.tc_edit, self.isim_edit, self.soyisim_edit]:
            e.blockSignals(True)
        self.tc_edit.setText(str(data.get("tc","")))
        self.isim_edit.setText(str(data.get("isim","")))
        self.soyisim_edit.setText(str(data.get("soyisim","")))
        self.sirket_edit.setText(str(data.get("sirket","") or ""))
        son_oda = str(data.get("oda",""))
        if son_oda:
            for i in range(self.oda_combo.count()):
                if str(self.oda_combo.itemData(i)) == son_oda:
                    self.oda_combo.setCurrentIndex(i)
                    break
        for e in [self.tc_edit, self.isim_edit, self.soyisim_edit]:
            e.blockSignals(False)

    def _get_form_data(self):
        return {
            "tc": self.tc_edit.text().strip(),
            "isim": self.isim_edit.text().strip().upper(),
            "soyisim": self.soyisim_edit.text().strip().upper(),
            "sirket": self.sirket_edit.text().strip(),
            "oda": self.oda_combo.currentData(),
            "giris": self.giris_date.date().toPyDate(),
            "cikis": self.cikis_date.date().toPyDate(),
            "odeme_yon": self.odeme_combo.currentText(),
            "odeme_tut": self.odeme_spin.value() if self.odeme_spin.value() > 0 else None
        }

    def _validate(self, data):
        errors = []
        if not data["tc"]:
            errors.append("T.C. Kimlik No zorunludur.")
        elif not data["tc"].isdigit() or len(data["tc"]) != 11:
            errors.append("T.C. Kimlik No 11 haneli sayı olmalıdır.")
        if not data["isim"]:
            errors.append("Ad zorunludur.")
        if not data["soyisim"]:
            errors.append("Soyad zorunludur.")
        if not data["oda"]:
            errors.append("Lütfen musait bir oda seçin.")
        return errors

    def _on_kaydet(self):
        data = self._get_form_data()
        errors = self._validate(data)
        if errors:
            show_warning(self, "Eksik Bilgi", "\n".join(errors))
            return
        # Blacklist kontrolu
        if self.dm.blacklist_kontrol(data["tc"]):
            show_error(self, "Kara Liste Uyarısı", "Bu kişi Kara Liste'de!\n\nKayit işlemi iptal edildi.")
            return
        try:
            kid = self.dm.kayit_ekle(
                data["tc"], data["isim"], data["soyisim"], data["sirket"],
                data["oda"], data["giris"], data["cikis"],
                data["odeme_yon"], data["odeme_tut"]
            )
            show_info(self, "Başarılı", f"Kayıt oluşturuldu!\nID: {kid}\nMisafir: {data['isim']} {data['soyisim']}\nOda: {data['oda']}")
            self._temizle()
            self.kayit_yapildi.emit()
        except Exception as e:
            show_error(self, "Hata", f"Kayıt sırasında hata oluştu:\n{str(e)}")

    def _on_rezerve(self):
        data = self._get_form_data()
        errors = self._validate(data)
        if errors:
            show_warning(self, "Eksik Bilgi", "\n".join(errors))
            return
        if self.dm.blacklist_kontrol(data["tc"]):
            show_error(self, "Kara Liste Uyarısı", "Bu kişi Kara Liste'de!\n\nRezervasyon işlemi iptal edildi.")
            return
        try:
            rid = self.dm.rezervasyon_ekle(
                data["tc"], data["isim"], data["soyisim"], data["sirket"],
                data["oda"], data["giris"], data["cikis"],
                data["odeme_yon"], data["odeme_tut"]
            )
            show_info(self, "Rezervasyon Oluşturuldu", f"Rezervasyon kaydedildi!\nRez. ID: {rid}\nMisafir: {data['isim']} {data['soyisim']}\nGiriş Tarihi: {data['giris'].strftime('%d/%m/%Y')}")
            self._temizle()
            self.rezervasyon_yapildi.emit()
        except Exception as e:
            show_error(self, "Hata", f"Rezervasyon sırasında hata oluştu:\n{str(e)}")

    def _temizle(self):
        self.tc_edit.clear()
        self.isim_edit.clear()
        self.soyisim_edit.clear()
        self.sirket_edit.clear()
        self.giris_date.setDate(QDate.currentDate())
        self.cikis_date.setDate(QDate.currentDate().addDays(1))
        self.odeme_combo.setCurrentIndex(0)
        self.odeme_spin.setValue(0)
        self.refresh_oda_listesi()
        ac_data = self.dm.get_autocomplete_data()
        for e in [self.tc_edit, self.isim_edit, self.soyisim_edit]:
            e.set_data(ac_data)

    def refresh(self):
        self._load_data()
