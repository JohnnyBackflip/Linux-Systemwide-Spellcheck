import time
import pyperclip
from pynput import keyboard
from PyQt6.QtCore import QObject, pyqtSignal

class SystemHooks(QObject):
    # This signal will carry the copied text back to the main GUI thread
    triggered = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.last_alt_press = 0
        self.double_tap_threshold = 0.4 # seconds
        self.controller = keyboard.Controller()
        # Listen globally
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.original_clipboard = ""

    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()

    def on_press(self, key):
        if key == keyboard.Key.alt or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            current_time = time.time()
            if current_time - self.last_alt_press < self.double_tap_threshold:
                # Double tap detected
                self.last_alt_press = 0 # reset to prevent multiple triggers
                self.handle_trigger()
            else:
                self.last_alt_press = current_time

    def on_release(self, key):
        pass

    def handle_trigger(self):
        # Backup clipboard
        self.original_clipboard = pyperclip.paste()
        
        # Clear clipboard temporarily to reliably detect new copy
        pyperclip.copy('')
        
        # Simulate Ctrl+C to copy highlighted text
        with self.controller.pressed(keyboard.Key.ctrl):
            self.controller.press('c')
            self.controller.release('c')
        
        # Wait for clipboard to update (up to 0.5s)
        copied_text = ""
        for _ in range(10):
            time.sleep(0.05)
            copied_text = pyperclip.paste()
            if copied_text:
                break
                
        if not copied_text:
            # Restore if nothing copied
            self.restore_clipboard()
            return
            
        # Emit signal to PyQt6 Main Thread
        # We don't want to block the pynput listener
        self.triggered.emit(copied_text)

    def replace_text(self, new_text):
        # Copy new text to clipboard
        pyperclip.copy(new_text)
        time.sleep(0.05)
        
        # Simulate Ctrl+V to replace
        with self.controller.pressed(keyboard.Key.ctrl):
            self.controller.press('v')
            self.controller.release('v')
            
        time.sleep(0.1)
        
        # Restore old clipboard
        self.restore_clipboard()

    def restore_clipboard(self):
        pyperclip.copy(self.original_clipboard)
