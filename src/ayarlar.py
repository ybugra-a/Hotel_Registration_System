"""
Ayarlar Modulu - v0.4
"""

import os
import shutil
from datetime import date
from custom_dialog import show_info, show_warning, show_error, show_question
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QFrame,
    QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt, pyqtSignal


class Ayarlar(QWidget):
    oda_degisti = pyqtSignal()

    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.dm = data_manager
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        baslik = QLabel("Ayarlar")
        baslik.setObjectName("panelTitle")
        main_layout.addWidget(baslik)

        cols = QHBoxLayout()
        cols.setSpacing(12)

        # Sol: Oda yonetimi
        oda_card = QFrame()
        oda_card.setObjectName("mainCard")
        oda_layout = QVBoxLayout(oda_card)
        oda_layout.setContentsMargins(20, 16, 20, 16)
        oda_layout.setSpacing(10)

        oda_baslik = QLabel("Oda Yonetimi")
        oda_baslik.setStyleSheet("font-size: 12pt; font-weight: bold; color: #white;")
        oda_layout.addWidget(oda_baslik)

        ekle_row = QHBoxLayout()
        self.yeni_oda_edit = QLineEdit()
        self.yeni_oda_edit.setPlaceholderText("Oda numarasi (orn: 201)")
        self.yeni_oda_edit.returnPressed.connect(self._ekle_oda)
        ekle_row.addWidget(self.yeni_oda_edit)
        btn_ekle = QPushButton("Ekle")
        btn_ekle.setObjectName("btnEkle")
        btn_ekle.clicked.connect(self._ekle_oda)
        ekle_row.addWidget(btn_ekle)
        oda_layout.addLayout(ekle_row)

        oda_layout.addWidget(QLabel("Mevcut odalar:"))
        self.oda_listesi = QListWidget()
        self.oda_listesi.setAlternatingRowColors(True)
        self.oda_listesi.setStyleSheet("""
            QListWidget {
                background-color: #1e1e30;
                border: 1px solid #3a3a50;
                border-radius: 8px;
                color: #e2e8f0;
                font-size: 10pt;
            }
            QListWidget::item {
                padding: 8px 12px;
                border-bottom: 1px solid #2a2a3e;
                color: #e2e8f0;
            }
            QListWidget::item:alternate {
                background-color: #22223a;
            }
            QListWidget::item:selected {
                background-color: rgba(59,130,246,0.20);
                color: #3b82f6;
            }
            QListWidget::item:hover {
                background-color: #2a2a3e;
            }
        """)
        oda_layout.addWidget(self.oda_listesi)

        btn_sil = QPushButton("Secili Odayi Sil")
        btn_sil.setObjectName("btnSil")
        btn_sil.clicked.connect(self._sil_oda)
        oda_layout.addWidget(btn_sil)
        cols.addWidget(oda_card)

        # Sag: Yedekleme + Bilgi
        sag = QVBoxLayout()
        sag.setSpacing(12)

        yedek_card = QFrame()
        yedek_card.setObjectName("mainCard")
        yedek_layout = QVBoxLayout(yedek_card)
        yedek_layout.setContentsMargins(20, 16, 20, 16)
        yedek_layout.setSpacing(10)

        yedek_baslik = QLabel("Yedekleme")
        yedek_baslik.setStyleSheet("font-size: 12pt; font-weight: bold; color: #ffffff;")
        yedek_layout.addWidget(yedek_baslik)

        self.yedek_tarih_lbl = QLabel()
        self.yedek_tarih_lbl.setStyleSheet("color: #64748b;")
        yedek_layout.addWidget(self.yedek_tarih_lbl)

        aciklama = QLabel("Excel dosyasini USB bellek veya bulut depolamaya yedekleyin.")
        aciklama.setStyleSheet("color: #64748b; font-size: 9pt;")
        aciklama.setWordWrap(True)
        yedek_layout.addWidget(aciklama)

        self.dosya_yolu_lbl = QLabel()
        self.dosya_yolu_lbl.setStyleSheet(
            "background: #1e1e30; border: 1px solid #3a3a50; border-radius: 6px; "
            "padding: 6px; font-size: 9pt; color: #94a3b8;"
        )
        self.dosya_yolu_lbl.setWordWrap(True)
        yedek_layout.addWidget(self.dosya_yolu_lbl)

        btn_yedekle = QPushButton("Simdi Yedekle")
        btn_yedekle.setObjectName("btnYedekle")
        btn_yedekle.clicked.connect(self._yedekle)
        yedek_layout.addWidget(btn_yedekle)
        sag.addWidget(yedek_card)

        bilgi_card = QFrame()
        bilgi_card.setObjectName("mainCard")
        bilgi_layout = QVBoxLayout(bilgi_card)
        bilgi_layout.setContentsMargins(20, 16, 20, 16)

        bilgi_baslik = QLabel("Program Bilgisi")
        bilgi_baslik.setStyleSheet("font-size: 12pt; font-weight: bold; color: #white;")
        bilgi_layout.addWidget(bilgi_baslik)

        for k, v in [("Uygulama","Otel Kayit ve Oda Yonetim Sistemi"),
                     ("Versiyon","v0.6.1")]:
            row = QHBoxLayout()
            row.addWidget(QLabel(f"<b>{k}:</b>"))
            row.addWidget(QLabel(v))
            row.addStretch()
            bilgi_layout.addLayout(row)

        sag.addWidget(bilgi_card)
        sag.addStretch()
        cols.addLayout(sag)
        main_layout.addLayout(cols)

    def refresh(self):
        self.oda_listesi.clear()
        for oda in sorted(self.dm.get_odalar(),
                          key=lambda x: int(x["no"]) if x["no"].isdigit() else x["no"]):
            item = QListWidgetItem(f"  Oda {oda['no']}   —   {oda['durum']}")
            item.setForeground(Qt.darkGreen if oda["durum"] == "Musait" else Qt.darkRed)
            item.setData(Qt.UserRole, oda["no"])
            self.oda_listesi.addItem(item)
        self.yedek_tarih_lbl.setText(f"Son yedekleme: <b>{self.dm.get_backup_date()}</b>")
        self.dosya_yolu_lbl.setText(f"Veri dosyasi: {self.dm.get_excel_path()}")

    def _ekle_oda(self):
        oda_no = self.yeni_oda_edit.text().strip()
        if not oda_no:
            show_warning(self, "Hata", "Oda numarası boş olamaz.")
            return
        if self.dm.oda_ekle(oda_no):
            self.yeni_oda_edit.clear()
            self.refresh()
            self.oda_degisti.emit()
        else:
            show_warning(self, "Uyarı", f"Oda {oda_no} zaten mevcut.")

    def _sil_oda(self):
        secili = self.oda_listesi.currentItem()
        if not secili:
            show_warning(self, "Uyari", "Silmek için bir oda seçin.")
            return
        oda_no = secili.data(Qt.UserRole)
        durum = next((o["durum"] for o in self.dm.get_odalar() if o["no"] == oda_no), None)
        if durum == "Dolu":
            show_warning(self, "Uyarı", f"Oda {oda_no} şu an dolu olduğu için silinemez.\nÖnce misafiri çıkış yaptırınız.")
            return
        reply = show_question(self, "Onay", f"Oda {oda_no} listeden silinecek. Emin misiniz?")
        if reply:
            self.dm.oda_sil(oda_no)
            self.refresh()
            self.oda_degisti.emit()

    def _yedekle(self):
        excel_path = self.dm.get_excel_path()
        if not os.path.exists(excel_path):
            show_warning(self, "Hata", "Veri dosyası bulunamadı.")
            return
        hedef, _ = QFileDialog.getSaveFileName(
            self, "Yedek Konumu Secin",
            f"kayitlar_yedek_{date.today().strftime('%Y%m%d')}.xlsx",
            "Excel Dosyalari (*.xlsx)")
        if not hedef:
            return
        try:
            shutil.copy2(excel_path, hedef)
            self.dm.update_backup_date()
            self.refresh()
            show_info(self, "Başarılı", f"Yedek oluşturuldu!\nKonum: {hedef}")
        except Exception as e:
            show_error(self, "Hata", f"Yedekleme başarısız:\n{str(e)}")
