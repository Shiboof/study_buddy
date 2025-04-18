import json
import os
from tkinter import filedialog, messagebox
uploaded_context = ""

TASK_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")

def upload_context_file(file_path):
    global uploaded_context
    try:
        with open(file_path, "r") as file:
            uploaded_context = file.read()
        return "File uploaded successfully and context stored."
    except Exception as e:
        return f"Error reading file: {str(e)}"

def get_uploaded_context():
    return uploaded_context

def save_study_data_to_file(study_data, filename="study_material.txt"):
    try:
        file_path = filedialog.asksaveasfilename(
            title="Save Study Material",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not file_path:
            return

        with open(file_path, "w") as file:
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

def add_task_to_file(task):
    tasks = get_all_tasks_from_file()
    tasks.append(task)
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f)

def get_all_tasks_from_file():
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, "r") as f:
        return json.load(f)