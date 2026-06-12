"""
Aktif Musteri Paneli - v0.4
"""

from custom_dialog import show_info, show_warning, show_error, show_question
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QMessageBox, QDialog,
    QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox, QGridLayout
)
from PyQt5.QtCore import Qt, pyqtSignal, QDate

_CAL_STYLE = """
    QDateEdit::drop-down { border: none; width: 28px; }
    QDateEdit::down-arrow {
        image: none; border-left: 5px solid transparent;
        border-right: 5px solid transparent; border-top: 6px solid #38bdf8; margin-right: 8px;
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
        image: none; border-left: 5px solid transparent;
        border-right: 5px solid transparent; border-top: 6px solid #38bdf8; margin-right: 8px;
    }
    QComboBox QAbstractItemView {
        background-color: #ffffff; border: 1.5px solid #e2e8f0; color: #1e293b;
        selection-background-color: #f1f5f9; selection-color: #0f172a; outline: none;
    }
    QComboBox QAbstractItemView::item { background-color: #ffffff; color: #1e293b; padding: 9px 14px; min-height: 20px; }
    QComboBox QAbstractItemView::item:hover { background-color: #f1f5f9; color: #0f172a; }
    QComboBox QAbstractItemView::item:selected { background-color: #f1f5f9; color: #0f172a; }
"""


