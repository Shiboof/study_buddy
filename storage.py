import json
from tkinter import messagebox, filedialog

'''
File will handle saving and loading study data
'''

uploaded_context = ""  # Global variable to store the uploaded file content

def upload_context_file(file_path):
    """Read the content of the uploaded file and store it for context."""
    global uploaded_context
    try:
        with open(file_path, "r") as file:
            uploaded_context = file.read()
        return "File uploaded successfully and context stored."
    except Exception as e:
        return f"Error reading file: {str(e)}"

def get_uploaded_context():
    """Return the uploaded context to be used in other functions."""
    return uploaded_context

def save_study_data_to_file(study_data, filename="study_material.txt"):
    """Save the study data to a plain text file."""
    try:
        # Open a file dialog for the user to choose
        file_path = filedialog.asksaveasfilename(
            title="Save Study Material",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not file_path:
            return

        # Write the study data to the selected file
        with open(file_path, "w") as file:
            # Write each section of the study data to the file
            file.write("Study Content:\n")
            file.write(study_data.get("content", "") + "\n\n")
            file.write("Flashcards:\n")
            file.write(study_data.get("flashcards", "") + "\n\n")
            file.write("Quiz:\n")
            file.write(study_data.get("quiz", "") + "\n\n")
            file.write("Test:\n")
            file.write(study_data.get("test", "") + "\n\n")
            file.write("Answers:\n")
            file.write(study_data.get("answers", "") + "\n\n")
        messagebox.showinfo("Success", f"Study material saved to '{file_path}'")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save study material: {str(e)}")

