import customtkinter as ctk
import requests
from ui import setup_ui

GITHUB_API_URL = "https://api.github.com/repos/<username>/<repository>/releases/latest"
CURRENT_VERSION = "1.0.0"  # Replace with your app's current version

def show_ctk_messagebox(title, message, message_type="info"):
    """Custom message box using customtkinter."""
    dialog = ctk.CTkToplevel()
    dialog.title(title)
    dialog.geometry("400x200")
    dialog.resizable(False, False)

    # Set dialog appearance
    ctk.set_appearance_mode("dark")  # Optional: Match the app's appearance mode

    # Add message label
    label = ctk.CTkLabel(dialog, text=message, font=("Helvetica", 14), wraplength=350)
    label.pack(pady=20, padx=20)

    # Add OK button
    ok_button = ctk.CTkButton(dialog, text="OK", command=dialog.destroy, fg_color="blue", hover_color="darkblue")
    ok_button.pack(pady=10)

    # Center the dialog on the screen
    dialog.grab_set()  # Make the dialog modal
    dialog.wait_window()  # Wait for the dialog to close

def check_for_updates():
    """Check GitHub for the latest release version."""
    try:
        response = requests.get(GITHUB_API_URL, timeout=5)
        response.raise_for_status()  # Raise an error for HTTP issues
        latest_release = response.json()
        latest_version = latest_release.get("tag_name", "0.0.0")  # Get the latest version tag

        if latest_version > CURRENT_VERSION:
            show_ctk_messagebox(
                "Update Available",
                f"A new version ({latest_version}) is available! Please update your application."
            )
        else:
            show_ctk_messagebox("Up-to-Date", "You are using the latest version.")
    except requests.RequestException as e:
        show_ctk_messagebox("Update Check Failed", f"Could not check for updates: {e}", message_type="error")

def main():
    """Main entry point for the Study Buddy application."""
    root = ctk.CTk()
    root.title("Study Buddy")
    root.geometry("600x600")
    root.configure(fg_color="white")

    # Check for updates
    check_for_updates()

    # Set up the UI
    setup_ui(root)

    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()

