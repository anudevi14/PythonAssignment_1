import fitz  # PyMuPDF
import re
import sqlite3
from abc import ABC, abstractmethod

# Abstract Base Class for Questions
class Question(ABC):
    def __init__(self, text):
        self.text = text

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def save_to_db(self, cursor, question_type):
        pass


# Subclasses for Different Question Types
class SubjectiveQuestion(Question):
    def __init__(self, text):
        super().__init__(text)

    def display(self):
        print(f"Subjective Question: {self.text}")

    def save_to_db(self, cursor, question_type="Subjective"):
        cursor.execute(
            "INSERT INTO questions (question_text, question_type) VALUES (?, ?)",
            (self.text, question_type),
        )


class TrueFalseQuestion(Question):
    def __init__(self, text, options):
        super().__init__(text)
        self.options = options

    def display(self):
        print(f"True/False Question: {self.text}")
        for option in self.options:
            print(f"- {option}")

    def save_to_db(self, cursor, question_type="True/False"):
        options_str = ", ".join(self.options)
        cursor.execute(
            "INSERT INTO questions (question_text, options, question_type) VALUES (?, ?, ?)",
            (self.text, options_str, question_type),
        )


class MultipleChoiceQuestion(Question):
    def __init__(self, text, options):
        super().__init__(text)
        self.options = options

    def display(self):
        print(f"Multiple Choice Question: {self.text}")
        for option in self.options:
            print(f"- {option}")

    def save_to_db(self, cursor, question_type="Multiple Choice"):
        options_str = ", ".join(self.options)
        cursor.execute(
            "INSERT INTO questions (question_text, options, question_type) VALUES (?, ?, ?)",
            (self.text, options_str, question_type),
        )


# Function to classify and create question objects
def classify_question(question_text, options):
    if len(options) == 0:
        return SubjectiveQuestion(question_text)
    elif len(options) == 2 and set(options) == {"True", "False"}:
        return TrueFalseQuestion(question_text, options)
    else:
        return MultipleChoiceQuestion(question_text, options)


# Database setup
def setup_database():
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT,
            options TEXT,
            question_type TEXT
        )
        """
    )
    conn.commit()
    return conn, cursor


# PDF Parsing and Question Extraction
def extract_questions_from_pdf(pdf_path):
    question_pattern = re.compile(r"^\d+\.\s+(.*)")  # Matches numbered questions
    option_pattern = re.compile(r"^[A-D]\)\s+(.*)")  # Matches options
    questions = []

    try:
        document = fitz.open(pdf_path)
        current_question = None
        current_options = []

        for page in document:
            lines = page.get_text("text").split("\n")
            for line in lines:
                line = line.strip()

                # Match a question
                question_match = question_pattern.match(line)
                if question_match:
                    if current_question:  # Save previous question
                        questions.append((current_question, current_options))
                    current_question = question_match.group(1).strip()
                    current_options = []

                # Match an option
                option_match = option_pattern.match(line)
                if option_match:
                    current_options.append(option_match.group(1).strip())

            # Save the last question on the page
            if current_question:
                questions.append((current_question, current_options))

        document.close()
    except Exception as e:
        print(f"Error reading PDF: {e}")

    return questions


# Main Function
def main():
    pdf_path = "Questions.pdf"  # Replace with your PDF file path
    questions = extract_questions_from_pdf(pdf_path)

    if not questions:
        print("No questions found in the PDF.")
        return

    # Setup database
    conn, cursor = setup_database()

    for question_text, options in questions:
        question = classify_question(question_text, options)
        question.display()
        question.save_to_db(cursor)  # Save the question to the database

    # Commit changes and close the database connection
    conn.commit()
    conn.close()
    print("All questions have been saved to the database.")


if __name__ == "__main__":
    main()