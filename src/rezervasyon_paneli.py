"""
Rezervasyon Paneli - v0.7
Üst: kart listesi, Alt: takvim grid
"""

from datetime import date
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QMessageBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont

from custom_dialog import show_info, show_warning, show_error, show_question

_COMBO_STYLE = """
    QComboBox::drop-down { border: none; width: 28px; }
    QComboBox::down-arrow {
        image: none; border-left: 5px solid transparent;
        border-right: 5px solid transparent; border-top: 6px solid #38bdf8; margin-right: 8px;
    }
    QComboBox QAbstractItemView {
        background-color: #252538; border: 1.5px solid #3a3a50; color: #e2e8f0;
        selection-background-color: #2a2a3e; selection-color: #22c55e; outline: none;
    }
    QComboBox QAbstractItemView::item { background-color: #252538; color: #e2e8f0; padding: 8px 12px; }
    QComboBox QAbstractItemView::item:hover { background-color: #2a2a3e; color: #22c55e; }
"""

GUN_ISIMLERI = {
    0: "Pazartesi", 1: "Salı", 2: "Çarşamba",
    3: "Perşembe", 4: "Cuma", 5: "Cumartesi", 6: "Pazar"
}

AY_ISIMLERI = {
    1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan",
    5: "Mayıs", 6: "Haziran", 7: "Temmuz", 8: "Ağustos",
    9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
}


class RezervasyonKarti(QFrame):
    checkin_clicked = pyqtSignal(dict)
    iptal_clicked = pyqtSignal(dict)
    sil_clicked = pyqtSignal(dict)

    def __init__(self, rezervasyon, parent=None):
        super().__init__(parent)
        self.rezervasyon = rezervasyon
        self.setObjectName("rezervKart")
        self.setFrameShape(QFrame.StyledPanel)
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(14)

        isim = str(self.rezervasyon.get('isim', ''))
        soyisim = str(self.rezervasyon.get('soyisim', ''))
        sirket = str(self.rezervasyon.get('sirket', '') or '')
        oda = str(self.rezervasyon.get('oda', ''))
        giris = str(self.rezervasyon.get('giris', ''))
        cikis = str(self.rezervasyon.get('cikis', '') or '')

        initials = f"{isim[:1]}{soyisim[:1]}".upper() if isim and soyisim else "?"
        avatar = QLabel(initials)
        avatar.setFixedSize(46, 46)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet("QLabel { background-color: #3a3050; color: #a78bfa; border-radius: 23px; font-size: 13pt; font-weight: bold; }")
        layout.addWidget(avatar)

        info = QVBoxLayout()
        info.setSpacing(3)

        isim_lbl = QLabel(f"{isim} {soyisim}")
        isim_lbl.setObjectName("musteriIsim")
        info.addWidget(isim_lbl)

        if sirket:
            sirket_lbl = QLabel(sirket)
            sirket_lbl.setStyleSheet("color: #a78bfa; font-size: 9pt; font-style: italic; background: transparent;")
            info.addWidget(sirket_lbl)

        alt_row = QHBoxLayout()
        alt_row.setSpacing(8)
        oda_lbl = QLabel(f"Oda {oda}")
        oda_lbl.setStyleSheet("font-size: 9pt; color: #a78bfa; font-weight: 600; background-color: rgba(139,92,246,0.15); border: 1px solid #8b5cf6; border-radius: 4px; padding: 1px 7px;")
        alt_row.addWidget(oda_lbl)
        tarih_lbl = QLabel(f"  •  Giriş: {giris}  —  Çıkış: {cikis}")
        tarih_lbl.setObjectName("musteriTarih")
        alt_row.addWidget(tarih_lbl)
        alt_row.addStretch()
        info.addLayout(alt_row)
        layout.addLayout(info)
        layout.addStretch()

        sag = QVBoxLayout()
        sag.setSpacing(8)
        sag.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        badge = QLabel("REZERVE")
        badge.setObjectName("rezervBadge")
        badge.setAlignment(Qt.AlignCenter)
        sag.addWidget(badge)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)

        btn_checkin = QPushButton("Check-in Yap")
        btn_checkin.setObjectName("btnCheckin")
        btn_checkin.clicked.connect(lambda: self.checkin_clicked.emit(self.rezervasyon))
        btn_row.addWidget(btn_checkin)

        btn_iptal = QPushButton("İptal")
        btn_iptal.setObjectName("btnIptal")
        btn_iptal.clicked.connect(lambda: self.iptal_clicked.emit(self.rezervasyon))
        btn_row.addWidget(btn_iptal)

        btn_sil = QPushButton("Sil")
        btn_sil.setObjectName("btnSil")
        btn_sil.setFixedWidth(63)
        btn_sil.setFont(QFont("Segoe UI", 9))
        btn_sil.clicked.connect(lambda: self.sil_clicked.emit(self.rezervasyon))
        btn_row.addWidget(btn_sil)

        sag.addLayout(btn_row)
        layout.addLayout(sag)


