import customtkinter as ctk
from tkinter import filedialog
from content_gen import generate_study_content, generate_flashcards, run_quiz, run_test, upload_context_file, generate_answers
from api.storage import save_study_data_to_file
from PIL import Image, ImageTk  # Import Pillow for image resizing
import sys
from pathlib import Path
import requests

'''
File will handle the UI setup and connect the buttons to the backend logic.
'''

# Dictionary to store generated study data
study_data = {
    "content": "",
    "flashcards": "",
    "quiz": "",
}

is_dark_mode = False

def toggle_dark_mode(root):
    """Toggle between light and dark mode."""
    global is_dark_mode
    is_dark_mode = not is_dark_mode

    # Define light and dark mode colors
    if is_dark_mode:
        ctk.set_appearance_mode("dark")  # Set customtkinter to dark mode
    else:
        ctk.set_appearance_mode("light")  # Set customtkinter to light mode

def setup_ui(root):
    """Set up the UI components."""
    ctk.set_appearance_mode("light")  # Set default appearance mode to light

    # Dynamically locate the assets folder
    if getattr(sys, 'frozen', False):  # Check if running as a PyInstaller bundle
        base_dir = Path(sys._MEIPASS)  # Temporary folder for PyInstaller
    else:
        base_dir = Path(__file__).resolve().parent

    assets_path = base_dir / "assets"

    # Load and resize the moon image using CTkImage
    moon_image_path = assets_path / "moon.png"  # Path to moon image
    try:
        moon_image = Image.open(moon_image_path)  # Open the image using Pillow
        moon_photo = ctk.CTkImage(light_image=moon_image, dark_image=moon_image, size=(30, 30))  # Use CTkImage
    except Exception as e:
        print(f"Error loading image: {e}")
        moon_photo = None

    if moon_photo:
        dark_mode_button = ctk.CTkButton(
            root,
            image=moon_photo,
            text="",
            command=lambda: toggle_dark_mode(root),
            fg_color="transparent",
            hover_color="lightblue",
            width=30,
            height=30,
            corner_radius=15
        )
        dark_mode_button.place(x=10, y=10)  # Position the button at the top left corner

    # Title Label
    title_label = ctk.CTkLabel(root, text="Study Buddy", font=("Helvetica", 20, "bold"), text_color="blue")
    title_label.pack(pady=10)

    # Instructions
    instructions = ctk.CTkLabel(root, text="Enter a topic and use the buttons below to generate study materials.", 
                                font=("Helvetica", 12))
    instructions.pack(pady=5)

    # Input Frame
    input_frame = ctk.CTkFrame(root)
    input_frame.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(input_frame, text="Enter Topic:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry = ctk.CTkEntry(input_frame, width=300, font=("Helvetica", 12))
    entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Frame for study data display
    study_data_frame = ctk.CTkFrame(root)
    study_data_frame.pack(side="right", padx =10, pady=10, fill="y") # Postion the study data drame on the

    study_data_label = ctk.CTkLabel(study_data_frame, text="Downloadable Content:", font=("Helvetica", 14, "bold"))
    study_data_label.pack(pady=5) # Add padding around the label

    # Add a CTkTexbox to the study_data_frame
    study_data_box = ctk.CTkTextbox(study_data_frame, width=300, height=400, font=("Helvetica", 10))
    study_data_box.pack(fill="both", expand=True)

    def update_study_data_display():
        """Update the study data display area."""
        # Clear current contents of the frame
        # Clear the current contents of the textbox
        study_data_box.delete("1.0", "end")

        # Add each key-value pair from study_data to the textbox
        for key, value in study_data.items():
            study_data_box.insert("end", f"{key.capitalize()}:\n{value if value else 'No data'}\n\n")

    # Button Frame
    button_frame = ctk.CTkFrame(root)
    button_frame.pack(pady=10)

    # Create buttons using ctk.CTkButton
    buttons = []
    buttons.append(ctk.CTkButton(button_frame, text="Generate Study Content", 
                                 command=lambda: [generate_study_content(entry.get(), output_box, study_data), update_study_data_display()], 
                                 fg_color="blue", hover_color="darkblue", width=200, height=40, corner_radius=10))
    buttons.append(ctk.CTkButton(button_frame, text="Generate Flashcards", 
                                 command=lambda: [generate_flashcards(entry.get(), output_box, study_data), update_study_data_display()], 
                                 fg_color="green", hover_color="darkgreen", width=200, height=40, corner_radius=10))
    buttons.append(ctk.CTkButton(button_frame, text="Generate Quiz", 
                                 command=lambda: [run_quiz(entry.get(), output_box, study_data), update_study_data_display()], 
                                 fg_color="orange", hover_color="gold", width=200, height=40, corner_radius=10))
    buttons.append(ctk.CTkButton(button_frame, text="Generate Test", 
                                 command=lambda: [run_test(entry.get(), output_box, study_data), update_study_data_display()], 
                                 fg_color="orange", hover_color="gold", width=200, height=40, corner_radius=10))
    buttons.append(ctk.CTkButton(button_frame, text="Upload Context File", 
                                 command=lambda: upload_file(output_box), 
                                 fg_color="red", hover_color="darkred", width=200, height=40, corner_radius=10))
    buttons.append(ctk.CTkButton(button_frame, text="Download Content", 
                                 command=lambda: save_study_data_to_file(study_data), 
                                 fg_color="coral", hover_color="darkred", width=200, height=40, corner_radius=10))
    buttons.append(ctk.CTkButton(button_frame, text="Study Data Answers",
                                command=lambda: [generate_answers(output_box, study_data), update_study_data_display()],
                                fg_color="purple", hover_color="darkviolet", width=200, height=40, corner_radius=10))
    buttons.append(ctk.CTkButton(button_frame, text="Send Topic to API",
                                command=lambda: send_topic_to_api(entry.get()),
                                fg_color="gray", hover_color="darkgray",
                                width=200, height=40, corner_radius=10))
    buttons.append(ctk.CTkButton(button_frame, text="Show Topics from API",
                             command=lambda: output_box.insert("end", "\n".join(get_topics_from_api()) + "\n"),
                             fg_color="teal", hover_color="darkcyan",
                             width=200, height=40, corner_radius=10))



    # Arrange buttons in a grid
    for i, button in enumerate(buttons):
        button.grid(row=i // 2, column=i % 2, padx=10, pady=10)

    # Output Frame
    output_frame = ctk.CTkFrame(root)
    output_frame.pack(pady=10, padx=20, fill="both", expand=True)

    output_label = ctk.CTkLabel(output_frame, text="Output:", font=("Helvetica", 12))
    output_label.pack(anchor="w")

    global output_box
    output_box = ctk.CTkTextbox(output_frame, height=15, width=70, font=("Helvetica", 10))
    output_box.pack(side="left", fill="both", expand=True)

def upload_file(output_box):
    """Open a file dialog to upload a file and store its content."""
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    if file_path:
        result = upload_context_file(file_path)  # Call the function in content_gen.py
        output_box.insert("end", f"{result}\n")
        output_box.insert("end", f"File uploaded: {file_path}\n")

def send_topic_to_api(topic):
    try:
        res = requests.post("http://127.0.0.1:5000/api/add_topic", json={"topic": topic}, timeout=5)
        if res.status_code == 200:
            print("✅ Sent to API:", topic)
        else:
            print("❌ API Error:", res.json())
    except Exception as e:
        print("❌ Could not reach API:", e)

def get_topics_from_api():
    try:
        res = requests.get("http://127.0.0.1:5000/api/get_topics", timeout=5)
        if res.status_code == 200:
            return res.json().get("topics", [])
        else:
            return ["Error fetching topics"]
    except Exception as e:
        return [f"API error: {e}"]
