import sqlite3
import os

class Database:
    def __init__(self, db_name="scolaire.db"):
        # On définit le chemin pour que la DB soit créée à la racine du projet
        self.db_path = os.path.join(os.path.dirname(__file__), "../../", db_name)
        self.init_db()

    def get_connection(self):
        """Établit une connexion et active les contraintes de clés étrangères."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_db(self):
        """Crée les tables si elles n'existent pas."""
        commands = [
            # 1. Table Users (Identifiants techniques uniquement)
            """
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT CHECK(role IN ('Admin', 'Enseignant', 'Étudiant')) NOT NULL,
                email TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """,
            # 2. Table Students (Profil métier)
            """
            CREATE TABLE IF NOT EXISTS Students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                birth_date TEXT,
                class TEXT,
                FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
            );
            """,
            # 3. Table Teachers (Profil métier)
            """
            CREATE TABLE IF NOT EXISTS Teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                specialty TEXT,
                FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
            );
            """,
            # Table Subjects
            """
            CREATE TABLE IF NOT EXISTS Subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                teacher_id INTEGER,
                FOREIGN KEY (teacher_id) REFERENCES Teachers(id) ON DELETE SET NULL
            );
            """,
            #  Table Grades
            """
            CREATE TABLE IF NOT EXISTS Grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                grade REAL NOT NULL,
                date TEXT DEFAULT (date('now')),
                FOREIGN KEY (student_id) REFERENCES Students(id) ON DELETE CASCADE,
                FOREIGN KEY (subject_id) REFERENCES Subjects(id) ON DELETE CASCADE
            );
            """
        ]
        
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            for command in commands:
                cursor.execute(command)
            conn.commit()
            print(" Base de données initialisée avec succès.")
        except sqlite3.Error as e:
            print(f" Erreur lors de l'initialisation : {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    db = Database()