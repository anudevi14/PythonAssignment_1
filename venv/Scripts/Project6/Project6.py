import sqlite3

# Database path
db_path = "questions.db"

def connect_to_db():
    """
    Connect to the SQLite database.
    """
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        exit(1)  # Exit the program if the connection fails

def fetch_questions_by_chapter(cursor, chapter_name):
    """
    Fetch all questions for a specific chapter from the database.
    """
    try:
        cursor.execute("""
            SELECT question_text, answer_options, correct_answer 
            FROM questions 
            WHERE chapter_name = ?
        """, (chapter_name,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error fetching questions: {e}")
        return []

def extract_questions():
    """
    Main function to take chapter name as input and retrieve questions.
    """
    # Get chapter name from the user
    chapter_name = input("Enter the chapter name: ").strip()

    # Connect to the database
    conn = connect_to_db()
    cursor = conn.cursor()

    # Fetch questions for the given chapter
    questions = fetch_questions_by_chapter(cursor, chapter_name)

    if questions:
        print(f"\nQuestions from chapter: {chapter_name}\n")
        for idx, (question_text, answer_options, correct_answer) in enumerate(questions, start=1):
            print(f"{idx}. {question_text}")
            print(f"   Options: {answer_options}")
            print(f"   Correct Answer: {correct_answer}\n")
    else:
        print(f"No questions found for the chapter: {chapter_name}")

    # Close the database connection
    conn.close()

extract_questions()