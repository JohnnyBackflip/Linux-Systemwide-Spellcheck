# Linux System-wide Spellchecker

A system-wide AI-powered spellchecker for Linux using the Google Gemini API. Work universally across all desktop applications (Browsers, Slack, Terminals, Discord, etc.) by highlighting text and double-tapping the `Alt` key.

## Features
- **Global Trigger:** Double-tap `Alt` to correct highlighted text anywhere.
- **AI-Powered:** Uses Google Gemini API with uncensored access (`BLOCK_NONE` safety settings) for accurate, unfiltered grammatical correction.
- **Premium UI:** PyQt6-based borderless floating popup and system tray integration.
- **Clipboard Management:** Safely backs up and restores your clipboard after pasting the corrected text inline.
- **Autostart:** Automatically runs in the background on system boot.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/JohnnyBackflip/Linux-Systemwide-Spellcheck.git
   cd Linux-Systemwide-Spellcheck
   ```

2. **Install Dependencies:**
   Requires Python 3.
   ```bash
   pip install -r requirements.txt
   ```
   *Note: depending on your Linux distribution, you might need to install `xclip` or `xdotool` if `pyperclip` requires it natively.*

3. **Configure Autostart:**
   ```bash
   python3 scripts/install_autostart.py
   ```

4. **Run the Daemon:**
   ```bash
   python3 main.py
   ```

## Configuration
1. Right-click the system tray icon (blue "S") and click **Settings**.
2. Enter your Gemini API Key. (Get one from Google AI Studio).
3. The model list will dynamically populate. `gemini-3.1-flash-lite-preview` is the default.
4. Modify the system prompt or language if needed.
