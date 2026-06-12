"""
Oda Durumu Paneli - v0.4
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QScrollArea, QGridLayout
)
from PyQt5.QtCore import Qt, pyqtSignal


class OdaKarti(QFrame):
    def __init__(self, oda_no, durum, parent=None):
        super().__init__(parent)
        self.setObjectName("odaMusait" if durum == "Musait" else "odaDolu")
        self.setFixedHeight(80)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignCenter)

        no_lbl = QLabel(f"{oda_no}")
        no_lbl.setObjectName("odaNo")
        no_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(no_lbl)

        durum_lbl = QLabel("Musait" if durum == "Musait" else "Dolu")
        durum_lbl.setObjectName("odaDurumMusait" if durum == "Musait" else "odaDurumDolu")
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

        baslik_row = QHBoxLayout()
        baslik = QLabel("Oda Durumu Paneli")
        baslik.setObjectName("panelTitle")
        baslik_row.addWidget(baslik)
        baslik_row.addStretch()
        self.musait_lbl = QLabel()
        self.musait_lbl.setStyleSheet("color: #16a34a; font-weight: bold;")
        self.dolu_lbl = QLabel()
        self.dolu_lbl.setStyleSheet("color: #ef4444; font-weight: bold;")
        baslik_row.addWidget(self.musait_lbl)
        baslik_row.addSpacing(16)
        baslik_row.addWidget(self.dolu_lbl)
        main_layout.addLayout(baslik_row)

        card = QFrame()
        card.setObjectName("mainCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.grid_widget = QWidget()
        self.grid_widget.setStyleSheet("background: transparent;")
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(10)
        scroll.setWidget(self.grid_widget)
        card_layout.addWidget(scroll)
        main_layout.addWidget(card)

    def refresh(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        odalar = self.dm.get_odalar()
        musait = sum(1 for o in odalar if o["durum"] == "Musait")
        dolu = len(odalar) - musait
        self.musait_lbl.setText(f"Musait: {musait}")
        self.dolu_lbl.setText(f"Dolu: {dolu}")

        cols = 5
        for i, oda in enumerate(sorted(odalar, key=lambda x: int(x["no"]) if x["no"].isdigit() else x["no"])):
            self.grid_layout.addWidget(OdaKarti(oda["no"], oda["durum"]), i // cols, i % cols)
