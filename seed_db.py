from database import init_db, get_connection
from auth_manager import hash_password

def seed():
    # 1. On s'assure que les tables existent
    init_db()
    
    conn = get_connection()
    cursor = conn.cursor()

    print("Nettoyage de la base de données...")
    # On vide les tables pour repartir sur une base propre
    # L'ordre est important à cause des clés étrangères
    cursor.execute("DELETE FROM Grades")
    cursor.execute("DELETE FROM Subjects")
    cursor.execute("DELETE FROM Teachers")
    cursor.execute("DELETE FROM Students")
    cursor.execute("DELETE FROM Users")

    print("Création du Super-Administrateur...")

    # Données de l'administrateur unique
    # Ordre des champs : username, password (en clair), role, email
    admin_user = 'admin'
    admin_pass = 'admin123'
    admin_role = 'Admin'
    admin_email = 'admin@groupe1.edu'

    # Hachage du mot de passe
    h_pass = hash_password(admin_pass)

    # Insertion dans la table Users (Attention à l'ordre des colonnes !)
    cursor.execute('''
        INSERT INTO Users (username, password_hash, role, email)
        VALUES (?, ?, ?, ?)
    ''', (admin_user, h_pass, admin_role, admin_email))

    conn.commit()
    conn.close()
    
    print("--- Initialisation terminée avec succès ! ---")
    print("Compte administrateur unique créé :")
    print(f"  - Pseudo : {admin_user}")
    print(f"  - Passe  : {admin_pass}")

if __name__ == "__main__":
    seed()