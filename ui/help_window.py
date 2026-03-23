from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class HelpWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linux Spellcheck - Help")
        self.setFixedSize(500, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #202124;
                color: #e8eaed;
            }
            QLabel {
                color: #e8eaed;
                font-family: 'Segoe UI', Roboto, sans-serif;
                font-size: 14px;
                line-height: 1.5;
            }
            QLabel#title {
                font-size: 20px;
                font-weight: bold;
                color: #8ab4f8;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #8ab4f8;
                color: #202124;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #aebce5;
            }
        """)

        layout = QVBoxLayout()
        
        title = QLabel("How to use the System-wide Spellchecker")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        content = QLabel(
            "1. <b>Configuration:</b><br>"
            "Right-click the system tray icon, click 'Settings' and enter your Google Gemini API key.<br><br>"
            "2. <b>Triggering a Check:</b><br>"
            "Highlight any text in any application where you can copy text.<br>"
            "Quickly double-tap the <b>Alt</b> key. The system will copy the text and analyze it.<br><br>"
            "3. <b>Reviewing:</b><br>"
            "A small floating window will appear showing the loading state.<br>"
            "Once complete, it shows the corrected text.<br><br>"
            "4. <b>Action:</b><br>"
            "Click <b>Accept</b> to automatically replace your text in the active application.<br>"
            "Click <b>Reject</b> or click anywhere outside the window to cancel."
        )
        content.setWordWrap(True)
        layout.addWidget(content)

        close_btn = QPushButton("Got it!")
        close_btn.clicked.connect(self.accept)
        layout.addStretch()
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
