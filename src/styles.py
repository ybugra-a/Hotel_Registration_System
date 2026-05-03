"""
Uygulama stilleri - Modern lacivert tema
"""

MAIN_STYLE = """
/* Genel */
QWidget {
    font-family: 'Segoe UI', Tahoma, Arial;
    font-size: 10pt;
    color: #2c3e50;
}

QMainWindow {
    background-color: #f0f2f5;
}

/* Baslik */
#header {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #1B3A6B, stop:1 #2563EB);
    border-bottom: 2px solid #1a3060;
}

#headerTitle {
    font-size: 15pt;
    font-weight: bold;
    color: white;
    letter-spacing: 0.5px;
}

#headerSubtitle {
    font-size: 9pt;
    color: #93c5fd;
}

/* Tab Widget */
#mainTabs {
    background-color: #f0f2f5;
}

#mainTabs::pane {
    border: none;
    background-color: #f0f2f5;
}

#mainTabs QTabBar::tab {
    background: #dde3ec;
    color: #4a5568;
    padding: 10px 20px;
    border: none;
    border-bottom: 3px solid transparent;
    font-size: 10pt;
    font-weight: 500;
    margin-right: 2px;
}

#mainTabs QTabBar::tab:selected {
    background: white;
    color: #1B3A6B;
    border-bottom: 3px solid #2563EB;
    font-weight: bold;
}

#mainTabs QTabBar::tab:hover:!selected {
    background: #e8edf5;
    color: #1B3A6B;
}

/* Kartlar */
QFrame[frameShape="1"], QFrame[frameShape="6"] {
    background: white;
    border-radius: 10px;
    border: 1px solid #e2e8f0;
}

/* Panel basliklar */
#panelTitle {
    font-size: 12pt;
    font-weight: bold;
    color: #1B3A6B;
    padding: 8px 0 4px 0;
}

#sectionTitle {
    font-size: 10pt;
    font-weight: bold;
    color: #374151;
    margin-top: 8px;
}

/* Form alanlari */
QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox {
    background: white;
    border: 1.5px solid #cbd5e1;
    border-radius: 6px;
    padding: 7px 10px;
    font-size: 10pt;
    color: #1e293b;
    min-height: 22px;
}

QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QDoubleSpinBox:focus {
    border: 1.5px solid #2563EB;
    background: #f8faff;
}

QLineEdit:hover, QComboBox:hover {
    border-color: #94a3b8;
}

QLineEdit[readOnly="true"] {
    background: #f8fafc;
    color: #64748b;
}

/* ComboBox */
QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #64748b;
    margin-right: 5px;
}

QComboBox QAbstractItemView {
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    background: white;
    selection-background-color: #dbeafe;
    selection-color: #1e40af;
    padding: 4px;
}

/* Butonlar */
QPushButton {
    border-radius: 6px;
    padding: 8px 18px;
    font-weight: bold;
    font-size: 10pt;
    border: none;
    min-height: 36px;
}

#btnKaydet {
    background: #16a34a;
    color: white;
}

#btnKaydet:hover {
    background: #15803d;
}

#btnKaydet:pressed {
    background: #166534;
}

#btnTemizle {
    background: #f1f5f9;
    color: #475569;
    border: 1px solid #cbd5e1;
}

#btnTemizle:hover {
    background: #e2e8f0;
}

#btnDuzenle {
    background: #1d4ed8;
    color: white;
    padding: 5px 12px;
    font-size: 9pt;
    min-height: 28px;
}

#btnDuzenle:hover {
    background: #1e40af;
}

#btnCikis {
    background: #dc2626;
    color: white;
    padding: 5px 12px;
    font-size: 9pt;
    min-height: 28px;
}

#btnCikis:hover {
    background: #b91c1c;
}

#btnEkle {
    background: #0891b2;
    color: white;
}

#btnEkle:hover {
    background: #0e7490;
}

#btnSil {
    background: #ef4444;
    color: white;
}

#btnSil:hover {
    background: #dc2626;
}

#btnAra {
    background: #7c3aed;
    color: white;
}

#btnAra:hover {
    background: #6d28d9;
}

#btnYedekle {
    background: #d97706;
    color: white;
}

#btnYedekle:hover {
    background: #b45309;
}

/* Musteri kartlari */
#musteriKart {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    margin: 3px 2px;
    padding: 10px;
}

#musteriKart:hover {
    border-color: #93c5fd;
    background: #f8faff;
}

#musteriIsim {
    font-size: 11pt;
    font-weight: bold;
    color: #1e3a8a;
}

#musteriOda {
    font-size: 10pt;
    color: #374151;
}

#musteriTarih {
    font-size: 9pt;
    color: #64748b;
}

#odemeUyari {
    font-size: 9pt;
    color: #dc2626;
    font-weight: bold;
}

#odemeVar {
    font-size: 9pt;
    color: #16a34a;
}

/* Oda kartlari */
#odaMusait {
    background: #f0fdf4;
    border: 1.5px solid #86efac;
    border-radius: 8px;
    padding: 8px;
}

#odaDolu {
    background: #fff1f2;
    border: 1.5px solid #fca5a5;
    border-radius: 8px;
    padding: 8px;
}

#odaNo {
    font-size: 14pt;
    font-weight: bold;
    color: #1e293b;
}

#odaDurumMusait {
    color: #16a34a;
    font-weight: bold;
}

#odaDurumDolu {
    color: #dc2626;
    font-weight: bold;
}

/* Tablo */
QTableWidget {
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    background: white;
    gridline-color: #f1f5f9;
    selection-background-color: #dbeafe;
    selection-color: #1e40af;
}

QTableWidget::item {
    padding: 6px 10px;
    border-bottom: 1px solid #f1f5f9;
}

QTableWidget::item:selected {
    background: #dbeafe;
    color: #1e40af;
}

QHeaderView::section {
    background: #1B3A6B;
    color: white;
    padding: 8px 10px;
    border: none;
    font-weight: bold;
    font-size: 9pt;
}

QHeaderView::section:first {
    border-radius: 8px 0 0 0;
}

/* Scroll area */
QScrollArea {
    border: none;
    background: transparent;
}

QScrollBar:vertical {
    border: none;
    background: #f1f5f9;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #94a3b8;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #64748b;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

/* Label */
QLabel {
    color: #374151;
}

/* Autocomplete popup */
QListWidget {
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    background: white;
    font-size: 10pt;
}

QListWidget::item {
    padding: 6px 10px;
    border-bottom: 1px solid #f1f5f9;
}

QListWidget::item:selected, QListWidget::item:hover {
    background: #dbeafe;
    color: #1e40af;
}

/* GroupBox */
QGroupBox {
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    margin-top: 12px;
    padding: 8px;
    font-weight: bold;
    color: #374151;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    color: #1B3A6B;
}

/* MessageBox */
QMessageBox {
    background: white;
}

QMessageBox QPushButton {
    min-width: 80px;
    background: #1d4ed8;
    color: white;
}

/* SpinBox */
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    width: 18px;
    border: none;
    background: #f1f5f9;
}

/* DateEdit */
QDateEdit::drop-down {
    border: none;
    width: 24px;
}

/* Filtre alanlari */
#filterPanel {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 8px;
}

/* Bos panel mesaji */
#bosaMessaj {
    color: #94a3b8;
    font-size: 13pt;
}

/* Durum etiketleri */
#etiketAktif {
    background: #dcfce7;
    color: #166534;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 9pt;
    font-weight: bold;
}

#etiketCikis {
    background: #fee2e2;
    color: #991b1b;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 9pt;
    font-weight: bold;
}

/* Yedekleme paneli */
#backupInfo {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: 8px;
    padding: 12px;
}
"""
