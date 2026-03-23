import sys
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction, QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt, QRect

from core.config import ConfigManager
from core.gemini_client import GeminiClient
from core.system_hooks import SystemHooks
from ui.settings_window import SettingsWindow
from ui.help_window import HelpWindow
from ui.popup_window import PopupWindow

def create_tray_icon():
    pixmap = QPixmap(64, 64)
    pixmap.fill(QColor("transparent"))
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QColor("#8ab4f8"))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(4, 4, 56, 56)
    painter.setPen(QColor("#202124"))
    font = painter.font()
    font.setPointSize(28)
    font.setBold(True)
    painter.setFont(font)
    painter.drawText(QRect(0, 0, 64, 64), Qt.AlignmentFlag.AlignCenter, "S")
    painter.end()
    return QIcon(pixmap)

class Application:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        self.config = ConfigManager()
        self.client = GeminiClient(self.config)
        self.hooks = SystemHooks()
        
        # Connect hook signal to UI popup ensuring it runs on the main thread
        self.hooks.triggered.connect(self.show_popup, Qt.ConnectionType.QueuedConnection)
        
        self.setup_tray()
        
        # Start listening for Alt double-tap
        self.hooks.start()

    def setup_tray(self):
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(create_tray_icon())
        self.tray.setVisible(True)

        self.menu = QMenu()
        
        self.settings_action = QAction("Settings")
        self.settings_action.triggered.connect(self.show_settings)
        self.menu.addAction(self.settings_action)
        
        self.help_action = QAction("Help")
        self.help_action.triggered.connect(self.show_help)
        self.menu.addAction(self.help_action)
        
        self.menu.addSeparator()
        
        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(self.quit_app)
        self.menu.addAction(self.quit_action)

        self.tray.setContextMenu(self.menu)

    def show_popup(self, text):
        if not text.strip():
            self.hooks.restore_clipboard()
            return
            
        self.popup = PopupWindow(self.client, self.hooks, text)
        
        from PyQt6.QtGui import QCursor
        cursor_pos = QCursor.pos()
        cursor_pos.setX(cursor_pos.x() + 10)
        cursor_pos.setY(cursor_pos.y() + 10)
        self.popup.move(cursor_pos)
        
        self.popup.show()

    def show_settings(self):
        self.settings_window = SettingsWindow(self.config, self.client)
        self.settings_window.show()

    def show_help(self):
        self.help_window = HelpWindow()
        self.help_window.show()

    def quit_app(self):
        self.hooks.stop()
        self.app.quit()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = Application()
    app.run()
