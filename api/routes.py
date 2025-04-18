from flask import request, jsonify
from api import app
from api.storage import add_topic_to_file, get_all_topics_from_file
from flask import send_from_directory
from flask import request

@app.route("/api/add_task", methods=["POST"])
def add_task():
    data = request.json
    task = data.get("task")
    if not task:
        return jsonify({"error": "Task is required"}), 400
    add_topic_to_file(task)
    return jsonify({"message": "Task added", "task": task})

@app.route("/api/get_tasks", methods=["GET"])
def get_tasks():
    tasks = get_all_topics_from_file()
    return jsonify({"tasks": tasks})

@app.route("/api/add_topic", methods=["POST"])
def add_topic():
    data = request.json
    topic = data.get("topic")
    if not topic:
        return jsonify({"error": "Topic is required"}), 400
    add_topic_to_file(topic)
    return jsonify({"message": "Topic added", "topic": topic})

@app.route("/api/get_topics", methods=["GET"])
def get_topics():
    topics = get_all_topics_from_file()
    return jsonify({"topics": topics})

@app.route('/flashcards')
def flashcards():
    return send_from_directory(os.path.join(os.getcwd(), "public"), "flashcards.html")

@app.route('/quiz')
def quiz():
    return send_from_directory(os.path.join(os.getcwd(), "public"), "quiz.html")

@app.route('/test')
def test():
    return send_from_directory(os.path.join(os.getcwd(), "public"), "test.html")

class MockText:
    """A mock object to mimic tkinter.Text behavior for capturing output."""
    def __init__(self):
        self.output = []

    def insert(self, index, text):
        self.output.append(text)

    def delete(self, a, b):
        self.output = []

    def getvalue(self):
        return "".join(self.output)


@app.route("/api/flashcards")
def api_flashcards():
    topic = request.args.get("topic", "")
    if not topic:
        return "Missing topic", 400

    from content_gen import generate_flashcards

    fake_box = MockText()  # Use the mock object instead of tk.Text
    study_data = {}
    generate_flashcards(topic, fake_box, study_data)
    return fake_box.getvalue()


@app.route("/api/quiz")
def api_quiz():
    topic = request.args.get("topic", "")
    if not topic:
        return "Missing topic", 400

    from content_gen import run_quiz

    fake_box = MockText()  # Use the mock object instead of tk.Text
    study_data = {}
    run_quiz(topic, fake_box, study_data)
    return fake_box.getvalue()


@app.route("/api/test")
def api_test():
    topic = request.args.get("topic", "")
    if not topic:
        return "Missing topic", 400

    from content_gen import run_test

    fake_box = MockText()  # Use the mock object instead of tk.Text
    study_data = {}
    run_test(topic, fake_box, study_data)
    return fake_box.getvalue()

import os

@app.route("/")
def serve_homepage():
    return send_from_directory(os.path.join(os.getcwd(), "public"), "index.html")