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
        messagebox.showinfo("Success", f"Study material saved to '{file_path}'")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save study material: {str(e)}")

# def load_study_data_from_file(filename="study_material.txt"):
#     """Load the study data from a plain text file."""
#     try:
#         with open(filename, "r") as file:
#             lines = file.readlines()
        
#         # Parse the text file into sections
#         study_data = {"content": "", "flashcards": "", "quiz": ""}
#         current_section = None
#         for line in lines:
#             line = line.strip()
#             if line == "Study Content:":
#                 current_section = "content"
#             elif line == "Flashcards:":
#                 current_section = "flashcards"
#             elif line == "Quiz:":
#                 current_section = "quiz"
#             elif current_section:
#                 study_data[current_section] += line + "\n"
        
#         return study_data
#     except FileNotFoundError:
#         return {"content": "", "flashcards": "", "quiz": ""}
#     except Exception as e:
#         messagebox.showerror("Error", f"Failed to load study material: {str(e)}")
#         return {"content": "", "flashcards": "", "quiz": ""}