class TakvimWidget(QWidget):
    """Ay bazlı rezervasyon takvim görünümü"""

    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.dm = data_manager
        self._bugun = date.today()
        self._yil = self._bugun.year
        self._ay = self._bugun.month
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Navigasyon: ay secimi
        nav = QHBoxLayout()

        self.btn_prev = QPushButton("◀")
        self.btn_prev.setFixedSize(32, 32)
        self.btn_prev.setStyleSheet("QPushButton { background: rgba(100,116,139,0.12); color: #94a3b8; border: 1px solid #475569; border-radius: 6px; font-size: 11pt; } QPushButton:hover { background: rgba(100,116,139,0.22); }")
        self.btn_prev.clicked.connect(self._prev_ay)
        nav.addWidget(self.btn_prev)

        self.ay_lbl = QLabel()
        self.ay_lbl.setAlignment(Qt.AlignCenter)
        self.ay_lbl.setStyleSheet("font-size: 11pt; font-weight: bold; color: #ffffff; background: transparent;")
        self.ay_lbl.setFixedWidth(160)
        nav.addWidget(self.ay_lbl)

        self.btn_next = QPushButton("▶")
        self.btn_next.setFixedSize(32, 32)
        self.btn_next.setStyleSheet("QPushButton { background: rgba(100,116,139,0.12); color: #94a3b8; border: 1px solid #475569; border-radius: 6px; font-size: 11pt; } QPushButton:hover { background: rgba(100,116,139,0.22); }")
        self.btn_next.clicked.connect(self._next_ay)
        nav.addWidget(self.btn_next)
        nav.addStretch()

        layout.addLayout(nav)

        # Tablo
        self.tablo = QTableWidget()
        self.tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tablo.setSelectionMode(QTableWidget.NoSelection)
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setShowGrid(True)
        self.tablo.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e30;
                border: 1px solid #2a2a3e;
                border-radius: 10px;
                gridline-color: #2a2a3e;
                color: #e2e8f0;
            }
            QTableWidget::item {
                padding: 4px 6px;
                border: none;
            }
            QHeaderView::section {
                background-color: #1B3A6B;
                color: #ffffff;
                padding: 6px 4px;
                border: none;
                border-right: 1px solid #2a2a3e;
                font-weight: bold;
                font-size: 9pt;
            }
        """)
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tablo.verticalHeader().setDefaultSectionSize(28)
        layout.addWidget(self.tablo)

        self._guncelle()

    def _prev_ay(self):
        if self._ay == 1:
            self._ay = 12
            self._yil -= 1
        else:
            self._ay -= 1
        self._guncelle()

    def _next_ay(self):
        if self._ay == 12:
            self._ay = 1
            self._yil += 1
        else:
            self._ay += 1
        self._guncelle()

    def _guncelle(self):
        self.ay_lbl.setText(f"{AY_ISIMLERI[self._ay]} {self._yil}")
        veri = self.dm.get_takvim_verisi(self._yil, self._ay)
        odalar = veri['odalar']
        gunler = veri['gunler']

        # Sütunlar: Tarih + Gun + odalar
        self.tablo.setColumnCount(2 + len(odalar))
        headers = ["Tarih", "Gün"] + odalar
        self.tablo.setHorizontalHeaderLabels(headers)

        # Genişlikler
        self.tablo.setColumnWidth(0, 110)
        self.tablo.setColumnWidth(1, 90)
        for i in range(len(odalar)):
            self.tablo.setColumnWidth(2 + i, 130)

        self.tablo.setRowCount(len(gunler))

        for row_idx, gun in enumerate(gunler):
            tarih_str = gun['tarih'].strftime("%d/%m/%Y")
            gun_adi = gun['gun_adi']
            hafta_sonu = gun['hafta_sonu']
            bugun = gun['tarih'] == self._bugun

            # Renk seçimi
            if bugun:
                row_bg = QColor("#1a3a6b")
                text_color = QColor("#93c5fd")
            elif hafta_sonu:
                row_bg = QColor("#2d2d44")
                text_color = QColor("#94a3b8")
            else:
                row_bg = QColor("#1e1e30")
                text_color = QColor("#e2e8f0")

            # Tarih hücresi
            tarih_item = QTableWidgetItem(tarih_str)
            tarih_item.setTextAlignment(Qt.AlignCenter)
            tarih_item.setBackground(row_bg)
            tarih_item.setForeground(text_color)
            if bugun:
                tarih_item.setFont(QFont("Segoe UI", 9, QFont.Bold))
            self.tablo.setItem(row_idx, 0, tarih_item)

            # Gün adı hücresi
            gun_item = QTableWidgetItem(gun_adi)
            gun_item.setTextAlignment(Qt.AlignCenter)
            gun_item.setBackground(row_bg)
            gun_item.setForeground(text_color)
            self.tablo.setItem(row_idx, 1, gun_item)

            # Oda hücreleri
            for col_idx, oda in enumerate(odalar):
                misafir = gun['hucreler'].get(oda)
                if misafir:
                    item = QTableWidgetItem(misafir.strip())
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QColor("#1a3a2a"))
                    item.setForeground(QColor("#4ade80"))
                    item.setFont(QFont("Segoe UI", 9, QFont.Bold))
                else:
                    item = QTableWidgetItem("")
                    item.setBackground(row_bg)
                    item.setForeground(text_color)
                self.tablo.setItem(row_idx, 2 + col_idx, item)

        # Bugünün satırına scroll et
        for row_idx, gun in enumerate(gunler):
            if gun['tarih'] == self._bugun:
                self.tablo.scrollToItem(self.tablo.item(row_idx, 0))
                break

    def refresh(self):
        self._guncelle()


class RezervasyonPaneli(QWidget):
    guncelleme_gerekli = pyqtSignal()

    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.dm = data_manager
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        # Ana scroll area — her şey içinde
        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True)
        main_scroll.setFrameShape(QFrame.NoFrame)
        main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        main_scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")

        main_widget = QWidget()
        main_widget.setStyleSheet("background: transparent;")
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(16)

        # --- ÜST: Kart listesi ---
        kart_card = QFrame()
        kart_card.setObjectName("mainCard")
        kart_layout = QVBoxLayout(kart_card)
        kart_layout.setContentsMargins(24, 20, 24, 20)
        kart_layout.setSpacing(10)

        baslik_row = QHBoxLayout()
        col = QVBoxLayout()
        col.setSpacing(2)
        baslik = QLabel("Rezervasyonlar")
        baslik.setObjectName("panelTitle")
        col.addWidget(baslik)
        self.subtitle_lbl = QLabel("Bekleyen rezervasyonlar")
        self.subtitle_lbl.setObjectName("panelSubtitle")
        col.addWidget(self.subtitle_lbl)
        baslik_row.addLayout(col)
        baslik_row.addStretch()
        kart_layout.addLayout(baslik_row)

        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: #2a2a3e;")
        kart_layout.addWidget(sep)

        self.kart_scroll = QScrollArea()
        self.kart_scroll.setWidgetResizable(True)
        self.kart_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.kart_scroll.setFrameShape(QFrame.NoFrame)
        self.kart_scroll.setFixedHeight(300)
        self.kart_scroll.setStyleSheet("background: transparent;")

        self.kart_widget = QWidget()
        self.kart_widget.setStyleSheet("background: transparent;")
        self.kart_layout = QVBoxLayout(self.kart_widget)
        self.kart_layout.setContentsMargins(0, 0, 0, 0)
        self.kart_layout.setSpacing(6)
        self.kart_layout.addStretch()
        self.kart_scroll.setWidget(self.kart_widget)
        kart_layout.addWidget(self.kart_scroll)

        main_layout.addWidget(kart_card)

        # --- ALT: Takvim ---
        takvim_card = QFrame()
        takvim_card.setObjectName("mainCard")
        takvim_layout = QVBoxLayout(takvim_card)
        takvim_layout.setContentsMargins(24, 20, 24, 20)
        takvim_layout.setSpacing(10)

        takvim_baslik = QLabel("Rezervasyon Takvimi")
        takvim_baslik.setStyleSheet("font-size: 13pt; font-weight: bold; color: #ffffff;")
        takvim_layout.addWidget(takvim_baslik)

        sep2 = QFrame()
        sep2.setFixedHeight(1)
        sep2.setStyleSheet("background-color: #2a2a3e;")
        takvim_layout.addWidget(sep2)

        self.takvim_widget = TakvimWidget(self.dm)
        takvim_layout.addWidget(self.takvim_widget)

        main_layout.addWidget(takvim_card)

        main_scroll.setWidget(main_widget)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(main_scroll)

    def refresh(self):
        # Kartları temizle
        while self.kart_layout.count() > 1:
            item = self.kart_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        rezervasyonlar = self.dm.get_rezervasyonlar()
        self.subtitle_lbl.setText(f"{len(rezervasyonlar)} bekleyen rezervasyon")

        if not rezervasyonlar:
            bos = QLabel("Şu an bekleyen rezervasyon bulunmuyor.")
            bos.setAlignment(Qt.AlignCenter)
            bos.setStyleSheet("color: #3a3a50; font-size: 11pt; padding: 30px; background: transparent;")
            self.kart_layout.insertWidget(0, bos)
        else:
            for r in rezervasyonlar:
                kart = RezervasyonKarti(r)
                kart.checkin_clicked.connect(self._on_checkin)
                kart.iptal_clicked.connect(self._on_iptal)
                kart.sil_clicked.connect(self._on_sil)
                self.kart_layout.insertWidget(self.kart_layout.count() - 1, kart)

        # Takvimi güncelle
        self.takvim_widget.refresh()

    def _on_checkin(self, rezervasyon):
        isim = f"{rezervasyon.get('isim','')} {rezervasyon.get('soyisim','')}"
        if show_question(self, "Check-in Onayı",
                f"{isim} için check-in yapılsın mı?\nRezervasyon aktif kayda dönüştürülecek."):
            if self.dm.rezervasyon_checkin(rezervasyon["id"]):
                show_info(self, "Başarılı", f"{isim} check-in yapıldı!")
                self.guncelleme_gerekli.emit()
            else:
                show_error(self, "Hata", "Check-in işlemi başarısız.")

    def _on_iptal(self, rezervasyon):
        isim = f"{rezervasyon.get('isim','')} {rezervasyon.get('soyisim','')}"
        if show_question(self, "İptal Onayı", f"{isim} rezervasyonu iptal edilsin mi?"):
            if self.dm.rezervasyon_iptal(rezervasyon["id"]):
                self.refresh()
            else:
                show_error(self, "Hata", "İptal işlemi başarısız.")

    def _on_sil(self, rezervasyon):
        isim = f"{rezervasyon.get('isim','')} {rezervasyon.get('soyisim','')}"
        if show_question(self, "Rezervasyon Silme",
                f"{isim} rezervasyonunu kalıcı olarak silmek istiyor musunuz?\n\nBu işlem geri alınamaz!"):
            if self.dm.rezervasyon_sil(rezervasyon["id"]):
                self.refresh()
            else:
                show_error(self, "Hata", "Silme işlemi başarısız.")
