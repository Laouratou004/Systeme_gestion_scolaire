from database import get_connection
from auth_manager import hash_password

def reset_and_setup():
    conn = get_connection()
    cursor = conn.cursor()

    # Vider les tables pour repartir à zéro
    cursor.execute("DELETE FROM Users")
    cursor.execute("DELETE FROM Students")
    cursor.execute("DELETE FROM Teachers")
    cursor.execute("DELETE FROM Subjects")

    # Créer l'administrateur proprement
    # Ordre : username, password_hash, role, email
    admin_data = ("admin", hash_password("admin123"), "Admin", "admin@groupe1.edu")
    cursor.execute("INSERT INTO Users (username, password_hash, role, email) VALUES (?,?,?,?)", admin_data)

    conn.commit()
    conn.close()
    print("Base de données réinitialisée avec succès !")

if __name__ == "__main__":
    reset_and_setup()