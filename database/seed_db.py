import sqlite3
import hashlib
from database import get_connection, create_tables


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def reset_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Grades")
    cursor.execute("DELETE FROM Subjects")
    cursor.execute("DELETE FROM Students")
    cursor.execute("DELETE FROM Teachers")
    cursor.execute("DELETE FROM Users")

    conn.commit()
    conn.close()


def create_admin():
    conn = get_connection()
    cursor = conn.cursor()

    username = "admin"
    password = hash_password("admin123")
    role = "Admin"
    email = "admin@school.com"

    cursor.execute("""
    INSERT INTO Users (username, password, role, email)
    VALUES (?, ?, ?, ?)
    """, (username, password, role, email))

    conn.commit()
    conn.close()


if _name_ == "_main_":
    create_tables()
    reset_database()
    create_admin()
    print("Base réinitialisée. Administrateur créé (admin / admin123).")