"""
Aktif Musteri Paneli - Stitch UI dark tema
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QMessageBox, QDialog, QDialogButtonBox,
    QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox, QGridLayout,
    QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtGui import QFont, QColor


class DuzenleDialog(QDialog):
    def __init__(self, musteri, data_manager, parent=None):
        super().__init__(parent)
        self.musteri = musteri
        self.dm = data_manager
        self.setWindowTitle(f"Duzenle - {musteri.get('isim','')} {musteri.get('soyisim','')}")
        self.setMinimumWidth(460)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog { background-color: #1a2635; }
            QLabel { color: #94a3b8; }
            QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox {
                background-color: #131f2e;
                border: 1.5px solid #2a3a4a;
                border-radius: 8px;
                padding: 8px 12px;
                color: #e2e8f0;
                min-height: 22px;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border-color: #22c55e;
            }
            QPushButton {
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: bold;
                min-height: 36px;
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #1a2635;
                color: #e2e8f0;
                selection-background-color: #22c55e22;
            }
        """)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        baslik = QLabel("Kayit Duzenleme")
        baslik.setStyleSheet("font-size: 13pt; font-weight: bold; color: #f1f5f9;")
        layout.addWidget(baslik)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setColumnMinimumWidth(0, 130)

        def add_row(row, label, widget):
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl, row, 0)
            grid.addWidget(widget, row, 1)

        self.tc_edit = QLineEdit(str(self.musteri.get('tc', '')))
        self.tc_edit.setMaxLength(11)
        add_row(0, "T.C. Kimlik No:", self.tc_edit)

        self.isim_edit = QLineEdit(str(self.musteri.get('isim', '')))
        add_row(1, "Isim:", self.isim_edit)

        self.soyisim_edit = QLineEdit(str(self.musteri.get('soyisim', '')))
        add_row(2, "Soyisim:", self.soyisim_edit)

        self.oda_combo = QComboBox()
        musait = self.dm.get_musait_odalar()
        mevcut_oda = str(self.musteri.get('oda', ''))
        tum_odalar = [mevcut_oda] + [o for o in musait if o != mevcut_oda]
        for oda in sorted(tum_odalar, key=lambda x: int(x) if x.isdigit() else x):
            self.oda_combo.addItem(f"Oda {oda}", oda)
        for i in range(self.oda_combo.count()):
            if self.oda_combo.itemData(i) == mevcut_oda:
                self.oda_combo.setCurrentIndex(i)
                break
        add_row(3, "Oda Numarasi:", self.oda_combo)

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
        add_row(4, "Giris Tarihi:", self.giris_date)

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
        add_row(5, "Cikis Tarihi:", self.cikis_date)

        self.odeme_yon = QComboBox()
        self.odeme_yon.addItems(["Nakit", "Kredi Karti", "Banka Karti"])
        mevcut_yon = str(self.musteri.get('odeme_yon', 'Nakit'))
        idx = self.odeme_yon.findText(mevcut_yon)
        if idx >= 0:
            self.odeme_yon.setCurrentIndex(idx)
        add_row(6, "Odeme Yontemi:", self.odeme_yon)

        self.odeme_tut = QDoubleSpinBox()
        self.odeme_tut.setRange(0, 999999.99)
        self.odeme_tut.setSpecialValueText("Bos (odeme alinmadi)")
        self.odeme_tut.setSuffix(" TL")
        self.odeme_tut.setDecimals(2)
        mevcut_tut = self.musteri.get('odeme_tut')
        if mevcut_tut:
            try:
                self.odeme_tut.setValue(float(str(mevcut_tut).replace(',', '.')))
            except:
                self.odeme_tut.setValue(0)
        add_row(7, "Odeme Tutari:", self.odeme_tut)

        layout.addLayout(grid)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_iptal = QPushButton("Iptal")
        btn_iptal.setStyleSheet("background-color: #1e2d3d; color: #94a3b8; border: 1px solid #2a3a4a;")
        btn_iptal.clicked.connect(self.reject)
        btn_layout.addWidget(btn_iptal)

        btn_kaydet = QPushButton("Kaydet")
        btn_kaydet.setStyleSheet("background-color: #22c55e; color: #0f1923;")
        btn_kaydet.clicked.connect(self._on_kaydet)
        btn_layout.addWidget(btn_kaydet)

        layout.addLayout(btn_layout)

    def _on_kaydet(self):
        tc = self.tc_edit.text().strip()
        if not tc.isdigit() or len(tc) != 11:
            QMessageBox.warning(self, "Hata", "T.C. Kimlik No 11 haneli sayi olmalidir.")
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

        success = self.dm.kayit_guncelle(self.musteri["id"], self.musteri["sheet"], data)
        if success:
            self.accept()
        else:
            QMessageBox.critical(self, "Hata", "Kayit guncellenemedi.")


