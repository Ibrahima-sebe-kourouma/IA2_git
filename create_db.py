import sqlite3

def create_db():
    conn = sqlite3.connect('users.db')  # Crée la base de données si elle n'existe pas
    cursor = conn.cursor()
    
    # Créer une table pour stocker les utilisateurs
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        email TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        photo BLOB
                    )''')
    
    conn.commit()
    conn.close()

# Appelle la fonction pour créer la base de données et la table
create_db()
