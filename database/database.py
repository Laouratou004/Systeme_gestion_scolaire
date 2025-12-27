import sqlite3

DB_NAME = "school.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")  
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Table Users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('Admin', 'Enseignant', 'Étudiant')) NOT NULL,
        email TEXT UNIQUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Table Students
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        birth_date DATE,
        class TEXT
    )
    """)

    # Table Teachers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        specialty TEXT
    )
    """)

    # Table Subjects
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        teacher_id INTEGER NOT NULL,
        FOREIGN KEY (teacher_id) REFERENCES Teachers(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
    )
    """)

    # Table Grades
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        subject_id INTEGER NOT NULL,
        grade REAL CHECK(grade >= 0 AND grade <= 20),
        date DATE,
        FOREIGN KEY (student_id) REFERENCES Students(id)
        ON DELETE CASCADE,
        FOREIGN KEY (subject_id) REFERENCES Subjects(id)
        ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Base de données et tables créées avec succès.")