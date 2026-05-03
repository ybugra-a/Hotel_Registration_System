"""
Arama ve Arsiv Modulu - Tum gecmis kayitlarda arama
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
    QFrame, QHeaderView, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor


class AramaArsiv(QWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.dm = data_manager
        self._setup_ui()
        self._load_filtreler()
        self.ara()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)

        # Baslik
        baslik = QLabel("🔍  Arama & Arşiv")
        baslik.setObjectName("panelTitle")
        main_layout.addWidget(baslik)

        # Filtre paneli
        filtre_card = QFrame()
        filtre_card.setObjectName("filterPanel")
        filtre_layout = QHBoxLayout(filtre_card)
        filtre_layout.setContentsMargins(12, 10, 12, 10)
        filtre_layout.setSpacing(10)

        # Arama kutusu
        self.arama_edit = QLineEdit()
        self.arama_edit.setPlaceholderText("🔍  İsim, soyisim veya T.C. ile arama...")
        self.arama_edit.returnPressed.connect(self.ara)
        self.arama_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        filtre_layout.addWidget(self.arama_edit, 3)

        # Yil filtresi
        filtre_layout.addWidget(QLabel("Yıl:"))
        self.yil_combo = QComboBox()
        self.yil_combo.setFixedWidth(90)
        filtre_layout.addWidget(self.yil_combo)

        # Donem filtresi
        filtre_layout.addWidget(QLabel("Dönem:"))
        self.donem_combo = QComboBox()
        self.donem_combo.setFixedWidth(80)
        filtre_layout.addWidget(self.donem_combo)

        # Durum filtresi
        filtre_layout.addWidget(QLabel("Durum:"))
        self.durum_combo = QComboBox()
        self.durum_combo.setFixedWidth(110)
        filtre_layout.addWidget(self.durum_combo)

        # Arama butonu
        btn_ara = QPushButton("🔍  Ara")
        btn_ara.setObjectName("btnAra")
        btn_ara.clicked.connect(self.ara)
        filtre_layout.addWidget(btn_ara)

        # Sifirla butonu
        btn_sifirla = QPushButton("↺  Sıfırla")
        btn_sifirla.setObjectName("btnTemizle")
        btn_sifirla.clicked.connect(self._sifirla)
        filtre_layout.addWidget(btn_sifirla)

        main_layout.addWidget(filtre_card)

        # Sonuc sayaci
        self.sonuc_lbl = QLabel("Tüm kayıtlar gösteriliyor")
        self.sonuc_lbl.setStyleSheet("color: #64748b; font-size: 9pt;")
        main_layout.addWidget(self.sonuc_lbl)

        # Tablo
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(10)
        self.tablo.setHorizontalHeaderLabels([
            "ID", "T.C.", "İsim", "Soyisim", "Oda",
            "Giriş", "Çıkış", "Ödeme Yöntemi", "Tutar (₺)", "Durum"
        ])
        self.tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tablo.setSelectionBehavior(QTableWidget.SelectRows)
        self.tablo.setAlternatingRowColors(True)
        self.tablo.setStyleSheet("""
            QTableWidget { alternate-background-color: #f8fafc; }
        """)
        header = self.tablo.horizontalHeader()
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.resizeSection(0, 60)
        header.resizeSection(1, 130)
        header.resizeSection(4, 70)
        header.resizeSection(5, 100)
        header.resizeSection(6, 100)
        header.resizeSection(7, 120)
        header.resizeSection(8, 90)
        header.resizeSection(9, 100)
        self.tablo.verticalHeader().setDefaultSectionSize(36)
        main_layout.addWidget(self.tablo)

    def _load_filtreler(self):
        self.yil_combo.addItem("Tümü", "Tumu")
        for yil in self.dm.get_yillar():
            self.yil_combo.addItem(yil, yil)

        self.donem_combo.addItem("Tümü", "Tumu")
        for donem in ["Q1", "Q2", "Q3", "Q4"]:
            self.donem_combo.addItem(donem, donem)

        self.durum_combo.addItem("Tümü", "Tumu")
        self.durum_combo.addItem("Aktif", "Aktif")
        self.durum_combo.addItem("Çıkış Yaptı", "Cikis Yapti")

    def ara(self):
        filtre = {
            "arama": self.arama_edit.text().strip(),
            "yil": self.yil_combo.currentData() or "Tumu",
            "donem": self.donem_combo.currentData() or "Tumu",
            "durum": self.durum_combo.currentData() or "Tumu",
        }
        kayitlar = self.dm.get_tum_kayitlar(filtre=filtre)
        self._fill_tablo(kayitlar)
        self.sonuc_lbl.setText(f"{len(kayitlar)} kayıt bulundu")

    def _fill_tablo(self, kayitlar):
        self.tablo.setRowCount(0)
        for k in kayitlar:
            row = self.tablo.rowCount()
            self.tablo.insertRow(row)

            sutunlar = [
                str(k.get("id", "")),
                str(k.get("tc", "")),
                str(k.get("isim", "")),
                str(k.get("soyisim", "")),
                str(k.get("oda", "")),
                str(k.get("giris", "")),
                str(k.get("cikis", "") or "—"),
                str(k.get("odeme_yon", "")),
                str(k.get("odeme_tut", "") or "—"),
                str(k.get("durum", "")),
            ]

            for col, val in enumerate(sutunlar):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)

                # Durum renkler
                durum = k.get("durum", "")
                if col == 9:
                    if durum == "Aktif":
                        item.setForeground(QColor("#16a34a"))
                    else:
                        item.setForeground(QColor("#dc2626"))

                # Odeme uyarisi
                if col == 8 and (not k.get("odeme_tut") or str(k.get("odeme_tut", "")).strip() in ["", "0", "0.0"]):
                    item.setForeground(QColor("#dc2626"))

                self.tablo.setItem(row, col, item)

    def _sifirla(self):
        self.arama_edit.clear()
        self.yil_combo.setCurrentIndex(0)
        self.donem_combo.setCurrentIndex(0)
        self.durum_combo.setCurrentIndex(0)
        self.ara()

    def refresh(self):
        # Yil listesini guncelle
        mevcut_yil = self.yil_combo.currentData()
        self.yil_combo.clear()
        self.yil_combo.addItem("Tümü", "Tumu")
        for yil in self.dm.get_yillar():
            self.yil_combo.addItem(yil, yil)
        self.ara()
