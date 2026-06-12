"""
Custom Dialog - v0.6.1
Koyu tema, frameless, suruklenebilir
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont


class CustomDialog(QDialog):
    """Koyu temali, frameless temel dialog"""

    def __init__(self, parent=None, title="Bilgi", message="", dialog_type="info"):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self._drag_pos = None
        self.setMinimumWidth(380)
        self._setup_ui(title, message, dialog_type)

    def _setup_ui(self, title, message, dialog_type):
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a2e;
                border: 1px solid #3a3a50;
                border-radius: 10px;
            }
        """)

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        # Title bar
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background-color: #0f0f1a; border-radius: 10px 10px 0 0;")
        title_bar.mousePressEvent = self._on_press
        title_bar.mouseMoveEvent = self._on_move

        tb_layout = QHBoxLayout(title_bar)
        tb_layout.setContentsMargins(16, 0, 4, 0)
        tb_layout.setSpacing(0)
        tb_layout.setAlignment(Qt.AlignVCenter)

        # Ikon
        icons = {"info": "ℹ", "warning": "⚠", "error": "✕", "question": "?"}
        colors = {"info": "#3b82f6", "warning": "#f59e0b", "error": "#ef4444", "question": "#22c55e"}
        icon_color = colors.get(dialog_type, "#3b82f6")

        icon_lbl = QLabel(icons.get(dialog_type, "ℹ"))
        icon_lbl.setStyleSheet(f"color: {icon_color}; font-size: 13pt; background: transparent;")
        icon_lbl.setAlignment(Qt.AlignCenter)
        tb_layout.addWidget(icon_lbl, 0, Qt.AlignVCenter)
        tb_layout.addSpacing(8)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #ffffff; font-size: 10pt; font-weight: 600; background: transparent;")
        tb_layout.addWidget(title_lbl, 0, Qt.AlignVCenter)
        tb_layout.addStretch()

        btn_close = QPushButton("✕")
        btn_close.setFixedSize(40, 40)
        btn_close.setStyleSheet("""
            QPushButton {
                background: transparent; color: #64748b;
                border: none; font-size: 12pt; border-radius: 4px;
                min-width: 40px; max-width: 40px;
                min-height: 40px; max-height: 40px;
                qproperty-alignment: AlignCenter;
                padding: 0px; margin: 0px;
            }
            QPushButton:hover { background: #dc2626; color: #ffffff; }
        """)
        btn_close.clicked.connect(self.reject)
        tb_layout.addWidget(btn_close, 0, Qt.AlignVCenter)
        main.addWidget(title_bar)

        # Ayirici
        sep = QWidget()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: #2a2a3e;")
        main.addWidget(sep)

        # Mesaj alani
        content = QWidget()
        content.setStyleSheet("background-color: #1a1a2e;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(20)

        msg_lbl = QLabel(message)
        msg_lbl.setWordWrap(True)
        msg_lbl.setStyleSheet("color: #e2e8f0; font-size: 10pt; background: transparent; line-height: 1.5;")
        msg_lbl.setAlignment(Qt.AlignLeft)
        content_layout.addWidget(msg_lbl)

        main.addWidget(content)

        # Alt ayirici
        sep2 = QWidget()
        sep2.setFixedHeight(1)
        sep2.setStyleSheet("background-color: #2a2a3e;")
        main.addWidget(sep2)

        # Buton alani - alt kisim
        btn_area = QWidget()
        btn_area.setStyleSheet("background-color: #0f0f1a; border-radius: 0 0 10px 10px;")
        btn_layout = QHBoxLayout(btn_area)
        btn_layout.setContentsMargins(16, 12, 16, 12)
        btn_layout.addStretch()
        main.addWidget(btn_area)

        self._btn_layout = btn_layout

    def add_button(self, text, role="accept", color="#22c55e"):
        """Buton ekle"""
        btn = QPushButton(text)
        btn.setFixedHeight(34)
        btn.setMinimumWidth(80)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba({self._hex_to_rgb(color)}, 0.15);
                color: {color};
                border: 2px solid {color};
                border-radius: 6px;
                padding: 4px 16px;
                font-weight: 600;
                font-size: 10pt;
            }}
            QPushButton:hover {{
                background-color: rgba({self._hex_to_rgb(color)}, 0.28);
            }}
        """)
        if role == "accept":
            btn.clicked.connect(self.accept)
        elif role == "reject":
            btn.clicked.connect(self.reject)
        self._btn_layout.addWidget(btn)
        return btn

    def _hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return f"{r}, {g}, {b}"

    def _on_press(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def _on_move(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_pos:
            self.move(event.globalPos() - self._drag_pos)


# ----------------------------------------------------------------
# Hazir dialog fonksiyonlari
# ----------------------------------------------------------------

def show_info(parent, title, message):
    d = CustomDialog(parent, title, message, "info")
    d.add_button("Tamam", "accept", "#3b82f6")
    d.exec_()


def show_warning(parent, title, message):
    d = CustomDialog(parent, title, message, "warning")
    d.add_button("Tamam", "accept", "#f59e0b")
    d.exec_()


def show_error(parent, title, message):
    d = CustomDialog(parent, title, message, "error")
    d.add_button("Tamam", "accept", "#ef4444")
    d.exec_()


def show_question(parent, title, message):
    """Evet/Hayir sorusu. True/False doner."""
    d = CustomDialog(parent, title, message, "question")
    d.add_button("Hayir", "reject", "#64748b")
    d.add_button("Evet", "accept", "#22c55e")
    return d.exec_() == QDialog.Accepted
