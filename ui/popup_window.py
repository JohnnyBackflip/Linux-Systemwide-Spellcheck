from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QMouseEvent

class APICallThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, client, text):
        super().__init__()
        self.client = client
        self.text = text

    def run(self):
        corrected = self.client.correct_text(self.text)
        self.finished.emit(corrected)

class PopupWindow(QDialog):
    def __init__(self, gemini_client, system_hooks, text):
        super().__init__()
        self.client = gemini_client
        self.system_hooks = system_hooks
        self.original_text = text
        self.init_ui()
        self.start_correction()

    def init_ui(self):
        # Frameless, transparent background (glassmorphism feel), stays on top
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 250)
        
        self.setStyleSheet("""
            #container {
                background-color: rgba(32, 33, 36, 0.95);
                border-radius: 12px;
                border: 1px solid #5f6368;
            }
            QLabel {
                color: #e8eaed;
                font-family: 'Segoe UI', Roboto, sans-serif;
                font-size: 14px;
            }
            QLabel#status {
                color: #8ab4f8;
                font-weight: bold;
                font-size: 16px;
            }
            QTextEdit {
                background-color: rgba(48, 49, 52, 0.7);
                color: #e8eaed;
                border: 1px solid #5f6368;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton {
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#accept {
                background-color: #81c995;
                color: #202124;
            }
            QPushButton#accept:hover {
                background-color: #a4d8b2;
            }
            QPushButton#reject {
                background-color: #f28b82;
                color: #202124;
            }
            QPushButton#reject:hover {
                background-color: #f6aca6;
            }
        """)

        # Main container for rounded corners and transparency support
        self.container = QDialog(self)
        self.container.setObjectName("container")
        self.container.setFixedSize(400, 250)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.container)

        layout = QVBoxLayout(self.container)

        self.status_label = QLabel("Loading / Correcting...")
        self.status_label.setObjectName("status")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setPlainText("Analyzing the text with Gemini API...")
        layout.addWidget(self.text_display)

        btn_layout = QHBoxLayout()
        self.reject_btn = QPushButton("Reject")
        self.reject_btn.setObjectName("reject")
        self.reject_btn.clicked.connect(self.reject)
        
        self.accept_btn = QPushButton("Accept")
        self.accept_btn.setObjectName("accept")
        self.accept_btn.clicked.connect(self.accept_changes)
        self.accept_btn.hide()
        
        btn_layout.addWidget(self.reject_btn)
        btn_layout.addWidget(self.accept_btn)
        
        layout.addLayout(btn_layout)

    def start_correction(self):
        self.api_thread = APICallThread(self.client, self.original_text)
        self.api_thread.finished.connect(self.on_corrected)
        self.api_thread.start()

    def on_corrected(self, result):
        self.corrected_text = result
        self.status_label.setText("Correction Complete")
        self.text_display.setPlainText(self.corrected_text)
        self.accept_btn.show()

    def accept_changes(self):
        self.system_hooks.replace_text(self.corrected_text)
        self.close()

    def reject(self):
        self.system_hooks.restore_clipboard()
        self.close()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()
