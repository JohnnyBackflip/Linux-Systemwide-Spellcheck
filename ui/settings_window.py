from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QComboBox, QTextEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class ModelFetcherThread(QThread):
    models_fetched = pyqtSignal(list)

    def __init__(self, gemini_client):
        super().__init__()
        self.client = gemini_client

    def run(self):
        models = self.client.get_models()
        self.models_fetched.emit(models)

class SettingsWindow(QDialog):
    def __init__(self, config_manager, gemini_client):
        super().__init__()
        self.config = config_manager
        self.client = gemini_client
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Spellcheck Settings" if self.config.get("language") == "en" else "Rechtschreibprüfung Einstellungen")
        self.setFixedSize(500, 450)
        self.setStyleSheet("""
            QDialog {
                background-color: #202124;
                color: #e8eaed;
            }
            QLabel {
                color: #e8eaed;
                font-family: 'Segoe UI', Roboto, sans-serif;
                font-size: 14px;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #303134;
                color: #e8eaed;
                border: 1px solid #5f6368;
                border-radius: 4px;
                padding: 5px;
                font-size: 13px;
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

        # Language
        lang_layout = QHBoxLayout()
        lang_label = QLabel("Language / Sprache:")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English (en)", "Deutsch (de)"])
        if self.config.get("language") == "de":
            self.lang_combo.setCurrentIndex(1)
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_combo)
        layout.addLayout(lang_layout)

        # API Key
        self.api_label = QLabel("Gemini API Key:")
        self.api_input = QLineEdit()
        self.api_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_input.setText(self.config.get("api_key", ""))
        layout.addWidget(self.api_label)
        layout.addWidget(self.api_input)

        # Models
        self.model_label = QLabel("Model:")
        self.model_combo = QComboBox()
        self.model_combo.addItem(self.config.get("model", "gemini-3.1-flash-lite-preview"))
        
        # Refresh models button
        model_layout = QHBoxLayout()
        model_layout.addWidget(self.model_combo)
        self.refresh_btn = QPushButton("Refresh List")
        self.refresh_btn.clicked.connect(self.fetch_models)
        model_layout.addWidget(self.refresh_btn)
        
        layout.addWidget(self.model_label)
        layout.addLayout(model_layout)

        # System Prompt
        self.prompt_label = QLabel("System Prompt:")
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlainText(self.config.get("system_prompt", ""))
        layout.addWidget(self.prompt_label)
        layout.addWidget(self.prompt_input)

        # Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_settings)
        btn_layout.addStretch()
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.update_labels()

        self.lang_combo.currentIndexChanged.connect(self.update_labels)

    def update_labels(self):
        is_de = self.lang_combo.currentIndex() == 1
        self.setWindowTitle("Rechtschreibprüfung Einstellungen" if is_de else "Spellcheck Settings")
        self.api_label.setText("Gemini API-Schlüssel:" if is_de else "Gemini API Key:")
        self.model_label.setText("Modell:" if is_de else "Model:")
        self.prompt_label.setText("System-Prompt:" if is_de else "System Prompt:")
        self.save_btn.setText("Speichern" if is_de else "Save")
        self.refresh_btn.setText("Liste aktualisieren" if is_de else "Refresh List")

    def fetch_models(self):
        # Temporarily save API key for fetch
        self.config.set("api_key", self.api_input.text().strip())
        self.refresh_btn.setEnabled(False)
        self.refresh_btn.setText("Fetching...")
        
        self.fetcher = ModelFetcherThread(self.client)
        self.fetcher.models_fetched.connect(self.on_models_fetched)
        self.fetcher.start()

    def on_models_fetched(self, models):
        self.model_combo.clear()
        self.model_combo.addItems(models)
        
        # Restore selection
        saved_model = self.config.get("model")
        index = self.model_combo.findText(saved_model)
        if index >= 0:
            self.model_combo.setCurrentIndex(index)
            
        self.refresh_btn.setEnabled(True)
        self.update_labels() # resets button text

    def save_settings(self):
        self.config.set("api_key", self.api_input.text().strip())
        self.config.set("model", self.model_combo.currentText())
        self.config.set("system_prompt", self.prompt_input.toPlainText().strip())
        self.config.set("language", "de" if self.lang_combo.currentIndex() == 1 else "en")
        
        QMessageBox.information(self, "Success", "Settings saved successfully! / Einstellungen erfolgreich gespeichert!")
        self.accept()
