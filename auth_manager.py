import hashlib
from database import get_connection

def hash_password(password):
    """
    Hash un mot de passe avec SHA-256.
    Transforme une chaîne de caractères en un hash hexadécimal de 64 caractères.
    """
    msg_uint8 = password.encode('utf-8')
    hash_obj = hashlib.sha256(msg_uint8)
    return hash_obj.hexdigest()

def verify_password(password, password_hash):
    """
    Vérifie si un mot de passe correspond au hash stocké.
    Retourne True si le mot de passe est correct, False sinon.
    """
    return hash_password(password) == password_hash

def verify_login(username, password):
    """
    Vérifie les identifiants dans la base de données.
    Retourne un tuple (user_id, role) si succès, sinon None.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # On hache le mot de passe saisi pour le comparer à celui en base
        password_hash = hash_password(password)
        
        query = "SELECT id, role FROM Users WHERE username = ? AND password_hash = ?"
        cursor.execute(query, (username, password_hash))
        result = cursor.fetchone()
        
        if result:
            return result  # Retourne (id, role) : ex: (1, 'Admin')
        return None
        
    except Exception as e:
        print(f"Erreur lors de la vérification : {e}")
        return None
    finally:
        conn.close()

def create_user(username, password, role, email):
    """
    Fonction utilitaire pour ajouter un utilisateur (utile pour l'Admin).
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    password_hash = hash_password(password)
    
    try:
        cursor.execute('''
            INSERT INTO Users (username, password_hash, role, email)
            VALUES (?, ?, ?, ?)
        ''', (username, password_hash, role, email))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la création de l'utilisateur : {e}")
        return False
    finally:
        conn.close()