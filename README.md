# Study Buddy

**Study Buddy** is a full-stack Python application that helps students generate study materials, quizzes, flashcards, and tests from any topic — powered by OpenAI's GPT models. The app includes a responsive web interface, a Flask-based backend with a clean RESTful API, and an optional desktop GUI built with CustomTkinter.

---

## Features

1. **Generate Study Content**  
   Enter a topic and generate detailed study content to help you learn effectively.

2. **Show Flashcards**  
   Create flashcards based on the entered topic to aid in memorization and quick review.

3. **Generate Quiz**  
   Generate quizzes to test your knowledge on the entered topic.

4. **Generate Test**  
   Create comprehensive tests for a deeper evaluation of your understanding.

5. **Upload Context File**  
   Upload a file containing additional context or information to enhance the generated study materials.

6. **Download Content**  
   Save the generated study materials, flashcards, quizzes, or tests to your local system for offline use.

7. **RESTful API**  
   Expose the core functionality via a RESTful API for integration with other systems or applications.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Shiboof/study_buddy.git
   cd study_buddy
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application from PowerShell:
   ```bash
   $env:RUN_GUI=1; python .\main.py
   ```

---

## Usage

Launch the application by running main.py.

Enter a topic in the input field.

Use the buttons to:

- Generate study content.
- Create flashcards.
- Generate quizzes or tests.
- Upload additional context files.
- Download the generated content.

View the output in the designated output area.

---

## Technologies Used

- Python: Core programming language.
- CustomTkinter: For building the modern GUI.
- Pillow: For handling images.
- Requests: For checking updates via GitHub API.

---

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```

3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```

4. Push to the branch:
   ```bash
   git push origin feature-name
   ```

5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact

For questions or feedback, feel free to reach out:

- GitHub: Shiboof
- Email: rogersbuilt@pm.me

---

## Acknowledgments

Special thanks to the developers of customtkinter and the Python community for their amazing tools and support!