class DuzenleDialog(QDialog):
    def __init__(self, musteri, data_manager, parent=None):
        super().__init__(parent)
        self.musteri = musteri
        self.dm = data_manager
        self.setWindowTitle(f"Duzenle - {musteri.get('isim','')} {musteri.get('soyisim','')}")
        self.setMinimumWidth(480)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog { background-color: #252538; }
            QLabel { color: #94a3b8; font-size: 8pt; font-weight: bold; letter-spacing: 0.5px; }
            QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox {
                background-color: #1e1e30; border: 1.5px solid #3a3a50;
                border-radius: 8px; padding: 9px 12px; color: #e2e8f0; min-height: 22px;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus { border-color: #22c55e; }
            QPushButton { border-radius: 8px; padding: 9px 20px; font-weight: 600; min-height: 38px; border: none; }
        """)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(28, 24, 28, 24)

        title = QLabel("Kayit Duzenleme")
        title.setStyleSheet("font-size: 13pt; font-weight: bold; color: #ffffff; background: transparent;")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setColumnMinimumWidth(0, 140)

        def lbl(t):
            l = QLabel(t)
            l.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            return l

        self.tc_edit = QLineEdit(str(self.musteri.get('tc', '')))
        self.tc_edit.setMaxLength(11)
        grid.addWidget(lbl("T.C. KIMLIK NO"), 0, 0)
        grid.addWidget(self.tc_edit, 0, 1)

        self.isim_edit = QLineEdit(str(self.musteri.get('isim', '')))
        grid.addWidget(lbl("AD"), 1, 0)
        grid.addWidget(self.isim_edit, 1, 1)

        self.soyisim_edit = QLineEdit(str(self.musteri.get('soyisim', '')))
        grid.addWidget(lbl("SOYAD"), 2, 0)
        grid.addWidget(self.soyisim_edit, 2, 1)

        self.sirket_edit = QLineEdit(str(self.musteri.get('sirket', '') or ''))
        self.sirket_edit.setPlaceholderText("Opsiyonel")
        grid.addWidget(lbl("SIRKET ISMI"), 3, 0)
        grid.addWidget(self.sirket_edit, 3, 1)

        self.oda_combo = QComboBox()
        self.oda_combo.setStyleSheet(_COMBO_STYLE)
        musait = self.dm.get_musait_odalar()
        mevcut_oda = str(self.musteri.get('oda', ''))
        tum = [mevcut_oda] + [o for o in musait if o != mevcut_oda]
        for oda in sorted(tum, key=lambda x: int(x) if x.isdigit() else x):
            self.oda_combo.addItem(f"Oda {oda}", oda)
        for i in range(self.oda_combo.count()):
            if self.oda_combo.itemData(i) == mevcut_oda:
                self.oda_combo.setCurrentIndex(i)
                break
        grid.addWidget(lbl("ODA NUMARASI"), 4, 0)
        grid.addWidget(self.oda_combo, 4, 1)

        self.giris_date = QDateEdit()
        self.giris_date.setCalendarPopup(True)
        self.giris_date.setDisplayFormat("dd/MM/yyyy")
        self.giris_date.setStyleSheet(_CAL_STYLE)
        giris_str = str(self.musteri.get('giris', ''))
        if giris_str:
            try:
                from datetime import datetime
                dt = datetime.strptime(giris_str, "%d/%m/%Y")
                self.giris_date.setDate(QDate(dt.year, dt.month, dt.day))
            except:
                self.giris_date.setDate(QDate.currentDate())
        grid.addWidget(lbl("GIRIS TARIHI"), 5, 0)
        grid.addWidget(self.giris_date, 5, 1)

        self.cikis_date = QDateEdit()
        self.cikis_date.setCalendarPopup(True)
        self.cikis_date.setDisplayFormat("dd/MM/yyyy")
        self.cikis_date.setStyleSheet(_CAL_STYLE)
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
        grid.addWidget(lbl("CIKIS TARIHI"), 6, 0)
        grid.addWidget(self.cikis_date, 6, 1)

        self.odeme_yon = QComboBox()
        self.odeme_yon.setStyleSheet(_COMBO_STYLE)
        self.odeme_yon.addItems(["Nakit", "Kredi Karti", "Banka Karti"])
        idx = self.odeme_yon.findText(str(self.musteri.get('odeme_yon', 'Nakit')))
        if idx >= 0:
            self.odeme_yon.setCurrentIndex(idx)
        grid.addWidget(lbl("ODEME YONTEMI"), 7, 0)
        grid.addWidget(self.odeme_yon, 7, 1)

        self.odeme_tut = QDoubleSpinBox()
        self.odeme_tut.setRange(0, 999999.99)
        self.odeme_tut.setSpecialValueText("Odeme alinmadi")
        self.odeme_tut.setPrefix("TL  ")
        self.odeme_tut.setDecimals(2)
        try:
            self.odeme_tut.setValue(float(str(self.musteri.get('odeme_tut', 0) or 0).replace(',', '.')))
        except:
            self.odeme_tut.setValue(0)
        grid.addWidget(lbl("ODEME TUTARI"), 8, 0)
        grid.addWidget(self.odeme_tut, 8, 1)

        layout.addLayout(grid)

        btn_row = QHBoxLayout()
        btn_row.addStretch()

        btn_iptal = QPushButton("Iptal")
        btn_iptal.setStyleSheet("background: rgba(100,116,139,0.12); color: #94a3b8; border: 2px solid #475569;")
        btn_iptal.clicked.connect(self.reject)
        btn_row.addWidget(btn_iptal)

        btn_kaydet = QPushButton("Kaydet")
        btn_kaydet.setStyleSheet("background: rgba(34,197,94,0.15); color: #22c55e; border: 2px solid #22c55e;")
        btn_kaydet.clicked.connect(self._on_kaydet)
        btn_row.addWidget(btn_kaydet)
        layout.addLayout(btn_row)

    def _on_kaydet(self):
        tc = self.tc_edit.text().strip()
        if not tc.isdigit() or len(tc) != 11:
            show_warning(self, "Hata", "T.C. Kimlik No 11 haneli sayı olmalıdır.")
            return
        data = {
            "tc": tc,
            "isim": self.isim_edit.text().strip().upper(),
            "soyisim": self.soyisim_edit.text().strip().upper(),
            "sirket": self.sirket_edit.text().strip(),
            "oda": self.oda_combo.currentData(),
            "giris": self.giris_date.date().toPyDate().strftime("%d/%m/%Y"),
            "cikis": self.cikis_date.date().toPyDate().strftime("%d/%m/%Y"),
            "odeme_yon": self.odeme_yon.currentText(),
            "odeme_tut": self.odeme_tut.value() if self.odeme_tut.value() > 0 else ""
        }
        if self.dm.kayit_guncelle(self.musteri["id"], self.musteri["sheet"], data):
            self.accept()
        else:
            show_error(self, "Hata", "Kayıt güncellenemedi.")


class AvatarWidget(QLabel):
    def __init__(self, isim, soyisim, parent=None):
        super().__init__(parent)
        initials = f"{isim[:1]}{soyisim[:1]}".upper() if isim and soyisim else "?"
        self.setText(initials)
        self.setFixedSize(46, 46)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("QLabel { background-color: #2a2a3e; color: #94a3b8; border-radius: 23px; font-size: 13pt; font-weight: bold; }")


class MusteriKarti(QFrame):
    duzenle_clicked = pyqtSignal(dict)
    cikis_clicked = pyqtSignal(dict)
    sil_clicked = pyqtSignal(dict)

    def __init__(self, musteri, parent=None):
        super().__init__(parent)
        self.musteri = musteri
        self.setObjectName("musteriKart")
        self.setFrameShape(QFrame.StyledPanel)
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(14)

        isim = str(self.musteri.get('isim', ''))
        soyisim = str(self.musteri.get('soyisim', ''))
        sirket = str(self.musteri.get('sirket', '') or '')

        avatar = AvatarWidget(isim, soyisim)
        layout.addWidget(avatar)

        info = QVBoxLayout()
        info.setSpacing(3)

        isim_lbl = QLabel(f"{isim} {soyisim}")
        isim_lbl.setObjectName("musteriIsim")
        info.addWidget(isim_lbl)

        if sirket:
            sirket_lbl = QLabel(sirket)
            sirket_lbl.setStyleSheet("color: #64748b; font-size: 9pt; font-style: italic; background: transparent;")
            info.addWidget(sirket_lbl)

        oda = str(self.musteri.get('oda', ''))
        giris = str(self.musteri.get('giris', ''))
        cikis = str(self.musteri.get('cikis', '') or 'Belirtilmedi')

        alt_row = QHBoxLayout()
        alt_row.setSpacing(8)
        oda_lbl = QLabel(f"Oda {oda}")
        oda_lbl.setObjectName("musteriOda")
        alt_row.addWidget(oda_lbl)
        tarih_lbl = QLabel(f"  •  {giris} - {cikis}")
        tarih_lbl.setObjectName("musteriTarih")
        alt_row.addWidget(tarih_lbl)
        alt_row.addStretch()
        info.addLayout(alt_row)
        layout.addLayout(info)
        layout.addStretch()

        sag = QVBoxLayout()
        sag.setSpacing(8)
        sag.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        odeme_tut = self.musteri.get('odeme_tut')
        if odeme_tut and str(odeme_tut).strip() not in ['', '0', '0.0']:
            badge = QLabel("ODENDI")
            badge.setObjectName("odemeVar")
        else:
            badge = QLabel("EKSIK ODEME")
            badge.setObjectName("odemeUyari")
        badge.setAlignment(Qt.AlignCenter)
        sag.addWidget(badge)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)

        btn_duzenle = QPushButton("Duzenle")
        btn_duzenle.setObjectName("btnDuzenle")
        btn_duzenle.clicked.connect(lambda: self.duzenle_clicked.emit(self.musteri))
        btn_row.addWidget(btn_duzenle)

        btn_cikis = QPushButton("Check-out")
        btn_cikis.setObjectName("btnCikis")
        btn_cikis.clicked.connect(lambda: self.cikis_clicked.emit(self.musteri))
        btn_row.addWidget(btn_cikis)

        btn_sil = QPushButton("Sil")
        btn_sil.setObjectName("btnSil")
        btn_sil.setFont(__import__("PyQt5.QtGui", fromlist=["QFont"]).QFont("Segoe UI", 9))
        btn_sil.clicked.connect(lambda: self.sil_clicked.emit(self.musteri))
        btn_row.addWidget(btn_sil)

        sag.addLayout(btn_row)
        layout.addLayout(sag)


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
        card.setObjectName("mainCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 20, 24, 20)
        card_layout.setSpacing(10)
        main_layout.addWidget(card)

        baslik_row = QHBoxLayout()
        col = QVBoxLayout()
        col.setSpacing(2)
        baslik = QLabel("Aktif Misafirler")
        baslik.setObjectName("panelTitle")
        col.addWidget(baslik)
        self.subtitle_lbl = QLabel("Otelde konaklamakta olan misafirler")
        self.subtitle_lbl.setObjectName("panelSubtitle")
        col.addWidget(self.subtitle_lbl)
        baslik_row.addLayout(col)
        baslik_row.addStretch()
        card_layout.addLayout(baslik_row)

        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: #2a2a3e;")
        card_layout.addWidget(sep)

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
        self.scroll_layout.setSpacing(6)
        self.scroll_layout.addStretch()
        self.scroll.setWidget(self.scroll_widget)

    def refresh(self):
        while self.scroll_layout.count() > 1:
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        musteriler = self.dm.get_aktif_musteriler()
        self.subtitle_lbl.setText(f"Otelde konaklamakta olan {len(musteriler)} misafir")

        if not musteriler:
            bos = QLabel("Su an aktif misafir bulunmuyor.")
            bos.setAlignment(Qt.AlignCenter)
            bos.setStyleSheet("color: #3a3a50; font-size: 12pt; padding: 50px; background: transparent;")
            self.scroll_layout.insertWidget(0, bos)
            return

        for m in musteriler:
            kart = MusteriKarti(m)
            kart.duzenle_clicked.connect(self._on_duzenle)
            kart.cikis_clicked.connect(self._on_cikis)
            kart.sil_clicked.connect(self._on_sil)
            self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, kart)

    def _on_duzenle(self, musteri):
        dialog = DuzenleDialog(musteri, self.dm, self)
        if dialog.exec_() == QDialog.Accepted:
            self.guncelleme_gerekli.emit()

    def _on_cikis(self, musteri):
        isim = f"{musteri.get('isim','')} {musteri.get('soyisim','')}"
        reply = show_question(self, "Check-out Onayı", f"{isim} için check-out yapılsın mı?\nOda {musteri.get('oda','')} müsait olacak.")
        if reply:
            if self.dm.cikis_yaptir(musteri["id"], musteri["sheet"]):
                self.guncelleme_gerekli.emit()
            else:
                show_error(self, "Hata", "Check-out işlemi başarısız.")

    def _on_sil(self, musteri):
        isim = f"{musteri.get('isim','')} {musteri.get('soyisim','')}"
        reply = show_question(self, "Kayıt Silme", f"{isim} kaydını kalıcı olarak silmek istiyor musunuz?\n\nBu işlem geri alınamaz!")
        if reply:
            if self.dm.kayit_sil(musteri["id"], musteri["sheet"]):
                self.guncelleme_gerekli.emit()
            else:
                show_error(self, "Hata", "Silme işlemi başarısız.")
