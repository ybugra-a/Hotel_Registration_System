"""
Aktif Musteri Paneli - Icerde olan musterilerin karti
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QMessageBox, QDialog, QDialogButtonBox,
    QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox, QGridLayout,
    QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtGui import QFont


class DuzenleDialog(QDialog):
    """Musteri bilgilerini duzenleme dialogu"""
    def __init__(self, musteri, data_manager, parent=None):
        super().__init__(parent)
        self.musteri = musteri
        self.dm = data_manager
        self.setWindowTitle(f"Düzenle - {musteri.get('isim','')} {musteri.get('soyisim','')}")
        self.setMinimumWidth(450)
        self.setModal(True)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        baslik = QLabel("✏️  Kayıt Düzenleme")
        baslik.setStyleSheet("font-size: 13pt; font-weight: bold; color: #1B3A6B; margin-bottom: 5px;")
        layout.addWidget(baslik)

        grid = QGridLayout()
        grid.setSpacing(8)
        grid.setColumnMinimumWidth(0, 130)

        def add_row(row, label, widget):
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl, row, 0)
            grid.addWidget(widget, row, 1)

        # TC
        self.tc_edit = QLineEdit(str(self.musteri.get('tc', '')))
        self.tc_edit.setMaxLength(11)
        add_row(0, "T.C. Kimlik No:", self.tc_edit)

        # Isim
        self.isim_edit = QLineEdit(str(self.musteri.get('isim', '')))
        add_row(1, "İsim:", self.isim_edit)

        # Soyisim
        self.soyisim_edit = QLineEdit(str(self.musteri.get('soyisim', '')))
        add_row(2, "Soyisim:", self.soyisim_edit)

        # Oda
        self.oda_combo = QComboBox()
        musait = self.dm.get_musait_odalar()
        mevcut_oda = str(self.musteri.get('oda', ''))
        # Mevcut odayi da ekle (dolu olsa bile duzenlerken gosterilmeli)
        tum_odalar = [mevcut_oda] + [o for o in musait if o != mevcut_oda]
        for oda in sorted(tum_odalar, key=lambda x: int(x) if x.isdigit() else x):
            self.oda_combo.addItem(f"Oda {oda}", oda)
        # Mevcut odayi sec
        for i in range(self.oda_combo.count()):
            if self.oda_combo.itemData(i) == mevcut_oda:
                self.oda_combo.setCurrentIndex(i)
                break
        add_row(3, "Oda Numarası:", self.oda_combo)

        # Giris tarihi
        self.giris_date = QDateEdit()
        self.giris_date.setCalendarPopup(True)
        self.giris_date.setDisplayFormat("dd/MM/yyyy")
        giris_str = str(self.musteri.get('giris', ''))
        if giris_str:
            try:
                from datetime import datetime
                dt = datetime.strptime(giris_str, "%d/%m/%Y")
                self.giris_date.setDate(QDate(dt.year, dt.month, dt.day))
            except:
                self.giris_date.setDate(QDate.currentDate())
        add_row(4, "Giriş Tarihi:", self.giris_date)

        # Cikis tarihi
        self.cikis_date = QDateEdit()
        self.cikis_date.setCalendarPopup(True)
        self.cikis_date.setDisplayFormat("dd/MM/yyyy")
        cikis_str = str(self.musteri.get('cikis', ''))
        if cikis_str and cikis_str.strip():
            try:
                from datetime import datetime
                dt = datetime.strptime(cikis_str, "%d/%m/%Y")
                self.cikis_date.setDate(QDate(dt.year, dt.month, dt.day))
            except:
                self.cikis_date.setDate(QDate.currentDate().addDays(1))
        else:
            self.cikis_date.setDate(QDate.currentDate().addDays(1))
        add_row(5, "Çıkış Tarihi:", self.cikis_date)

        # Odeme yontemi
        self.odeme_yon = QComboBox()
        self.odeme_yon.addItems(["Nakit", "Kredi Kartı", "Banka Kartı"])
        mevcut_yon = str(self.musteri.get('odeme_yon', 'Nakit'))
        idx = self.odeme_yon.findText(mevcut_yon)
        if idx >= 0:
            self.odeme_yon.setCurrentIndex(idx)
        add_row(6, "Ödeme Yöntemi:", self.odeme_yon)

        # Odeme tutari
        self.odeme_tut = QDoubleSpinBox()
        self.odeme_tut.setRange(0, 999999.99)
        self.odeme_tut.setSpecialValueText("Boş (ödeme alınmadı)")
        self.odeme_tut.setSuffix(" ₺")
        self.odeme_tut.setDecimals(2)
        mevcut_tut = self.musteri.get('odeme_tut')
        if mevcut_tut:
            try:
                self.odeme_tut.setValue(float(str(mevcut_tut).replace(',', '.')))
            except:
                self.odeme_tut.setValue(0)
        add_row(7, "Ödeme Tutarı:", self.odeme_tut)

        layout.addLayout(grid)

        # Butonlar
        btn_box = QDialogButtonBox()
        btn_kaydet = QPushButton("💾  Kaydet")
        btn_kaydet.setObjectName("btnKaydet")
        btn_iptal = QPushButton("İptal")
        btn_iptal.setObjectName("btnTemizle")
        btn_kaydet.clicked.connect(self._on_kaydet)
        btn_iptal.clicked.connect(self.reject)
        btn_box.addButton(btn_kaydet, QDialogButtonBox.AcceptRole)
        btn_box.addButton(btn_iptal, QDialogButtonBox.RejectRole)
        layout.addWidget(btn_box)

    def _on_kaydet(self):
        tc = self.tc_edit.text().strip()
        if not tc.isdigit() or len(tc) != 11:
            QMessageBox.warning(self, "Hata", "T.C. Kimlik No 11 haneli sayı olmalıdır.")
            return

        data = {
            "tc": tc,
            "isim": self.isim_edit.text().strip().upper(),
            "soyisim": self.soyisim_edit.text().strip().upper(),
            "oda": self.oda_combo.currentData(),
            "giris": self.giris_date.date().toPyDate().strftime("%d/%m/%Y"),
            "cikis": self.cikis_date.date().toPyDate().strftime("%d/%m/%Y"),
            "odeme_yon": self.odeme_yon.currentText(),
            "odeme_tut": self.odeme_tut.value() if self.odeme_tut.value() > 0 else ""
        }

        success = self.dm.kayit_guncelle(
            self.musteri["id"],
            self.musteri["sheet"],
            data
        )
        if success:
            self.accept()
        else:
            QMessageBox.critical(self, "Hata", "Kayıt güncellenemedi.")


class MusteriKarti(QFrame):
    """Tek bir misafirin karti"""
    duzenle_clicked = pyqtSignal(dict)
    cikis_clicked = pyqtSignal(dict)

    def __init__(self, musteri, parent=None):
        super().__init__(parent)
        self.musteri = musteri
        self.setObjectName("musteriKart")
        self.setFrameShape(QFrame.StyledPanel)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)

        # Ust satir: isim + oda
        ust = QHBoxLayout()
        isim = f"{self.musteri.get('isim','')} {self.musteri.get('soyisim','')}"
        isim_lbl = QLabel(f"👤  {isim}")
        isim_lbl.setObjectName("musteriIsim")
        ust.addWidget(isim_lbl)
        ust.addStretch()

        oda_lbl = QLabel(f"🏠  Oda {self.musteri.get('oda','')}")
        oda_lbl.setObjectName("musteriOda")
        ust.addWidget(oda_lbl)
        layout.addLayout(ust)

        # Tarih satiri
        giris = self.musteri.get('giris', '-')
        cikis = self.musteri.get('cikis', '-') or 'Belirtilmedi'
        tarih_lbl = QLabel(f"📅  Giriş: {giris}  →  Çıkış: {cikis}")
        tarih_lbl.setObjectName("musteriTarih")
        layout.addWidget(tarih_lbl)

        # Odeme satiri
        odeme_tut = self.musteri.get('odeme_tut')
        odeme_yon = self.musteri.get('odeme_yon', '')
        if odeme_tut and str(odeme_tut).strip() and str(odeme_tut) != '0' and str(odeme_tut) != '0.0':
            try:
                tutar = float(str(odeme_tut).replace(',', '.'))
                odeme_lbl = QLabel(f"💳  {odeme_yon}  —  {tutar:,.2f} ₺")
                odeme_lbl.setObjectName("odemeVar")
            except:
                odeme_lbl = QLabel(f"💳  {odeme_yon}")
                odeme_lbl.setObjectName("odemeVar")
        else:
            odeme_lbl = QLabel("⚠  Ödeme Alınmadı")
            odeme_lbl.setObjectName("odemeUyari")
        layout.addWidget(odeme_lbl)

        # Butonlar
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(6)
        btn_layout.addStretch()

        btn_duzenle = QPushButton("✏  Düzenle")
        btn_duzenle.setObjectName("btnDuzenle")
        btn_duzenle.clicked.connect(lambda: self.duzenle_clicked.emit(self.musteri))
        btn_layout.addWidget(btn_duzenle)

        btn_cikis = QPushButton("🚪  Çıkış Yaptır")
        btn_cikis.setObjectName("btnCikis")
        btn_cikis.clicked.connect(lambda: self.cikis_clicked.emit(self.musteri))
        btn_layout.addWidget(btn_cikis)

        layout.addLayout(btn_layout)


class AktifMusteriPaneli(QWidget):
    guncelleme_gerekli = pyqtSignal()

    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.dm = data_manager
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Kart cercevesi
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(8)
        main_layout.addWidget(card)

        # Baslik + sayac
        baslik_row = QHBoxLayout()
        baslik = QLabel("🏨  Aktif Misafirler")
        baslik.setObjectName("panelTitle")
        baslik_row.addWidget(baslik)
        baslik_row.addStretch()
        self.sayac_lbl = QLabel("0 misafir")
        self.sayac_lbl.setStyleSheet("color: #64748b; font-size: 9pt;")
        baslik_row.addWidget(self.sayac_lbl)
        card_layout.addLayout(baslik_row)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #e2e8f0;")
        card_layout.addWidget(sep)

        # Scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setFrameShape(QFrame.NoFrame)
        card_layout.addWidget(self.scroll)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(6)
        self.scroll_layout.addStretch()
        self.scroll.setWidget(self.scroll_widget)

    def refresh(self):
        # Mevcut karti temizle
        while self.scroll_layout.count() > 1:
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        musteriler = self.dm.get_aktif_musteriler()
        self.sayac_lbl.setText(f"{len(musteriler)} misafir")

        if not musteriler:
            bos_lbl = QLabel("Şu an aktif misafir bulunmuyor.")
            bos_lbl.setObjectName("bosaMessaj")
            bos_lbl.setAlignment(Qt.AlignCenter)
            bos_lbl.setStyleSheet("color: #94a3b8; font-size: 12pt; padding: 40px;")
            self.scroll_layout.insertWidget(0, bos_lbl)
            return

        for m in musteriler:
            kart = MusteriKarti(m)
            kart.duzenle_clicked.connect(self._on_duzenle)
            kart.cikis_clicked.connect(self._on_cikis)
            self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, kart)

    def _on_duzenle(self, musteri):
        dialog = DuzenleDialog(musteri, self.dm, self)
        dialog.setStyleSheet(self.styleSheet())
        if dialog.exec_() == QDialog.Accepted:
            self.guncelleme_gerekli.emit()

    def _on_cikis(self, musteri):
        isim = f"{musteri.get('isim','')} {musteri.get('soyisim','')}"
        reply = QMessageBox.question(
            self, "Çıkış Onayı",
            f"⚠  {isim} misafirine çıkış yaptırmak istiyor musunuz?\n\n"
            f"Oda {musteri.get('oda','')} müsait durumuna geçecektir.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            success = self.dm.cikis_yaptir(musteri["id"], musteri["sheet"])
            if success:
                QMessageBox.information(self, "Başarılı", f"✅ {isim} çıkışı yapıldı.")
                self.guncelleme_gerekli.emit()
            else:
                QMessageBox.critical(self, "Hata", "Çıkış işlemi gerçekleştirilemedi.")
