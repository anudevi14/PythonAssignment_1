import fitz  # PyMuPDF
import re
import sqlite3
import logging

# Set up logging
logging.basicConfig(filename="pdf_extraction_errors.log", level=logging.ERROR)

# Database setup
db_path = "questions.db"

# Function to handle database operations safely
def connect_to_db():
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")
        return None

# Function to create the table if it doesn't exist
def create_table(cursor):
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name TEXT,
            chapter_name TEXT,
            question_text TEXT,
            answer_options TEXT,
            correct_answer TEXT
        )
        """)
    except sqlite3.Error as e:
        logging.error(f"Error creating table: {e}")

# Function to insert data into the database
def insert_data(cursor, subject_name, chapter_name, question_text, formatted_options, correct_answer):
    try:
        cursor.execute("""
            INSERT INTO questions (subject_name, chapter_name, question_text, answer_options, correct_answer)
            VALUES (?, ?, ?, ?, ?)
        """, (subject_name, chapter_name, question_text.strip(), formatted_options, correct_answer))
        cursor.connection.commit()  # Commit after the insert
    except sqlite3.Error as e:
        logging.error(f"Error inserting data: {e}")

# Initialize the database connection
conn = connect_to_db()
if conn is None:
    print("Database connection failed. Exiting program.")
    exit()

cursor = conn.cursor()

# Create the table if it doesn't exist
create_table(cursor)

# Define regular expressions for patterns
chapter_pattern = re.compile(r"^Chapter\s+\d+:\s+(.*)")  # Detects chapter titles
question_pattern = re.compile(r"^\d+\.\s+(.*)")          # Detects numbered questions
option_pattern = re.compile(r"^([A-D])\)\s+(.*)")        # Detects options and labels
answer_pattern = re.compile(r"^Answer:\s*(.*)")          # Detects answers

# Initialize storage
current_chapter = None
current_question = None
current_options = []
current_answer = None
multi_line_question = False  # Tracks multi-line questions

# PDF file path
pdf_path = "Chemistry Questions.pdf"
document = fitz.open(pdf_path)

# Process each page in the PDF
for page_num in range(len(document)):
    page = document[page_num]
    text = page.get_text("text")  # Extract text
    lines = text.split("\n")      # Split into lines

    # Process each line
    for line in lines:
        line = line.strip()  # Remove extra spaces

        chapter_match = chapter_pattern.match(line)
        question_match = question_pattern.match(line)
        option_match = option_pattern.match(line)
        answer_match = answer_pattern.match(line)

        if chapter_match:
            # Save the previous question-answer pair if any
            if current_question:
                formatted_options = " ".join(current_options)
                insert_data(cursor, "Chemistry", current_chapter, current_question, formatted_options, current_answer)

            # Start a new chapter
            current_chapter = chapter_match.group(1).strip()
            current_question = None
            current_options = []
            current_answer = None

        elif question_match:
            # Save the current question-answer pair before starting a new question
            if current_question:
                formatted_options = " ".join(current_options)
                insert_data(cursor, "Chemistry", current_chapter, current_question, formatted_options, current_answer)

            # Start a new question
            current_question = question_match.group(1).strip()
            current_options = []
            current_answer = None
            multi_line_question = True  # Multi-line question expected

        elif option_match:
            # Add the option to the current options list, keeping the label (A), (B), etc.
            option_label = option_match.group(1).strip()
            option_text = option_match.group(2).strip()
            current_options.append(f"{option_label}) {option_text}")

            multi_line_question = False  # Options indicate the question has ended

        elif answer_match:
            # Capture the answer for the current question
            current_answer = answer_match.group(1).strip()
            multi_line_question = False  # Answer indicates the question has ended

        elif multi_line_question:
            # Append additional lines to the current question text
            current_question += " " + line

    # Ensure the last question-answer pair is saved after the last page
    if current_chapter and current_question:
        formatted_options = " ".join(current_options)
        insert_data(cursor, "Chemistry", current_chapter, current_question, formatted_options, current_answer)

# Close the database connection
conn.close()

print("Data extraction and storage completed successfully.")