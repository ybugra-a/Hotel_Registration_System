"""
Blacklist Modulu - v0.4
"""

from custom_dialog import show_info, show_warning, show_error, show_question
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor


class BlacklistModulu(QWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.dm = data_manager
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        baslik = QLabel("Kara Liste")
        baslik.setObjectName("panelTitle")
        main_layout.addWidget(baslik)

        # Ekleme formu
        form_card = QFrame()
        form_card.setObjectName("mainCard")
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(24, 20, 24, 20)
        form_layout.setSpacing(10)

        form_title = QLabel("Kara Listeye Ekle")
        form_title.setStyleSheet("font-size: 12pt; font-weight: bold; color: #white;")
        form_layout.addWidget(form_title)

        def lbl(t):
            l = QLabel(t)
            l.setObjectName("formLabel")
            return l

        # TC | Ad | Soyad yan yana
        row1 = QHBoxLayout(); row1.setSpacing(10)

        c1 = QVBoxLayout(); c1.setSpacing(4)
        c1.addWidget(lbl("T.C. KIMLIK NO *"))
        self.tc_edit = QLineEdit()
        self.tc_edit.setPlaceholderText("11 haneli TC")
        self.tc_edit.setMaxLength(11)
        c1.addWidget(self.tc_edit)
        row1.addLayout(c1)

        c2 = QVBoxLayout(); c2.setSpacing(4)
        c2.addWidget(lbl("AD *"))
        self.isim_edit = QLineEdit()
        self.isim_edit.setPlaceholderText("Ad")
        c2.addWidget(self.isim_edit)
        row1.addLayout(c2)

        c3 = QVBoxLayout(); c3.setSpacing(4)
        c3.addWidget(lbl("SOYAD *"))
        self.soyisim_edit = QLineEdit()
        self.soyisim_edit.setPlaceholderText("Soyad")
        c3.addWidget(self.soyisim_edit)
        row1.addLayout(c3)
        form_layout.addLayout(row1)

        # Sirket | Sebep yan yana
        row2 = QHBoxLayout(); row2.setSpacing(10)

        c4 = QVBoxLayout(); c4.setSpacing(4)
        c4.addWidget(lbl("SIRKET ISMI"))
        self.sirket_edit = QLineEdit()
        self.sirket_edit.setPlaceholderText("Opsiyonel")
        c4.addWidget(self.sirket_edit)
        row2.addLayout(c4)

        c5 = QVBoxLayout(); c5.setSpacing(4)
        c5.addWidget(lbl("SEBEP"))
        self.sebep_edit = QLineEdit()
        self.sebep_edit.setPlaceholderText("Kara listeye eklenme sebebi (opsiyonel)")
        c5.addWidget(self.sebep_edit)
        row2.addLayout(c5, 2)
        form_layout.addLayout(row2)

        # Buton
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.btn_ekle = QPushButton("Kara Listeye Ekle")
        self.btn_ekle.setObjectName("btnBlacklist")
        self.btn_ekle.clicked.connect(self._on_ekle)
        btn_row.addWidget(self.btn_ekle)
        form_layout.addLayout(btn_row)

        main_layout.addWidget(form_card)

        # Liste
        liste_card = QFrame()
        liste_card.setObjectName("mainCard")
        liste_layout = QVBoxLayout(liste_card)
        liste_layout.setContentsMargins(24, 20, 24, 20)
        liste_layout.setSpacing(10)

        # Arama + baslik
        arama_row = QHBoxLayout()
        liste_baslik = QLabel("Kara Liste Kayitlari")
        liste_baslik.setStyleSheet("font-size: 12pt; font-weight: bold; color: #white;")
        arama_row.addWidget(liste_baslik)
        arama_row.addStretch()

        self.arama_edit = QLineEdit()
        self.arama_edit.setPlaceholderText("Ara...")
        self.arama_edit.setFixedWidth(200)
        self.arama_edit.textChanged.connect(self.refresh)
        arama_row.addWidget(self.arama_edit)
        liste_layout.addLayout(arama_row)

        self.tablo = QTableWidget()
        self.tablo.setColumnCount(7)
        self.tablo.setHorizontalHeaderLabels(["ID","T.C.","Ad","Soyad","Sirket","Sebep","Eklenme"])
        self.tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tablo.setSelectionBehavior(QTableWidget.SelectRows)
        self.tablo.setAlternatingRowColors(True)
        header = self.tablo.horizontalHeader()
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        header.resizeSection(0, 50)
        header.resizeSection(1, 120)
        header.resizeSection(2, 100)
        header.resizeSection(3, 100)
        header.resizeSection(4, 120)
        header.resizeSection(6, 100)
        self.tablo.verticalHeader().setDefaultSectionSize(36)
        liste_layout.addWidget(self.tablo)

        # Sil butonu
        sil_row = QHBoxLayout()
        sil_row.addStretch()
        btn_sil = QPushButton("Secili Kaydi Sil")
        btn_sil.setObjectName("btnSil")
        btn_sil.clicked.connect(self._on_sil)
        sil_row.addWidget(btn_sil)
        liste_layout.addLayout(sil_row)

        main_layout.addWidget(liste_card)

    def _on_ekle(self):
        tc = self.tc_edit.text().strip()
        isim = self.isim_edit.text().strip().upper()
        soyisim = self.soyisim_edit.text().strip().upper()
        sirket = self.sirket_edit.text().strip()
        sebep = self.sebep_edit.text().strip()

        if not tc or not tc.isdigit() or len(tc) != 11:
            show_warning(self, "Hata", "T.C. Kimlik No 11 haneli sayı olmalıdır.")
            return
        if not isim or not soyisim:
            show_warning(self, "Hata", "Ad ve Soyad zorunludur.")
            return

        # Zaten listede mi?
        if self.dm.blacklist_kontrol(tc):
            show_warning(self, "Uyari", "Bu T.C. numarası zaten Kara Liste'de!")
            return

        self.dm.blacklist_ekle(tc, isim, soyisim, sirket, sebep)
        show_info(self, "Başarılı", f"{isim} {soyisim} Kara Liste'ye eklendi.")
        self.tc_edit.clear()
        self.isim_edit.clear()
        self.soyisim_edit.clear()
        self.sirket_edit.clear()
        self.sebep_edit.clear()
        self.refresh()

    def _on_sil(self):
        row = self.tablo.currentRow()
        if row < 0:
            show_warning(self, "Uyari", "Lütfen silmek için bir kayıt seçin.")
            return
        bl_id = self.tablo.item(row, 0).text()
        isim = f"{self.tablo.item(row, 2).text()} {self.tablo.item(row, 3).text()}"
        reply = show_question(self, "Silme Onayı", f"{isim} Kara Liste'den kalıcı olarak silinsin mi?")
        if reply:
            if self.dm.blacklist_sil(bl_id):
                self.refresh()
            else:
                show_error(self, "Hata", "Silme başarısız.")

    def refresh(self):
        arama = self.arama_edit.text().strip() if hasattr(self, 'arama_edit') else ""
        kayitlar = self.dm.get_blacklist(arama)
        self.tablo.setRowCount(0)
        for k in kayitlar:
            row = self.tablo.rowCount()
            self.tablo.insertRow(row)
            degerler = [str(k.get("id","")), str(k.get("tc","")),
                        str(k.get("isim","")), str(k.get("soyisim","")),
                        str(k.get("sirket","") or ""), str(k.get("sebep","") or ""),
                        str(k.get("tarih",""))]
            for col, val in enumerate(degerler):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                item.setForeground(QColor("#e2e8f0"))
                self.tablo.setItem(row, col, item)
