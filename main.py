"""
Uygulama stilleri - Koyu tema (Stitch UI referansi)
"""

MAIN_STYLE = """
/* === GENEL === */
QWidget {
    font-family: 'Segoe UI', Tahoma, Arial;
    font-size: 10pt;
    color: #e2e8f0;
    background-color: #0f1923;
}

QMainWindow {
    background-color: #0f1923;
}

/* === HEADER === */
#header {
    background-color: #0d1520;
    border-bottom: 1px solid #1e2d3d;
}

#headerTitle {
    font-size: 14pt;
    font-weight: bold;
    color: #f1f5f9;
}

#headerSubtitle {
    font-size: 9pt;
    color: #64748b;
}

/* === TAB WIDGET === */
#mainTabs {
    background-color: #0f1923;
}

#mainTabs::pane {
    border: none;
    background-color: #0f1923;
}

#mainTabs QTabBar::tab {
    background: transparent;
    color: #64748b;
    padding: 12px 24px;
    border: none;
    border-bottom: 3px solid transparent;
    font-size: 10pt;
    font-weight: 500;
    margin-right: 4px;
}

#mainTabs QTabBar::tab:selected {
    color: #f1f5f9;
    border-bottom: 3px solid #22c55e;
    font-weight: bold;
}

#mainTabs QTabBar::tab:hover:!selected {
    color: #94a3b8;
    border-bottom: 3px solid #2a3a4a;
}

/* === PANEL BASLIK === */
#panelTitle {
    font-size: 13pt;
    font-weight: bold;
    color: #f1f5f9;
    padding: 4px 0;
}

/* === KARTLAR === */
QFrame[frameShape="1"], QFrame[frameShape="6"] {
    background-color: #1a2635;
    border-radius: 12px;
    border: 1px solid #1e2d3d;
}

/* === FORM ALANLARI === */
QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox {
    background-color: #1a2635;
    border: 1.5px solid #2a3a4a;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 10pt;
    color: #e2e8f0;
    min-height: 22px;
}

QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QDoubleSpinBox:focus {
    border: 1.5px solid #22c55e;
    background-color: #1e2d3d;
}

QLineEdit:hover, QComboBox:hover {
    border-color: #3a4a5a;
}

QLineEdit::placeholder {
    color: #3a4a5a;
}

QLineEdit[readOnly="true"] {
    background-color: #131f2e;
    color: #475569;
}

/* === COMBOBOX === */
QComboBox::drop-down {
    border: none;
    width: 28px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #64748b;
    margin-right: 8px;
}

QComboBox QAbstractItemView {
    border: 1px solid #2a3a4a;
    border-radius: 8px;
    background-color: #1a2635;
    selection-background-color: #22c55e22;
    selection-color: #22c55e;
    padding: 4px;
    outline: none;
}

QComboBox QAbstractItemView::item {
    padding: 8px 12px;
    color: #e2e8f0;
}

/* === BUTONLAR === */
QPushButton {
    border-radius: 8px;
    padding: 9px 20px;
    font-weight: bold;
    font-size: 10pt;
    border: none;
    min-height: 36px;
}

#btnKaydet {
    background-color: #22c55e;
    color: #0f1923;
}

#btnKaydet:hover {
    background-color: #16a34a;
}

#btnKaydet:pressed {
    background-color: #15803d;
}

#btnTemizle {
    background-color: #1e2d3d;
    color: #94a3b8;
    border: 1px solid #2a3a4a;
}

#btnTemizle:hover {
    background-color: #2a3a4a;
    color: #e2e8f0;
}

#btnDuzenle {
    background-color: #1e2d3d;
    color: #94a3b8;
    border: 1px solid #2a3a4a;
    padding: 6px 14px;
    font-size: 9pt;
    min-height: 30px;
}

#btnDuzenle:hover {
    background-color: #2a3a4a;
    color: #e2e8f0;
}

#btnCikis {
    background-color: #1e2d3d;
    color: #94a3b8;
    border: 1px solid #2a3a4a;
    padding: 6px 14px;
    font-size: 9pt;
    min-height: 30px;
}

#btnCikis:hover {
    background-color: #dc262622;
    color: #f87171;
    border-color: #dc2626;
}

#btnEkle {
    background-color: #22c55e;
    color: #0f1923;
}

#btnEkle:hover {
    background-color: #16a34a;
}

#btnSil {
    background-color: #1e2d3d;
    color: #f87171;
    border: 1px solid #dc2626;
}

#btnSil:hover {
    background-color: #dc262622;
}

#btnAra {
    background-color: #22c55e;
    color: #0f1923;
}

#btnAra:hover {
    background-color: #16a34a;
}

#btnYedekle {
    background-color: #1e2d3d;
    color: #fbbf24;
    border: 1px solid #d97706;
}

#btnYedekle:hover {
    background-color: #d9770622;
}

/* === MISAFIR KARTLARI === */
#musteriKart {
    background-color: #1e2d3d;
    border: 1px solid #2a3a4a;
    border-radius: 12px;
    margin: 3px 2px;
    padding: 12px;
}

#musteriKart:hover {
    border-color: #3a4a5a;
    background-color: #22334a;
}

#musteriIsim {
    font-size: 11pt;
    font-weight: bold;
    color: #f1f5f9;
}

#musteriOda {
    font-size: 10pt;
    color: #94a3b8;
}

#musteriTarih {
    font-size: 9pt;
    color: #64748b;
}

#odemeUyari {
    font-size: 9pt;
    color: #fb923c;
    font-weight: bold;
    background-color: #fb923c22;
    border-radius: 4px;
    padding: 2px 8px;
}

#odemeVar {
    font-size: 9pt;
    color: #22c55e;
    font-weight: bold;
    background-color: #22c55e22;
    border-radius: 4px;
    padding: 2px 8px;
}

/* === ODA KARTLARI === */
#odaMusait {
    background-color: #22c55e11;
    border: 1.5px solid #22c55e44;
    border-radius: 10px;
    padding: 8px;
}

#odaDolu {
    background-color: #ef444411;
    border: 1.5px solid #ef444444;
    border-radius: 10px;
    padding: 8px;
}

#odaNo {
    font-size: 14pt;
    font-weight: bold;
    color: #f1f5f9;
}

#odaDurumMusait {
    color: #22c55e;
    font-weight: bold;
}

#odaDurumDolu {
    color: #ef4444;
    font-weight: bold;
}

/* === TABLO === */
QTableWidget {
    border: 1px solid #1e2d3d;
    border-radius: 10px;
    background-color: #1a2635;
    gridline-color: #1e2d3d;
    selection-background-color: #22c55e22;
    selection-color: #22c55e;
    alternate-background-color: #1e2d3d;
}

QTableWidget::item {
    padding: 8px 10px;
    border-bottom: 1px solid #1e2d3d;
    color: #e2e8f0;
}

QTableWidget::item:selected {
    background-color: #22c55e22;
    color: #22c55e;
}

QHeaderView::section {
    background-color: #131f2e;
    color: #64748b;
    padding: 10px;
    border: none;
    border-bottom: 1px solid #1e2d3d;
    font-weight: bold;
    font-size: 9pt;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* === SCROLL === */
QScrollArea {
    border: none;
    background: transparent;
}

QScrollBar:vertical {
    border: none;
    background: #131f2e;
    width: 6px;
    border-radius: 3px;
}

QScrollBar::handle:vertical {
    background: #2a3a4a;
    border-radius: 3px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #3a4a5a;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

/* === LIST WIDGET (Autocomplete) === */
QListWidget {
    border: 1px solid #2a3a4a;
    border-radius: 8px;
    background-color: #1a2635;
    font-size: 10pt;
    color: #e2e8f0;
}

QListWidget::item {
    padding: 8px 12px;
    border-bottom: 1px solid #1e2d3d;
}

QListWidget::item:selected, QListWidget::item:hover {
    background-color: #22c55e22;
    color: #22c55e;
}

/* === GROUPBOX === */
QGroupBox {
    border: 1px solid #2a3a4a;
    border-radius: 10px;
    margin-top: 12px;
    padding: 8px;
    color: #94a3b8;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    color: #22c55e;
}

/* === MESSAGEBOX === */
QMessageBox {
    background-color: #1a2635;
    color: #e2e8f0;
}

QMessageBox QLabel {
    color: #e2e8f0;
}

QMessageBox QPushButton {
    min-width: 80px;
    background-color: #22c55e;
    color: #0f1923;
    border-radius: 6px;
    padding: 6px 16px;
}

QMessageBox QPushButton:hover {
    background-color: #16a34a;
}

/* === SPINBOX / DATEEDIT === */
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    width: 20px;
    border: none;
    background-color: #2a3a4a;
}

QDateEdit::drop-down {
    border: none;
    width: 28px;
    background-color: transparent;
}

/* === FILTRE PANELI === */
#filterPanel {
    background-color: #1a2635;
    border: 1px solid #1e2d3d;
    border-radius: 10px;
    padding: 8px;
}

/* === BOS PANEL === */
#bosaMessaj {
    color: #2a3a4a;
    font-size: 13pt;
}

/* === DURUM ETIKETLERI === */
#etiketAktif {
    background-color: #22c55e22;
    color: #22c55e;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 9pt;
    font-weight: bold;
}

#etiketCikis {
    background-color: #ef444422;
    color: #ef4444;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 9pt;
    font-weight: bold;
}

/* === YEDEKLEME PANELI === */
#backupInfo {
    background-color: #1e2d3d;
    border: 1px solid #2a3a4a;
    border-radius: 10px;
    padding: 12px;
}

/* === LABEL === */
QLabel {
    color: #94a3b8;
    background: transparent;
}
"""
