"""
Ayarlar Modulu - Oda yonetimi, yedekleme takibi
"""

import os
import shutil
from datetime import date
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QFrame,
    QMessageBox, QFileDialog, QGroupBox, QScrollArea
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

        baslik = QLabel("⚙️  Ayarlar")
        baslik.setObjectName("panelTitle")
        main_layout.addWidget(baslik)

        # Iki sutunlu layout
        cols = QHBoxLayout()
        cols.setSpacing(12)

        # Sol: Oda yonetimi
        oda_card = QFrame()
        oda_card.setFrameShape(QFrame.StyledPanel)
        oda_card.setStyleSheet("QFrame { background: white; border-radius: 12px; border: 1px solid #e2e8f0; }")
        oda_layout = QVBoxLayout(oda_card)
        oda_layout.setContentsMargins(16, 16, 16, 16)
        oda_layout.setSpacing(10)

        oda_baslik = QLabel("🏠  Oda Yönetimi")
        oda_baslik.setStyleSheet("font-size: 12pt; font-weight: bold; color: #1B3A6B;")
        oda_layout.addWidget(oda_baslik)

        # Oda ekleme
        ekle_row = QHBoxLayout()
        self.yeni_oda_edit = QLineEdit()
        self.yeni_oda_edit.setPlaceholderText("Oda numarası (örn: 201)")
        self.yeni_oda_edit.returnPressed.connect(self._ekle_oda)
        ekle_row.addWidget(self.yeni_oda_edit)

        btn_ekle = QPushButton("➕  Ekle")
        btn_ekle.setObjectName("btnEkle")
        btn_ekle.clicked.connect(self._ekle_oda)
        ekle_row.addWidget(btn_ekle)
        oda_layout.addLayout(ekle_row)

        # Oda listesi
        oda_layout.addWidget(QLabel("Mevcut odalar:"))
        self.oda_listesi = QListWidget()
        self.oda_listesi.setAlternatingRowColors(True)
        self.oda_listesi.setStyleSheet("alternate-background-color: #f8fafc;")
        oda_layout.addWidget(self.oda_listesi)

        # Sil butonu
        btn_sil = QPushButton("🗑  Seçili Odayı Sil")
        btn_sil.setObjectName("btnSil")
        btn_sil.clicked.connect(self._sil_oda)
        oda_layout.addWidget(btn_sil)

        cols.addWidget(oda_card)

        # Sag: Yedekleme + Bilgi
        sag = QVBoxLayout()
        sag.setSpacing(12)

        # Yedekleme karti
        yedek_card = QFrame()
        yedek_card.setObjectName("backupInfo")
        yedek_card.setFrameShape(QFrame.StyledPanel)
        yedek_card.setStyleSheet("""
            QFrame#backupInfo {
                background: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)
        yedek_layout = QVBoxLayout(yedek_card)
        yedek_layout.setContentsMargins(16, 16, 16, 16)
        yedek_layout.setSpacing(10)

        yedek_baslik = QLabel("💾  Yedekleme")
        yedek_baslik.setStyleSheet("font-size: 12pt; font-weight: bold; color: #1B3A6B;")
        yedek_layout.addWidget(yedek_baslik)

        self.yedek_tarih_lbl = QLabel()
        self.yedek_tarih_lbl.setStyleSheet("color: #64748b;")
        yedek_layout.addWidget(self.yedek_tarih_lbl)

        aciklama = QLabel(
            "Excel dosyasını güvenli bir konuma kopyalayarak\n"
            "yedekleyin. USB bellek veya bulut depolama önerilir."
        )
        aciklama.setStyleSheet("color: #64748b; font-size: 9pt;")
        aciklama.setWordWrap(True)
        yedek_layout.addWidget(aciklama)

        self.dosya_yolu_lbl = QLabel()
        self.dosya_yolu_lbl.setStyleSheet(
            "background: #f8fafc; border: 1px solid #e2e8f0; "
            "border-radius: 4px; padding: 6px; font-size: 9pt; color: #374151;"
        )
        self.dosya_yolu_lbl.setWordWrap(True)
        yedek_layout.addWidget(self.dosya_yolu_lbl)

        btn_yedekle = QPushButton("💾  Şimdi Yedekle")
        btn_yedekle.setObjectName("btnYedekle")
        btn_yedekle.clicked.connect(self._yedekle)
        yedek_layout.addWidget(btn_yedekle)

        sag.addWidget(yedek_card)

        # Program bilgisi
        bilgi_card = QFrame()
        bilgi_card.setFrameShape(QFrame.StyledPanel)
        bilgi_card.setStyleSheet("QFrame { background: white; border-radius: 12px; border: 1px solid #e2e8f0; }")
        bilgi_layout = QVBoxLayout(bilgi_card)
        bilgi_layout.setContentsMargins(16, 16, 16, 16)

        bilgi_baslik = QLabel("ℹ️  Program Bilgisi")
        bilgi_baslik.setStyleSheet("font-size: 12pt; font-weight: bold; color: #1B3A6B;")
        bilgi_layout.addWidget(bilgi_baslik)

        bilgiler = [
            ("Uygulama", "Otel Kayıt ve Oda Yönetim Sistemi"),
            ("Versiyon", "v1.0"),
            ("Teknoloji", "Python 3 + PyQt5 + openpyxl"),
            ("Platform", "Windows"),
        ]
        for k, v in bilgiler:
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
        # Oda listesini guncelle
        self.oda_listesi.clear()
        odalar = self.dm.get_odalar()
        for oda in sorted(odalar, key=lambda x: int(x["no"]) if x["no"].isdigit() else x["no"]):
            item = QListWidgetItem(f"  Oda {oda['no']}   —   {oda['durum']}")
            if oda["durum"] == "Musait":
                item.setForeground(Qt.darkGreen)
            else:
                item.setForeground(Qt.darkRed)
            item.setData(Qt.UserRole, oda["no"])
            self.oda_listesi.addItem(item)

        # Yedekleme bilgisi
        son_yedek = self.dm.get_backup_date()
        self.yedek_tarih_lbl.setText(f"Son yedekleme: <b>{son_yedek}</b>")
        self.dosya_yolu_lbl.setText(f"Veri dosyası: {self.dm.get_excel_path()}")

    def _ekle_oda(self):
        oda_no = self.yeni_oda_edit.text().strip()
        if not oda_no:
            QMessageBox.warning(self, "Hata", "Oda numarası boş olamaz.")
            return

        success = self.dm.oda_ekle(oda_no)
        if success:
            self.yeni_oda_edit.clear()
            self.refresh()
            self.oda_degisti.emit()
        else:
            QMessageBox.warning(self, "Uyarı", f"Oda {oda_no} zaten mevcut.")

    def _sil_oda(self):
        secili = self.oda_listesi.currentItem()
        if not secili:
            QMessageBox.warning(self, "Uyarı", "Silmek için bir oda seçin.")
            return

        oda_no = secili.data(Qt.UserRole)
        durum = self.dm.get_odalar()
        oda_durum = next((o["durum"] for o in durum if o["no"] == oda_no), None)

        if oda_durum == "Dolu":
            QMessageBox.warning(
                self, "Uyarı",
                f"Oda {oda_no} şu an dolu olduğu için silinemiez.\n"
                "Misafirin çıkışını yapın, ardından tekrar deneyin."
            )
            return

        reply = QMessageBox.question(
            self, "Onay",
            f"Oda {oda_no} listeden silinecek. Emin misiniz?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.dm.oda_sil(oda_no)
            self.refresh()
            self.oda_degisti.emit()

    def _yedekle(self):
        excel_path = self.dm.get_excel_path()
        if not os.path.exists(excel_path):
            QMessageBox.warning(self, "Hata", "Veri dosyası bulunamadı.")
            return

        # Kaydetme dialogu
        hedef, _ = QFileDialog.getSaveFileName(
            self, "Yedek Konumu Seçin",
            f"kayitlar_yedek_{date.today().strftime('%Y%m%d')}.xlsx",
            "Excel Dosyaları (*.xlsx)"
        )
        if not hedef:
            return

        try:
            shutil.copy2(excel_path, hedef)
            self.dm.update_backup_date()
            self.refresh()
            QMessageBox.information(
                self, "Başarılı",
                f"✅ Yedek başarıyla oluşturuldu!\n\nKonum: {hedef}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Yedekleme başarısız:\n{str(e)}")
