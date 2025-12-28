import sys
import os
import hashlib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import get_connection
from src.models.schemas import User

def hash_password(password):
    """Hash un mot de passe avec SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    """
    Authentifie un utilisateur
    Args:
        username (str): Nom d'utilisateur
        password (str): Mot de passe en clair
    Returns:
        User: Objet User si authentification réussie, None sinon
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    hashed_password = hash_password(password)
    cursor.execute("""
        SELECT id, username, password, role, email, created_at 
        FROM Users 
        WHERE username=? AND password=?
    """, (username, hashed_password))
    
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return User(
            id=user_data[0],
            username=user_data[1],
            password_hash=user_data[2],
            role=user_data[3],
            email=user_data[4],
            created_at=user_data[5]
        )
    return None

def create_user(username, password, role, email):
    """
    Crée un nouvel utilisateur
    Args:
        username (str): Nom d'utilisateur
        password (str): Mot de passe en clair
        role (str): 'Admin', 'Enseignant' ou 'Étudiant'
        email (str): Email de l'utilisateur
    Returns:
        bool: True si création réussie, False sinon
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        hashed_password = hash_password(password)
        cursor.execute("""
            INSERT INTO Users (username, password, role, email)
            VALUES (?, ?, ?, ?)
        """, (username, hashed_password, role, email))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erreur lors de la création de l'utilisateur: {e}")
        return False

def get_user_by_id(user_id):
    """
    Récupère un utilisateur par son ID
    Args:
        user_id (int): ID de l'utilisateur
    Returns:
        User: Objet User si trouvé, None sinon
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, username, password, role, email, created_at 
        FROM Users 
        WHERE id=?
    """, (user_id,))
    
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return User(
            id=user_data[0],
            username=user_data[1],
            password_hash=user_data[2],
            role=user_data[3],
            email=user_data[4],
            created_at=user_data[5]
        )
    return None

def get_all_users():
    """
    Récupère tous les utilisateurs
    Returns:
        list[User]: Liste des objets User
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, username, password, role, email, created_at 
        FROM Users
    """)
    
    users_data = cursor.fetchall()
    conn.close()
    
    users = []
    for user_data in users_data:
        users.append(User(
            id=user_data[0],
            username=user_data[1],
            password_hash=user_data[2],
            role=user_data[3],
            email=user_data[4],
            created_at=user_data[5]
        ))
    
    return users

def update_user(user_id, username=None, password=None, role=None, email=None):
    """
    Met à jour un utilisateur
    Args:
        user_id (int): ID de l'utilisateur
        username (str, optional): Nouveau nom d'utilisateur
        password (str, optional): Nouveau mot de passe
        role (str, optional): Nouveau rôle
        email (str, optional): Nouvel email
    Returns:
        bool: True si mise à jour réussie, False sinon
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if username:
            updates.append("username=?")
            params.append(username)
        if password:
            updates.append("password=?")
            params.append(hash_password(password))
        if role:
            updates.append("role=?")
            params.append(role)
        if email:
            updates.append("email=?")
            params.append(email)
        
        if not updates:
            return False
        
        params.append(user_id)
        query = f"UPDATE Users SET {', '.join(updates)} WHERE id=?"
        
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour: {e}")
        return False

def delete_user(user_id):
    """
    Supprime un utilisateur
    Args:
        user_id (int): ID de l'utilisateur
    Returns:
        bool: True si suppression réussie, False sinon
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM Users WHERE id=?", (user_id,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erreur lors de la suppression: {e}")
        return False

# Test du module
if __name__ == "__main__":
    print("=== Test du module d'authentification ===\n")
    
    # Test de connexion admin
    print("Test de connexion avec admin...")
    user = authenticate("admin", "admin123")
    
    if user:
        print(f"✓ Connexion réussie!")
        print(f"  Username: {user.username}")
        print(f"  Role: {user.role}")
        print(f"  Email: {user.email}")
    else:
        print("✗ Échec de connexion")
    
    # Test de connexion échouée
    print("\nTest de connexion avec mauvais mot de passe...")
    user = authenticate("admin", "wrong_password")
    if user:
        print("✗ Erreur: connexion réussie avec mauvais mot de passe")
    else:
        print("✓ Connexion refusée comme prévu")