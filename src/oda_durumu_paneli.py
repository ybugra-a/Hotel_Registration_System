"""
Oda Durumu Paneli - Tum odalarin musait/dolu listesi
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QFrame, QScrollArea, QPushButton
)
from PyQt5.QtCore import Qt, pyqtSignal


class OdaKarti(QFrame):
    def __init__(self, oda_no, durum, parent=None):
        super().__init__(parent)
        self.oda_no = oda_no
        self.durum = durum
        self._setup_ui()

    def _setup_ui(self):
        if self.durum == "Musait":
            self.setObjectName("odaMusait")
        else:
            self.setObjectName("odaDolu")

        self.setFixedHeight(80)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignCenter)

        no_lbl = QLabel(f"🏠  {self.oda_no}")
        no_lbl.setObjectName("odaNo")
        no_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(no_lbl)

        if self.durum == "Musait":
            durum_lbl = QLabel("✅  Müsait")
            durum_lbl.setObjectName("odaDurumMusait")
        else:
            durum_lbl = QLabel("❌  Dolu")
            durum_lbl.setObjectName("odaDurumDolu")

        durum_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(durum_lbl)


class OdaDurumuPaneli(QWidget):
    oda_degisti = pyqtSignal()

    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.dm = data_manager
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)

        # Baslik
        baslik_row = QHBoxLayout()
        baslik = QLabel("🏠  Oda Durumu Paneli")
        baslik.setObjectName("panelTitle")
        baslik_row.addWidget(baslik)
        baslik_row.addStretch()

        # Istatistik
        self.musait_lbl = QLabel()
        self.musait_lbl.setStyleSheet("color: #16a34a; font-weight: bold;")
        self.dolu_lbl = QLabel()
        self.dolu_lbl.setStyleSheet("color: #dc2626; font-weight: bold;")
        baslik_row.addWidget(self.musait_lbl)
        baslik_row.addSpacing(16)
        baslik_row.addWidget(self.dolu_lbl)
        main_layout.addLayout(baslik_row)

        # Odalar grid
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("QFrame { background: white; border-radius: 12px; border: 1px solid #e2e8f0; }")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(10)
        scroll.setWidget(self.grid_widget)
        card_layout.addWidget(scroll)

        main_layout.addWidget(card)

    def refresh(self):
        # Grid'i temizle
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        odalar = self.dm.get_odalar()
        musait = sum(1 for o in odalar if o["durum"] == "Musait")
        dolu = len(odalar) - musait

        self.musait_lbl.setText(f"✅  {musait} Müsait")
        self.dolu_lbl.setText(f"❌  {dolu} Dolu")

        # Odalari grid'e yerlestir (5 sutun)
        cols = 5
        for i, oda in enumerate(sorted(odalar, key=lambda x: int(x["no"]) if x["no"].isdigit() else x["no"])):
            row = i // cols
            col = i % cols
            kart = OdaKarti(oda["no"], oda["durum"])
            self.grid_layout.addWidget(kart, row, col)

        # Bos hucreleri doldur
        if odalar:
            remaining = cols - (len(odalar) % cols)
            if remaining < cols:
                last_row = (len(odalar) - 1) // cols
                for c in range(cols - remaining, cols):
                    spacer = QWidget()
                    self.grid_layout.addWidget(spacer, last_row, c)
