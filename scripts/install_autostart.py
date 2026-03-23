import os
from pathlib import Path

def setup_autostart():
    autostart_dir = Path.home() / ".config" / "autostart"
    autostart_dir.mkdir(parents=True, exist_ok=True)
    
    desktop_file = autostart_dir / "linux-spellcheck.desktop"
    
    project_dir = Path(__file__).resolve().parent.parent
    main_script = project_dir / "main.py"
    
    desktop_entry = f"""[Desktop Entry]
Type=Application
Exec=python3 {main_script}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Linux Spellcheck
Comment=System-wide AI spelling correction via Gemini
Icon=text-editor
"""
    
    with open(desktop_file, "w") as f:
        f.write(desktop_entry)
        
    print(f"Autostart configured: {desktop_file}")

if __name__ == "__main__":
    setup_autostart()
