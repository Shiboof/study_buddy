import customtkinter as ctk
from dotenv import load_dotenv
import os
from pathlib import Path
import sys
from ui import setup_ui
from api import app  # ✅ Use the app defined in api/__init__.py
import api.routes     # ✅ This registers your /api/* routes
from flask import send_from_directory

CURRENT_VERSION = "v1.0.3"
GITHUB_API_URL = "https://api.github.com/repos/Shiboof/study_buddy/releases/latest"

# Load .env file for API keys, etc.
load_dotenv()

def run_gui():
    """Launch the GUI for Study Buddy."""
    root = ctk.CTk()
    root.title("Study Buddy")
    root.geometry("1000x600")
    setup_ui(root)
    root.mainloop()

if __name__ == "__main__":
    if "RUN_GUI" in os.environ:
        run_gui()  # Launch the GUI if RUN_GUI is set
    else:
        app.run(host="0.0.0.0", port=8080)  # Run the Flask API server
