import tkinter as tk
from tkinter import messagebox
from openai import OpenAI
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from storage import upload_context_file, get_uploaded_context
from pathlib import Path
import sys

'''
This file handles the logic for generating study content, flashcards, quizzes, and tests.
The OpenAI API is used to interact with the GPT-3.5 model.
'''

# Dynamically locate the .env file
if getattr(sys, 'frozen', False):  # Check if running as a PyInstaller bundle
    base_dir = Path(sys._MEIPASS)  # Temporary folder for PyInstaller
else:
    base_dir = Path(__file__).resolve().parent

env_path = base_dir / ".env"
load_dotenv(dotenv_path=env_path)

# Set the OpenAI API key
client = OpenAI()

def call_openai_api(model, messages, max_tokens=500, temperature=0.7):
    """Call the OpenAI API using OpenAI SDK >=1.0.0"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def generate_study_content(topic, output_box, study_data):
    """Generate study content for the given topic."""
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, f"Generating study content for {topic}...\n")
    try:
        context = get_uploaded_context()
        messages = [
            {"role": "system", "content": "You are a helpful study assistant."},
            {"role": "user", "content": f"Use the following context:\n{context}\nGenerate a study summary for the topic '{topic}'."}
        ]
        # Call the OpenAI API to generate the study content
        summary = call_openai_api(model="gpt-3.5-turbo-0125", messages=messages)
        if summary.startswith("Error:"):
            raise Exception(summary)
        output_box.insert(tk.END, summary)
        study_data["content"] = summary
    except Exception as e:
        output_box.insert(tk.END, f"{e}")
        messagebox.showerror("Error", str(e))

def generate_flashcards(topic, output_box, study_data):
    """Generate flashcards for the given topic."""
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, f"Generating flashcards for {topic}...\n")
    try:
        context = get_uploaded_context()
        messages = [
            {"role": "system", "content": "You are a study assistant that creates flashcards."},
            {"role": "user", "content": f"Use the following context:\n{context}\nGenerate 5 flashcards (Q&A pairs) about {topic}, formatted as 'Q: ... A: ...'"}
        ]
        flashcards = call_openai_api(model="gpt-3.5-turbo", messages=messages)
        if flashcards.startswith("Error:"):
            raise Exception(flashcards)
        output_box.insert(tk.END, f"\nFlashcards:\n{flashcards}")
        study_data["flashcards"] = flashcards
    except Exception as e:
        output_box.insert(tk.END, f"{e}")
        messagebox.showerror("Error", str(e))

def run_quiz(topic, output_box, study_data):
    """Generate a quiz for the given topic."""
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, f"Generating quiz for {topic}...\n")
    try:
        context = get_uploaded_context()
        messages = [
            {"role": "system", "content": "You are a study assistant that creates quizzes."},
            {"role": "user", "content": f"Use the following context:\n{context}\nGenerate 20 question quizzes about {topic}, formatted as 'Q: ... A: A, B, C, D'"}
        ]
        quiz = call_openai_api(model="gpt-3.5-turbo", messages=messages)
        if quiz.startswith("Error:"):
            raise Exception(quiz)
        output_box.insert(tk.END, quiz)
        study_data["quiz"] = quiz
    except Exception as e:
        output_box.insert(tk.END, f"{e}")
        messagebox.showerror("Error", str(e))

def run_test(topic, output_box, study_data):
    """Generate a test for the given topic."""
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, f"Generating test for {topic}...\n")

    def generate_mc_questions():
        context = get_uploaded_context()
        messages_mc = [
            {"role": "system", "content": "You are a study assistant that creates structured tests."},
            {"role": "user", "content": (
                f"Use the following context:\n{context}\nCreate 30 multiple-choice questions about the topic '{topic}'.\n"
                "Each question should have 4 options labeled A, B, C, D.\n"
                "Format the questions like this:\n"
                "Q1: What is ...?\n"
                "A. Option 1\n"
                "B. Option 2\n"
                "C. Option 3\n"
                "D. Option 4\n"
            )}
        ]
        return call_openai_api(model="gpt-3.5-turbo", messages=messages_mc, max_tokens=1500)

    def generate_fill_questions():
        context = get_uploaded_context()
        messages_fill = [
            {"role": "system", "content": "You are a study assistant that creates structured tests."},
            {"role": "user", "content": (
                f"Use the following context:\n{context}\nCreate 30 fill-in-the-blank questions about the topic '{topic}'.\n"
                "Format the questions like this:\n"
                "Q31: _____ is the capital of France.\n"
            )}
        ]
        return call_openai_api(model="gpt-3.5-turbo", messages=messages_fill, max_tokens=1000)

    try:
        with ThreadPoolExecutor() as executor:
            mc_future = executor.submit(generate_mc_questions)
            fill_future = executor.submit(generate_fill_questions)

            mc_questions = mc_future.result()
            fill_questions = fill_future.result()

            if mc_questions.startswith("Error:") or fill_questions.startswith("Error:"):
                raise Exception(f"{mc_questions}\n{fill_questions}")

            output_box.insert(tk.END, f"\nMultiple-Choice Questions:\n{mc_questions}\n")
            output_box.insert(tk.END, f"\nFill-in-the-Blank Questions:\n{fill_questions}\n")

            # Store the test in study_data
            study_data["test"] = f"{mc_questions}\n{fill_questions}"
    except Exception as e:
        output_box.insert(tk.END, f"{e}")
        messagebox.showerror("Error", str(e))
