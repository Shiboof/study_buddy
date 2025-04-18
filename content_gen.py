import tkinter as tk
from tkinter import messagebox
from openai import OpenAI, OpenAIError, RateLimitError, APIConnectionError, AuthenticationError
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from api.storage import upload_context_file, get_uploaded_context
from pathlib import Path
import sys

# Dynamically locate the .env file
if getattr(sys, 'frozen', False):
    base_dir = Path(sys._MEIPASS)
else:
    base_dir = Path(__file__).resolve().parent

env_path = base_dir / ".env"
load_dotenv(dotenv_path=env_path)

client = OpenAI()

def call_openai_api(model, messages, max_tokens=500, temperature=0.7):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content
    except AuthenticationError:
        raise RuntimeError("Authentication failed. Please check your OpenAI API key.")
    except RateLimitError:
        raise RuntimeError("Rate limit exceeded. Please wait and try again later.")
    except APIConnectionError:
        raise RuntimeError("Failed to connect to OpenAI API. Please check your internet connection.")
    except OpenAIError as e:
        raise RuntimeError(f"An OpenAI API error occurred: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")

def generate_study_content(topic, output_box, study_data):
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, f"Generating study content for {topic}...\n")
    try:
        context = get_uploaded_context()
        messages = [
            {"role": "system", "content": "You are a helpful study assistant."},
            {"role": "user", "content": f"Use the following context:\n{context}\nGenerate a study summary for the topic '{topic}'."}
        ]
        summary = call_openai_api(model="gpt-3.5-turbo-0125", messages=messages)
        output_box.insert(tk.END, summary)
        study_data["content"] = summary
    except RuntimeError as e:
            error_msg = f"Error generating study content: {e}"
            output_box.insert(tk.END, error_msg)
            messagebox.showerror("Error", error_msg)
    except Exception as e:
        error_msg = f"An unexpected error occurred: {e}"
        output_box.insert(tk.END, error_msg)
        messagebox.showerror("Error", error_msg)
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
    except RuntimeError as e:
        error_msg = f"Error generating flashcards: {e}"
        output_box.insert(tk.END, error_msg)
        messagebox.showerror("Error", error_msg)
    except Exception as e:
        error_msg = f"An unexpected error occurred: {e}"
        output_box.insert(tk.END, error_msg)
        messagebox.showerror("Error", error_msg)

def run_quiz(topic, output_box, study_data):
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, f"Generating quiz for {topic}...\n")
    try:
        context = get_uploaded_context()
        messages = [
            {"role": "system", "content": "You are a study assistant that creates quizzes."},
            {"role": "user", "content": f"Use the following context:\n{context}\nGenerate 20 question quizzes about {topic}, formatted as 'Q: ... A: A, B, C, D'"}
        ]
        quiz = call_openai_api(model="gpt-3.5-turbo", messages=messages)
        output_box.insert(tk.END, quiz)
        study_data["quiz"] = quiz
    except RuntimeError as e:
        error_msg = f"Error generating flashcards: {e}"
        output_box.insert(tk.END, error_msg)
    except Exception as e:
        error_msg = f"Error generating quiz: {e}"
        output_box.insert(tk.END, error_msg)
        messagebox.showerror("Error", error_msg)

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

            study_data["test"] = f"{mc_questions}\n{fill_questions}"
    except RuntimeError as e:
        error_msg = f"Error generating flashcards: {e}"
        output_box.insert(tk.END, error_msg)
    except Exception as e:
        error_msg = f"Error generating test: {e}"
        output_box.insert(tk.END, error_msg)
        messagebox.showerror("Error", error_msg)

def generate_answers(output_box, study_data):
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "Generating answers for quizzes and tests...\n")
    try:
        if not study_data.get("quiz") and not study_data.get("test"):
            raise Exception("No quiz or test data found to generate answers.")

        answers = ""

        if study_data.get("quiz"):
            output_box.insert(tk.END, "Generating answers for the quiz...\n")
            quiz_questions = study_data["quiz"].split("\n")
            quiz_answers = []
            for question in quiz_questions:
                if question.strip():
                    quiz_messages = [
                        {"role": "user", "content": f"Provide an answer for the following question:\n{question}"}
                    ]
                    answer = call_openai_api(model="gpt-3.5-turbo", messages=quiz_messages)
                    quiz_answers.append(f"{question}\nAnswer: {answer.strip()}\n")
            answers += "Quiz Answers:\n" + "\n".join(quiz_answers) + "\n\n"

        if study_data.get("test"):
            output_box.insert(tk.END, "Generating answers for the test...\n")
            test_questions = study_data["test"].split("\n")
            test_answers = []
            for question in test_questions:
                if question.strip():
                    test_messages = [
                        {"role": "user", "content": f"Provide an answer for the following question:\n{question}"}
                    ]
                    answer = call_openai_api(model="gpt-3.5-turbo", messages=test_messages)
                    test_answers.append(f"{question}\nAnswer: {answer.strip()}\n")
            answers += "Test Answers:\n" + "\n".join(test_answers) + "\n\n"

        study_data["answers"] = answers
        output_box.insert(tk.END, f"Answers:\n{answers}\n")
    except RuntimeError as e:
        error_msg = f"Error generating flashcards: {e}"
        output_box.insert(tk.END, error_msg)
    except Exception as e:
        error_msg = f"Error generating answers: {e}"
        output_box.insert(tk.END, error_msg)
        messagebox.showerror("Error", error_msg)
