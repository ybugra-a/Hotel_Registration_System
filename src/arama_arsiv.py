"""
Arama ve Arsiv Modulu - v0.4
Yeni: Silme islemi, Sirket sutunu
"""

from custom_dialog import show_info, show_warning, show_error, show_question
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
    QFrame, QHeaderView, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor

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
    QComboBox QAbstractItemView::item { background-color: #ffffff; color: #1e293b; padding: 9px 14px; }
    QComboBox QAbstractItemView::item:hover { background-color: #f1f5f9; }
    QComboBox QAbstractItemView::item:selected { background-color: #f1f5f9; }
"""


class AramaArsiv(QWidget):
    guncelleme_gerekli = pyqtSignal()

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

        baslik = QLabel("Arama & Arsiv")
        baslik.setObjectName("panelTitle")
        main_layout.addWidget(baslik)

        # Filtre
        filtre = QFrame()
        filtre.setObjectName("filterPanel")
        filtre_layout = QHBoxLayout(filtre)
        filtre_layout.setContentsMargins(12, 10, 12, 10)
        filtre_layout.setSpacing(10)

        self.arama_edit = QLineEdit()
        self.arama_edit.setPlaceholderText("Isim, soyisim, TC veya sirket ile ara...")
        self.arama_edit.returnPressed.connect(self.ara)
        self.arama_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        filtre_layout.addWidget(self.arama_edit, 3)

        filtre_layout.addWidget(QLabel("Yil:"))
        self.yil_combo = QComboBox()
        self.yil_combo.setFixedWidth(90)
        self.yil_combo.setStyleSheet(_COMBO_STYLE)
        filtre_layout.addWidget(self.yil_combo)

        filtre_layout.addWidget(QLabel("Donem:"))
        self.donem_combo = QComboBox()
        self.donem_combo.setFixedWidth(80)
        self.donem_combo.setStyleSheet(_COMBO_STYLE)
        filtre_layout.addWidget(self.donem_combo)

        filtre_layout.addWidget(QLabel("Durum:"))
        self.durum_combo = QComboBox()
        self.durum_combo.setFixedWidth(120)
        self.durum_combo.setStyleSheet(_COMBO_STYLE)
        filtre_layout.addWidget(self.durum_combo)

        btn_ara = QPushButton("Ara")
        btn_ara.setObjectName("btnAra")
        btn_ara.clicked.connect(self.ara)
        filtre_layout.addWidget(btn_ara)

        btn_sifirla = QPushButton("Sifirla")
        btn_sifirla.setObjectName("btnTemizle")
        btn_sifirla.clicked.connect(self._sifirla)
        filtre_layout.addWidget(btn_sifirla)

        main_layout.addWidget(filtre)

        # Sonuc sayaci + sil butonu
        alt_row = QHBoxLayout()
        self.sonuc_lbl = QLabel("Tum kayitlar gosteriliyor")
        self.sonuc_lbl.setStyleSheet("color: #64748b; font-size: 9pt;")
        alt_row.addWidget(self.sonuc_lbl)
        alt_row.addStretch()

        btn_sil = QPushButton("Secili Kaydi Sil")
        btn_sil.setObjectName("btnSilWide")
        btn_sil.clicked.connect(self._on_sil)
        alt_row.addWidget(btn_sil)
        main_layout.addLayout(alt_row)

        # Tablo - Sirket sutunu eklendi
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(11)
        self.tablo.setHorizontalHeaderLabels([
            "ID", "T.C.", "Ad", "Soyad", "Sirket", "Oda",
            "Giris", "Cikis", "Odeme", "Tutar (TL)", "Durum"
        ])
        self.tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tablo.setSelectionBehavior(QTableWidget.SelectRows)
        self.tablo.setAlternatingRowColors(True)
        header = self.tablo.horizontalHeader()
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.resizeSection(0, 50)
        header.resizeSection(1, 120)
        header.resizeSection(5, 60)
        header.resizeSection(6, 90)
        header.resizeSection(7, 90)
        header.resizeSection(8, 100)
        header.resizeSection(9, 90)
        header.resizeSection(10, 100)
        self.tablo.verticalHeader().setDefaultSectionSize(36)
        main_layout.addWidget(self.tablo)

    def _load_filtreler(self):
        self.yil_combo.addItem("Tümü", "Tümü")
        for y in self.dm.get_yillar():
            self.yil_combo.addItem(y, y)
        self.donem_combo.addItem("Tümü", "Tümü")
        for d in ["Q1","Q2","Q3","Q4"]:
            self.donem_combo.addItem(d, d)
        self.durum_combo.addItem("Tümü", "Tümü")
        self.durum_combo.addItem("Aktif", "Aktif")
        self.durum_combo.addItem("Çıkış Yaptı", "Çıkış Yaptı")

    def ara(self):
        filtre = {
            "arama": self.arama_edit.text().strip(),
            "yil": self.yil_combo.currentData() or "Tümü",
            "donem": self.donem_combo.currentData() or "Tümü",
            "durum": self.durum_combo.currentData() or "Tümü",
        }
        kayitlar = self.dm.get_tum_kayitlar(filtre=filtre)
        self._fill_tablo(kayitlar)
        self.sonuc_lbl.setText(f"{len(kayitlar)} kayit bulundu")

    def _fill_tablo(self, kayitlar):
        self.tablo.setRowCount(0)
        for k in kayitlar:
            row = self.tablo.rowCount()
            self.tablo.insertRow(row)
            degerler = [
                str(k.get("id","")), str(k.get("tc","")),
                str(k.get("isim","")), str(k.get("soyisim","")),
                str(k.get("sirket","") or ""), str(k.get("oda","")),
                str(k.get("giris","")), str(k.get("cikis","") or "—"),
                str(k.get("odeme_yon","")), str(k.get("odeme_tut","") or "—"),
                str(k.get("durum",""))
            ]
            for col, val in enumerate(degerler):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                item.setData(Qt.UserRole, k)
                if col == 10:
                    if k.get("durum") == "Aktif":
                        item.setForeground(QColor("#4ade80"))
                    else:
                        item.setForeground(QColor("#f87171"))
                else:
                    item.setForeground(QColor("#cbd5e1"))
                self.tablo.setItem(row, col, item)

    def _on_sil(self):
        row = self.tablo.currentRow()
        if row < 0:
            show_warning(self, "Uyari", "Lütfen silmek için bir kayıt seçin.")
            return
        k = self.tablo.item(row, 0).data(Qt.UserRole)
        if not k:
            return
        isim = f"{k.get('isim','')} {k.get('soyisim','')}"
        durum = k.get("durum","")
        extra = "\nBu aktif bir kayıt! Oda müsait durumuna geçecek." if durum == "Aktif" else ""
        reply = show_question(self, "Kayıt Silme", f"{isim} kaydını kalıcı olarak silmek istiyor musunuz?{extra}\n\nBu işlem geri alınamaz!")
        if reply:
            if self.dm.kayit_sil(k["id"], k["sheet"]):
                self.ara()
                self.guncelleme_gerekli.emit()
            else:
                show_error(self, "Hata", "Silme işlemi başarısız.")

    def _sifirla(self):
        self.arama_edit.clear()
        self.yil_combo.setCurrentIndex(0)
        self.donem_combo.setCurrentIndex(0)
        self.durum_combo.setCurrentIndex(0)
        self.ara()

    def refresh(self):
        mevcut_yil = self.yil_combo.currentData()
        self.yil_combo.clear()
        self.yil_combo.addItem("Tümü", "Tümü")
        for y in self.dm.get_yillar():
            self.yil_combo.addItem(y, y)
        self.ara()
