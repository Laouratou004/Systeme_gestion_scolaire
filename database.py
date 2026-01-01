import sqlite3

def get_connection():
    """Retourne une connexion à la base de données avec les clés étrangères activées"""
    conn = sqlite3.connect('gestion_scolaire.db')
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Initialise toutes les tables de la base de données"""
    conn = get_connection()
    cursor = conn.cursor()

    # Table Users - Table principale des utilisateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT CHECK(role IN ('Admin', 'Enseignant', 'Étudiant')) NOT NULL,
            email TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table Students - Fiches des étudiants (l'ID correspond à l'ID dans Users)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            id INTEGER PRIMARY KEY, 
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            birth_date TEXT,
            class_name TEXT,
            FOREIGN KEY (id) REFERENCES Users(id) ON DELETE CASCADE
        )
    ''')

    # Table Teachers - Fiches des enseignants (l'ID correspond à l'ID dans Users)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Teachers (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            specialty TEXT,
            class_name TEXT,
            FOREIGN KEY (id) REFERENCES Users(id) ON DELETE CASCADE
        )
    ''')

    # Table Subjects - Les matières enseignées
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            teacher_id INTEGER,
            class_name TEXT,
            FOREIGN KEY (teacher_id) REFERENCES Teachers(id) ON DELETE SET NULL
        )
    ''')
    
    # Table Grades - Les notes des étudiants
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            grade REAL CHECK(grade >= 0 AND grade <= 20),
            date TEXT,
            FOREIGN KEY (student_id) REFERENCES Students(id) ON DELETE CASCADE,
            FOREIGN KEY (subject_id) REFERENCES Subjects(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Base de données initialisée avec succès.")

if __name__ == "__main__":
    init_db()