class AvatarWidget(QLabel):
    """Isim baş harflerinden avatar"""
    def __init__(self, isim, soyisim, parent=None):
        super().__init__(parent)
        initials = f"{isim[:1]}{soyisim[:1]}".upper() if isim and soyisim else "?"
        self.setText(initials)
        self.setFixedSize(44, 44)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: #2a3a4a;
                color: #94a3b8;
                border-radius: 22px;
                font-size: 13pt;
                font-weight: bold;
            }
        """)


class MusteriKarti(QFrame):
    duzenle_clicked = pyqtSignal(dict)
    cikis_clicked = pyqtSignal(dict)

    def __init__(self, musteri, parent=None):
        super().__init__(parent)
        self.musteri = musteri
        self.setObjectName("musteriKart")
        self.setFrameShape(QFrame.StyledPanel)
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(14)

        # Avatar
        isim = str(self.musteri.get('isim', ''))
        soyisim = str(self.musteri.get('soyisim', ''))
        avatar = AvatarWidget(isim, soyisim)
        layout.addWidget(avatar)

        # Orta: bilgiler
        info_col = QVBoxLayout()
        info_col.setSpacing(4)

        isim_lbl = QLabel(f"{isim} {soyisim}")
        isim_lbl.setObjectName("musteriIsim")
        info_col.addWidget(isim_lbl)

        oda = self.musteri.get('oda', '')
        giris = self.musteri.get('giris', '')
        cikis = self.musteri.get('cikis', '') or 'Belirtilmedi'
        alt_lbl = QLabel(f"Oda {oda}   •   {giris} - {cikis}")
        alt_lbl.setObjectName("musteriTarih")
        info_col.addWidget(alt_lbl)

        layout.addLayout(info_col)
        layout.addStretch()

        # Sag: odeme badge + butonlar
        sag_col = QVBoxLayout()
        sag_col.setSpacing(8)
        sag_col.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Odeme badge
        odeme_tut = self.musteri.get('odeme_tut')
        odeme_yon = self.musteri.get('odeme_yon', '')
        if odeme_tut and str(odeme_tut).strip() and str(odeme_tut) not in ['0', '0.0']:
            badge = QLabel("ODENDI")
            badge.setObjectName("odemeVar")
        else:
            badge = QLabel("EKSIK ODEME")
            badge.setObjectName("odemeUyari")
        badge.setAlignment(Qt.AlignCenter)
        sag_col.addWidget(badge)

        # Butonlar
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        btn_duzenle = QPushButton("Duzenle")
        btn_duzenle.setObjectName("btnDuzenle")
        btn_duzenle.clicked.connect(lambda: self.duzenle_clicked.emit(self.musteri))
        btn_row.addWidget(btn_duzenle)

        btn_cikis = QPushButton("Cikis Yap")
        btn_cikis.setObjectName("btnCikis")
        btn_cikis.clicked.connect(lambda: self.cikis_clicked.emit(self.musteri))
        btn_row.addWidget(btn_cikis)

        sag_col.addLayout(btn_row)
        layout.addLayout(sag_col)


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

        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                background-color: #1a2635;
                border-radius: 12px;
                border: 1px solid #1e2d3d;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(8)
        main_layout.addWidget(card)

        # Baslik satiri
        baslik_row = QHBoxLayout()
        baslik = QLabel("Aktif Misafirler")
        baslik.setObjectName("panelTitle")
        baslik_row.addWidget(baslik)
        baslik_row.addStretch()

        self.sayac_badge = QLabel("0 ODA DOLU")
        self.sayac_badge.setStyleSheet("""
            QLabel {
                background-color: #22c55e22;
                color: #22c55e;
                border-radius: 4px;
                padding: 3px 10px;
                font-size: 9pt;
                font-weight: bold;
            }
        """)
        baslik_row.addWidget(self.sayac_badge)
        card_layout.addLayout(baslik_row)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #1e2d3d; background-color: #1e2d3d; max-height: 1px;")
        card_layout.addWidget(sep)

        # Scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        card_layout.addWidget(self.scroll)

        self.scroll_widget = QWidget()
        self.scroll_widget.setStyleSheet("background: transparent;")
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(8)
        self.scroll_layout.addStretch()
        self.scroll.setWidget(self.scroll_widget)

        # Alt bilgi satiri
        alt_row = QHBoxLayout()
        self.toplam_lbl = QLabel("Toplam: 0 Misafir")
        self.toplam_lbl.setStyleSheet("color: #64748b; font-size: 9pt;")
        alt_row.addWidget(self.toplam_lbl)
        alt_row.addStretch()
        card_layout.addLayout(alt_row)

    def refresh(self):
        while self.scroll_layout.count() > 1:
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        musteriler = self.dm.get_aktif_musteriler()
        count = len(musteriler)
        self.sayac_badge.setText(f"{count} ODA DOLU")
        self.toplam_lbl.setText(f"Toplam: {count} Misafir")

        if not musteriler:
            bos_lbl = QLabel("Su an aktif misafir bulunmuyor.")
            bos_lbl.setObjectName("bosaMessaj")
            bos_lbl.setAlignment(Qt.AlignCenter)
            bos_lbl.setStyleSheet("color: #2a3a4a; font-size: 12pt; padding: 40px;")
            self.scroll_layout.insertWidget(0, bos_lbl)
            return

        for m in musteriler:
            kart = MusteriKarti(m)
            kart.duzenle_clicked.connect(self._on_duzenle)
            kart.cikis_clicked.connect(self._on_cikis)
            self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, kart)

    def _on_duzenle(self, musteri):
        dialog = DuzenleDialog(musteri, self.dm, self)
        if dialog.exec_() == QDialog.Accepted:
            self.guncelleme_gerekli.emit()

    def _on_cikis(self, musteri):
        isim = f"{musteri.get('isim','')} {musteri.get('soyisim','')}"
        reply = QMessageBox.question(
            self, "Cikis Onayi",
            f"{isim} misafirine cikis yaptirmak istiyor musunuz?\n\n"
            f"Oda {musteri.get('oda','')} musait durumuna gececektir.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            success = self.dm.cikis_yaptir(musteri["id"], musteri["sheet"])
            if success:
                self.guncelleme_gerekli.emit()
            else:
                QMessageBox.critical(self, "Hata", "Cikis islemi gerceklestirilemedi.")
