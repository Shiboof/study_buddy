import customtkinter as ctk
import requests
from dotenv import load_dotenv
import os
from pathlib import Path
import sys
from ui import setup_ui


CURRENT_VERSION = "v1.0.2"
GITHUB_API_URL = "https://api.github.com/repos/Shiboof/study_buddy/releases/latest"

def show_ctk_messagebox(title, message, message_type="info"):
    """Custom message box using customtkinter."""
    dialog = ctk.CTkToplevel()
    dialog.title(title)
    dialog.geometry("400x200")
    dialog.resizable(False, False)

    ctk.set_appearance_mode("dark")

    label = ctk.CTkLabel(dialog, text=message, font=("Helvetica", 14), wraplength=350)
    label.pack(pady=20, padx=20)

    ok_button = ctk.CTkButton(dialog, text="OK", command=dialog.destroy, fg_color="blue", hover_color="darkblue")
    ok_button.pack(pady=10)

    dialog.grab_set()
    dialog.wait_window()

def check_for_updates():
    """Check GitHub for the latest release version."""
    try:
        response = requests.get(GITHUB_API_URL, timeout=5)
        response.raise_for_status()
        latest_release = response.json()
        latest_version = latest_release.get("tag_name", "0.0.0")

        if latest_version > CURRENT_VERSION:
            message = (
                f"A new version ({latest_version}) is available!\n"
                f"Please update your application.\n\n"
                f"Visit\nhttps://github.com/Shiboof/study_buddy/releases\n to download the latest version."
            )
            show_ctk_messagebox("Update Available", message)
        else:
            show_ctk_messagebox("Up-to-Date", "You are using the latest version.")
    except requests.RequestException as e:
        show_ctk_messagebox("Update Check Failed", f"Could not check for updates: {e}", message_type="error")

def main():
    """Main entry point for the Study Buddy application."""
    root = ctk.CTk()
    root.title("Study Buddy")
    root.geometry("1000x600")

    check_for_updates()
    setup_ui(root)
    root.mainloop()

if __name__ == "__main__":
    main()

