import tkinter as tk
from tkinter import messagebox
from openai import OpenAI
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from storage import upload_context_file, get_uploaded_context

'''
file will handle the logic for generating study content, flashcards, and quizzes
gpt-3.5-turbo is used for generating study content, flashcards, and quizzes.
The OpenAI API is used to interact with the GPT-3.5 model.
'''

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_openai_api(model, messages, max_tokens=500, temperature=0.7):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise e

def generate_study_content(topic, output_box, study_data):
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, f"Generating study content for {topic}...\n")
    try:
        context = get_uploaded_context()
        messages = [
            {"role": "system", "content": "You are a helpful study assistant."},
            {"role": "user", "content": f"Use the following context:\n{context}\nGenerate a study summary for the topic '{topic}'."}
        ]
        # Call the OpenAI API to generate the study content
        summary = call_openai_api(model="gpt-3.5-turbo", messages=messages)
        output_box.insert(tk.END, summary)
        study_data["content"] = summary
    except Exception as e:
        output_box.insert(tk.END, "Error generating content: " + str(e))
        messagebox.showerror("Error", "Failed to generate study content. Please try again.")

def generate_flashcards(topic, output_box, study_data):
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, f"Generating flashcards for {topic}...\n")
    try:
        context = get_uploaded_context()
        messages = [
            {"role": "system", "content": "You are a study assistant that creates flashcards."},
            {"role": "user", "content": f"Use the following context:\n{context}\nGenerate 5 flashcards (Q&A pairs) about {topic}, formatted as 'Q: ... A: ...'"}
        ]
        flashcards = call_openai_api(model="gpt-3.5-turbo", messages=messages)
        output_box.insert(tk.END, f"\nFlashcards:\n{flashcards}")
        study_data["flashcards"] = flashcards
    except Exception as e:
        output_box.insert(tk.END, "Error generating flashcards: " + str(e))
        messagebox.showerror("Error", "Failed to generate flashcards. Please try again.")

def run_quiz(topic, output_box, study_data):
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, f"Generating quiz for {topic}...\n")
    try:
        context = get_uploaded_context()
        messages = [
            {"role": "system", "content": "You are a study assistant that creates quizzes."},
            {"role": "user", "content": f"Use the following context:\n{context}\nGenerate 20 question quizzes about {topic}, formatted as 'Q: ... A: A, B, C, D'"}
        ]
        # Call the OpenAI API to generate the quiz
        quiz = call_openai_api(model="gpt-3.5-turbo", messages=messages)
        output_box.insert(tk.END, quiz)
        study_data["quiz"] = quiz
    except Exception as e:
        output_box.insert(tk.END, "Error generating quiz: " + str(e))
        messagebox.showerror("Error", "Failed to generate quiz. Please try again.")

def run_test(topic, output_box, study_data):
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

            output_box.insert(tk.END, f"\nMultiple-Choice Questions:\n{mc_questions}\n")
            output_box.insert(tk.END, f"\nFill-in-the-Blank Questions:\n{fill_questions}\n")

            # Store the test in study_data
            study_data["test"] = f"{mc_questions}\n{fill_questions}"
    except Exception as e:
        output_box.insert(tk.END, "Error generating test: " + str(e))
        messagebox.showerror("Error", "Failed to generate test. Please try again.")
