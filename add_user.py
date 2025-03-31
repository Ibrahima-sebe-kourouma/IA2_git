import sqlite3
import hashlib

def hash_password(password):
    """Hache le mot de passe avec SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()



def add_user(username, email, password):
    """Ajoute un utilisateur sans photo."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Vérifier si l'utilisateur existe déjà
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        print("⚠️ Utilisateur déjà existant.")
        conn.close()
        return
    
    # Ajouter l'utilisateur
    password_hash = hash_password(password)
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                   (username, email, password_hash))
    
    conn.commit()
    conn.close()
    print(f"✅ Utilisateur {username} ajouté avec succès (sans photo).")

def add_user_avec_photo(username, email, password, photo_path):
    """Ajoute un utilisateur avec une photo."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Vérifier si l'utilisateur existe déjà
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        print("⚠️ Utilisateur déjà existant.")
        conn.close()
        return
    
    # Lire la photo en mode binaire
    with open(photo_path, 'rb') as file:
        photo_data = file.read()
    
    # Ajouter l'utilisateur avec photo
    password_hash = hash_password(password)
    cursor.execute("INSERT INTO users (username, email, password, photo) VALUES (?, ?, ?, ?)", 
                   (username, email, password_hash, photo_data))
    
    conn.commit()
    conn.close()
    print(f"✅ Utilisateur {username} ajouté avec succès (avec photo).")

