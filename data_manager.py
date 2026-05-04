"""
Otel Kayit ve Oda Yonetim Sistemi
Ana uygulama dosyasi
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QTabWidget, QLabel, QMessageBox, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon

# Yerel moduller
from data_manager import DataManager
from kayit_modulu import KayitModulu
from aktif_musteri_paneli import AktifMusteriPaneli
from oda_durumu_paneli import OdaDurumuPaneli
from arama_arsiv import AramaArsiv
from ayarlar import Ayarlar
from styles import MAIN_STYLE


def get_icon_path():
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "otel_icon.png")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "otel_icon.png")


class OtelKayitApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.setWindowTitle("Otel Kayit ve Oda Yonetim Sistemi")
        self.setMinimumSize(1280, 720)

        icon_path = get_icon_path()
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self._setup_ui()
        self._check_backup_warning()

    def _setup_ui(self):
        self.setStyleSheet(MAIN_STYLE)

        # Ana widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Baslik cubugu
        header = self._create_header()
        main_layout.addWidget(header)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setObjectName("mainTabs")
        self.tabs.currentChanged.connect(self._on_tab_changed)
        main_layout.addWidget(self.tabs)

        # Sekmeleri olustur
        self._create_main_tab()
        self._create_odalar_tab()
        self._create_arama_tab()
        self._create_ayarlar_tab()

    def _create_header(self):
        header = QWidget()
        header.setObjectName("header")
        header.setFixedHeight(56)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(8)

        title_col = QVBoxLayout()
        title_col.setSpacing(1)
        title = QLabel("Otel Kayit ve Oda Yonetim Sistemi")
        title.setObjectName("headerTitle")
        subtitle = QLabel("Resepsiyon Yonetim Paneli")
        subtitle.setObjectName("headerSubtitle")
        title_col.addWidget(title)
        title_col.addWidget(subtitle)
        layout.addLayout(title_col)
        layout.addStretch()

        return header

    def _create_main_tab(self):
        """Ana sekme: Kayit Formu + Aktif Musteri Paneli yan yana"""
        main_widget = QWidget()
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Sol: Kayit formu
        self.kayit_modulu = KayitModulu(self.data_manager)
        self.kayit_modulu.kayit_yapildi.connect(self._on_kayit_yapildi)
        layout.addWidget(self.kayit_modulu, 40)

        # Sag: Aktif musteri paneli
        self.aktif_panel = AktifMusteriPaneli(self.data_manager)
        self.aktif_panel.guncelleme_gerekli.connect(self._refresh_all)
        layout.addWidget(self.aktif_panel, 60)

        self.tabs.addTab(main_widget, "📋  Kayit & Aktif Musteriler")

    def _create_odalar_tab(self):
        self.oda_paneli = OdaDurumuPaneli(self.data_manager)
        self.oda_paneli.oda_degisti.connect(self._on_oda_degisti)
        self.tabs.addTab(self.oda_paneli, "🏠  Oda Durumu")

    def _create_arama_tab(self):
        self.arama_modulu = AramaArsiv(self.data_manager)
        self.tabs.addTab(self.arama_modulu, "🔍  Arama & Arsiv")

    def _create_ayarlar_tab(self):
        self.ayarlar_modulu = Ayarlar(self.data_manager)
        self.ayarlar_modulu.oda_degisti.connect(self._refresh_all)
        self.tabs.addTab(self.ayarlar_modulu, "⚙️  Ayarlar")

    def _on_tab_changed(self, index):
        """Sekme degistiginde ilgili paneli guncelle"""
        # Ayarlar sekmesi (index 3) acildiginda oda listesini guncelle
        if index == 3:
            self.ayarlar_modulu.refresh()
        # Oda durumu sekmesi (index 1)
        elif index == 1:
            self.oda_paneli.refresh()

    def _on_kayit_yapildi(self):
        self.aktif_panel.refresh()
        self.oda_paneli.refresh()
        self.kayit_modulu.refresh_oda_listesi()

    def _on_oda_degisti(self):
        self.kayit_modulu.refresh_oda_listesi()
        self.aktif_panel.refresh()

    def _refresh_all(self):
        self.aktif_panel.refresh()
        self.oda_paneli.refresh()
        self.kayit_modulu.refresh_oda_listesi()
        self.arama_modulu.refresh()

    def _check_backup_warning(self):
        """30 gun yedekleme kontrolu"""
        if self.data_manager.check_backup_needed():
            QTimer.singleShot(500, self._show_backup_warning)

    def _show_backup_warning(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Yedekleme Hatirlatmasi")
        msg.setIcon(QMessageBox.Warning)
        msg.setText(
            "⚠️  Son yedeklemenin uzerinden 30 gun gecti.\n\n"
            "Lutfen kayitlar.xlsx dosyasini yedekleyin.\n\n"
            "Dosya konumu:\n"
            f"{self.data_manager.get_excel_path()}"
        )
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet(MAIN_STYLE)
        msg.exec_()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Otel Kayit Sistemi")
    
    font = QFont("Segoe UI", 10)
    icon_path = get_icon_path()
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    app.setFont(font)

    window = OtelKayitApp()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
