import customtkinter as ctk
from tkinter import filedialog
from content_gen import generate_study_content, generate_flashcards, run_quiz, run_test, upload_context_file
from storage import save_study_data_to_file
from PIL import Image, ImageTk  # Import Pillow for image resizing

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

    # Load and resize the moon image using CTkImage
    moon_image_path = "assets/moon.png"  # Path to moon image
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

    # Button Frame
    button_frame = ctk.CTkFrame(root)
    button_frame.pack(pady=10)

    # Create buttons using ctk.CTkButton
    buttons = []
    buttons.append(ctk.CTkButton(button_frame, text="Generate Study Content", 
                                 command=lambda: generate_study_content(entry.get(), output_box, study_data), 
                                 fg_color="blue", hover_color="darkblue", width=200, height=40, corner_radius=10))
    buttons.append(ctk.CTkButton(button_frame, text="Show Flashcards", 
                                 command=lambda: generate_flashcards(entry.get(), output_box, study_data), 
                                 fg_color="green", hover_color="darkgreen", width=200, height=40, corner_radius=10))
    buttons.append(ctk.CTkButton(button_frame, text="Generate Quiz", 
                                 command=lambda: run_quiz(entry.get(), output_box, study_data), 
                                 fg_color="orange", hover_color="gold", width=200, height=40, corner_radius=10))
    buttons.append(ctk.CTkButton(button_frame, text="Generate Test", 
                                 command=lambda: run_test(entry.get(), output_box, study_data), 
                                 fg_color="orange", hover_color="gold", width=200, height=40, corner_radius=10))
    buttons.append(ctk.CTkButton(button_frame, text="Upload Context File", 
                                 command=lambda: upload_file(output_box), 
                                 fg_color="red", hover_color="darkred", width=200, height=40, corner_radius=10))
    buttons.append(ctk.CTkButton(button_frame, text="Download Content", 
                                 command=lambda: save_study_data_to_file(study_data), 
                                 fg_color="coral", hover_color="darkred", width=200, height=40, corner_radius=10))

    # Arrange buttons in a grid
    for i, button in enumerate(buttons):
        button.grid(row=i // 2, column=i % 2, padx=10, pady=10)

    # Output Frame
    output_frame = ctk.CTkFrame(root)
    output_frame.pack(pady=10, padx=20, fill="both", expand=True)

    output_label = ctk.CTkLabel(output_frame, text="Output:", font=("Helvetica", 12))
    output_label.pack(anchor="w")

    # Add a scrollbar to the output box
    output_scrollbar = ctk.CTkScrollbar(output_frame)
    output_scrollbar.pack(side="right", fill="y")

    global output_box
    output_box = ctk.CTkTextbox(output_frame, height=15, width=70, font=("Helvetica", 10), yscrollcommand=output_scrollbar.set)
    output_box.pack(side="left", fill="both", expand=True)
    output_scrollbar.configure(command=output_box.yview)

def upload_file(output_box):
    """Open a file dialog to upload a file and store its content."""
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    if file_path:
        result = upload_context_file(file_path)  # Call the function in content_gen.py
        output_box.insert("end", f"{result}\n")

# Create root window
root = ctk.CTk()
root.title("Study Buddy")
root.geometry("1000x600")

# Configure resizing behavior
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)

def main():
    setup_ui(root)
    root.mainloop()

if __name__ == "__main__":
    main()

