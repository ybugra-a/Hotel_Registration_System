"""
Uygulama stilleri - v0.5 Koyu Tema
"""

MAIN_STYLE = """
/* === GENEL === */
QWidget {
    font-family: 'Segoe UI', Tahoma, Arial;
    font-size: 10pt;
    color: #e2e8f0;
    background-color: #1a1a2e;
}
QMainWindow { background-color: #1a1a2e; }

/* === TITLE BAR === */
#titleBar {
    background-color: #0f0f1a;
    border-bottom: 1px solid #2a2a3e;
}
#appTitle {
    font-size: 12pt; font-weight: bold; color: #ffffff; letter-spacing: -0.3px;
}

/* === STAT KARTLARI === */
#statKart {
    background-color: #252538;
    border-radius: 14px;
    border: 1px solid #2a2a3e;
}
#statBaslik { font-size: 9pt; font-weight: 500; color: #94a3b8; letter-spacing: 0.5px; }
#statDeger { font-size: 24pt; font-weight: bold; color: #ffffff; letter-spacing: -0.5px; }

/* === PANEL BASLIK === */
#panelTitle { font-size: 16pt; font-weight: bold; color: #ffffff; letter-spacing: -0.3px; }
#panelSubtitle { font-size: 9pt; color: #64748b; }

/* === ANA KARTLAR === */
#mainCard {
    background-color: #252538;
    border-radius: 16px;
    border: 1px solid #2a2a3e;
}

/* === FORM ALANLARI === */
QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox {
    background-color: #1e1e30;
    border: 1.5px solid #3a3a50;
    border-radius: 8px;
    padding: 9px 12px;
    font-size: 10pt;
    color: #e2e8f0;
    min-height: 22px;
}
QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QDoubleSpinBox:focus {
    border: 1.5px solid #22c55e;
    background-color: #1a1a2e;
}
QLineEdit:hover, QComboBox:hover { border-color: #4a4a60; }
QLineEdit::placeholder { color: #4a4a60; }

/* === FORM ETIKETLERI === */
#formLabel { font-size: 8pt; font-weight: bold; color: #64748b; letter-spacing: 0.5px; }

/* === COMBOBOX === */
QComboBox::drop-down { border: none; width: 28px; background: transparent; }
QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #38bdf8;
    margin-right: 8px;
}
QDateEdit::drop-down { border: none; width: 28px; background: transparent; }
QDateEdit::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #38bdf8;
    margin-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: #252538;
    border: 1.5px solid #3a3a50;
    border-radius: 8px;
    color: #e2e8f0;
    selection-background-color: #2a2a3e;
    selection-color: #22c55e;
    padding: 4px; outline: none;
}
QComboBox QAbstractItemView::item {
    background-color: #252538; color: #e2e8f0; padding: 9px 14px; min-height: 20px;
}
QComboBox QAbstractItemView::item:hover { background-color: #2a2a3e; color: #22c55e; }
QComboBox QAbstractItemView::item:selected { background-color: #2a2a3e; color: #22c55e; }

/* === BUTONLAR - Hepsine arka plan eklendi === */
QPushButton {
    border-radius: 8px; padding: 10px 20px;
    font-weight: 600; font-size: 10pt; min-height: 38px;
}

/* Kaydet - Yesil */
#btnKaydet {
    background-color: rgba(34,197,94,0.15);
    color: #22c55e;
    border: 2px solid #22c55e;
}
#btnKaydet:hover { background-color: rgba(34,197,94,0.28); color: #4ade80; border-color: #4ade80; }
#btnKaydet:pressed { background-color: rgba(34,197,94,0.40); }

/* Rezerve Et - Mor */
#btnRezarve {
    background-color: rgba(139,92,246,0.15);
    color: #a78bfa;
    border: 2px solid #8b5cf6;
}
#btnRezarve:hover { background-color: rgba(139,92,246,0.28); color: #c4b5fd; border-color: #a78bfa; }

/* Temizle - Gri */
#btnTemizle {
    background-color: rgba(100,116,139,0.12);
    color: #94a3b8;
    border: 2px solid #475569;
}
#btnTemizle:hover { background-color: rgba(100,116,139,0.22); color: #cbd5e1; border-color: #64748b; }

/* Duzenle - Mavi gri */
#btnDuzenle {
    background-color: rgba(100,116,139,0.12);
    color: #94a3b8;
    border: 2px solid #475569;
    padding: 6px 16px; font-size: 9pt; min-height: 32px; border-radius: 6px;
}
#btnDuzenle:hover { background-color: rgba(100,116,139,0.22); color: #cbd5e1; border-color: #64748b; }

/* Check-out - Kirmizi */
#btnCikis {
    background-color: rgba(239,68,68,0.15);
    color: #f87171;
    border: 2px solid #ef4444;
    padding: 6px 16px; font-size: 9pt; min-height: 32px; border-radius: 6px;
}
#btnCikis:hover { background-color: rgba(239,68,68,0.28); color: #fca5a5; border-color: #f87171; }

/* Ekle - Yesil */
#btnEkle {
    background-color: rgba(34,197,94,0.15);
    color: #22c55e;
    border: 2px solid #22c55e;
}
#btnEkle:hover { background-color: rgba(34,197,94,0.28); }

/* Sil - Kirmizi */
#btnSil {
    background-color: rgba(239,68,68,0.12);
    color: #f87171;
    border: 2px solid #ef4444;
}
#btnSil:hover { background-color: rgba(239,68,68,0.25); color: #fca5a5; }

/* Ara - Cyan */
#btnAra {
    background-color: rgba(56,189,248,0.12);
    color: #38bdf8;
    border: 2px solid #38bdf8;
}
#btnAra:hover { background-color: rgba(56,189,248,0.22); color: #7dd3fc; }

/* Yedekle - Amber */
#btnYedekle {
    background-color: rgba(251,191,36,0.12);
    color: #fbbf24;
    border: 2px solid #f59e0b;
}
#btnYedekle:hover { background-color: rgba(251,191,36,0.22); }

/* Kara Listeye Ekle - Koyu kirmizi */
#btnBlacklist {
    background-color: rgba(239,68,68,0.18);
    color: #fca5a5;
    border: 2px solid #dc2626;
}
#btnBlacklist:hover { background-color: rgba(239,68,68,0.32); color: #ffffff; border-color: #ef4444; }

/* Iptal - Turuncu */
#btnIptal {
    background-color: rgba(251,146,60,0.12);
    color: #fb923c;
    border: 2px solid #f97316;
    padding: 6px 14px; font-size: 9pt; min-height: 30px; border-radius: 6px;
}
#btnIptal:hover { background-color: rgba(251,146,60,0.25); }

/* Check-in - Yesil kucuk */
#btnCheckin {
    background-color: rgba(34,197,94,0.15);
    color: #4ade80;
    border: 2px solid #22c55e;
    padding: 6px 14px; font-size: 9pt; min-height: 30px; border-radius: 6px;
}
#btnCheckin:hover { background-color: rgba(34,197,94,0.28); }

/* === MISAFIR KARTI === */
#musteriKart {
    background-color: #1e1e30;
    border: 1px solid #2a2a3e;
    border-radius: 12px; margin: 2px 0; padding: 14px;
}
#musteriKart:hover { border-color: #3a3a50; background-color: #22223a; }
#musteriIsim { font-size: 11pt; font-weight: bold; color: #ffffff; }
#musteriOda {
    font-size: 9pt; color: #22c55e; font-weight: 600;
    background-color: rgba(34,197,94,0.12);
    border: 1px solid rgba(34,197,94,0.30);
    border-radius: 4px; padding: 1px 7px;
}
#musteriTarih { font-size: 9pt; color: #64748b; }

/* === REZERVASYON KARTI === */
#rezervKart {
    background-color: #1e1e30;
    border: 1px solid #3a3050;
    border-radius: 12px; margin: 2px 0; padding: 14px;
}
#rezervKart:hover { border-color: #5a4a70; }

/* === BADGE === */
#odemeUyari {
    font-size: 8pt; color: #fbbf24; font-weight: bold;
    background-color: rgba(251,191,36,0.12);
    border: 1.5px solid #f59e0b; border-radius: 5px; padding: 3px 10px;
}
#odemeVar {
    font-size: 8pt; color: #4ade80; font-weight: bold;
    background-color: rgba(34,197,94,0.12);
    border: 1.5px solid #22c55e; border-radius: 5px; padding: 3px 10px;
}
#rezervBadge {
    font-size: 8pt; color: #a78bfa; font-weight: bold;
    background-color: rgba(139,92,246,0.12);
    border: 1.5px solid #8b5cf6; border-radius: 5px; padding: 3px 10px;
}

/* === ODA KARTLARI === */
#odaMusait {
    background-color: rgba(34,197,94,0.08);
    border: 1.5px solid rgba(34,197,94,0.30);
    border-radius: 10px; padding: 10px;
}
#odaDolu {
    background-color: rgba(239,68,68,0.08);
    border: 1.5px solid rgba(239,68,68,0.30);
    border-radius: 10px; padding: 10px;
}
#odaNo { font-size: 14pt; font-weight: bold; color: #ffffff; }
#odaDurumMusait { color: #4ade80; font-weight: bold; font-size: 9pt; }
#odaDurumDolu { color: #f87171; font-weight: bold; font-size: 9pt; }

/* === TABLO === */
QTableWidget {
    border: 1px solid #2a2a3e; border-radius: 12px;
    background-color: #1e1e30; gridline-color: #2a2a3e;
    selection-background-color: rgba(34,197,94,0.15);
    selection-color: #4ade80;
    alternate-background-color: #22223a;
}
QTableWidget::item { padding: 8px 12px; border-bottom: 1px solid #2a2a3e; color: #cbd5e1; }
QTableWidget::item:selected { background-color: rgba(34,197,94,0.15); color: #4ade80; }
QHeaderView::section {
    background-color: #1a1a2e; color: #64748b; padding: 10px 12px;
    border: none; border-bottom: 1px solid #2a2a3e;
    font-weight: bold; font-size: 8pt; letter-spacing: 0.5px;
}

/* === SCROLL === */
QScrollArea { border: none; background: transparent; }
QScrollBar:vertical { border: none; background: #1e1e30; width: 6px; border-radius: 3px; }
QScrollBar::handle:vertical { background: #3a3a50; border-radius: 3px; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #4a4a60; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

/* === AUTOCOMPLETE === */
QListWidget {
    border: 1.5px solid #3a3a50; border-radius: 8px;
    background-color: #252538; color: #e2e8f0;
}
QListWidget::item { padding: 8px 12px; border-bottom: 1px solid #2a2a3e; color: #e2e8f0; }
QListWidget::item:hover, QListWidget::item:selected { background-color: #2a2a3e; color: #22c55e; }

/* === GROUPBOX === */
QGroupBox {
    border: 1px solid #2a2a3e; border-radius: 10px;
    margin-top: 12px; padding: 8px; background-color: #252538;
}
QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 6px; color: #22c55e; font-weight: bold; }

/* === MESSAGEBOX === */
QMessageBox { background-color: #252538; }
QMessageBox QLabel { color: #e2e8f0; font-size: 10pt; }
QMessageBox QPushButton {
    min-width: 80px; background-color: rgba(34,197,94,0.15);
    color: #22c55e; border: 2px solid #22c55e;
    border-radius: 6px; padding: 6px 16px; font-weight: 600;
}
QMessageBox QPushButton:hover { background-color: rgba(34,197,94,0.28); }

/* === SPINBOX === */
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button { width: 20px; border: none; background: #2a2a3e; }

/* === FILTRE === */
#filterPanel { background-color: #252538; border: 1px solid #2a2a3e; border-radius: 10px; padding: 10px; }
#bosaMessaj { color: #3a3a50; font-size: 12pt; }

/* === DURUM ETIKETLERI === */
#etiketAktif {
    background-color: rgba(34,197,94,0.12); color: #4ade80;
    border: 1.5px solid #22c55e; border-radius: 4px; padding: 2px 8px;
    font-size: 8pt; font-weight: bold;
}
#etiketCikis {
    background-color: rgba(239,68,68,0.10); color: #f87171;
    border: 1.5px solid #ef4444; border-radius: 4px; padding: 2px 8px;
    font-size: 8pt; font-weight: bold;
}

/* === YEDEKLEME === */
#backupInfo { background-color: #252538; border: 1px solid #3a3a50; border-radius: 10px; padding: 12px; }

/* === PROGRESS BAR === */
QProgressBar { border: none; border-radius: 3px; background-color: #2a2a3e; height: 8px; }
QProgressBar::chunk { border-radius: 3px; background-color: #3a3a50; }

/* === LABEL === */
QLabel { color: #94a3b8; background: transparent; }
"""
