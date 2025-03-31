import sqlite3

def delete_user(username, email):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Créer la table des utilisateurs si elle n'existe pas (assuré pour la gestion globale de la base)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # Vérifier si l'utilisateur existe avec le nom d'utilisateur et l'email
    cursor.execute("SELECT * FROM users WHERE username = ? AND email = ?", (username, email))
    user = cursor.fetchone()

    if user:
        # L'utilisateur existe, on peut le supprimer
        cursor.execute("DELETE FROM users WHERE username = ? AND email = ?", (username, email))
        conn.commit()
        print(f"Utilisateur '{username}' avec l'email '{email}' supprimé avec succès.")
    else:
        print(f"Aucun utilisateur trouvé avec le nom d'utilisateur '{username}' et l'email '{email}'.")

    # Fermer la connexion à la base de données
    conn.close()

# Exemple d'utilisation
delete_user('ken2', 'photo_signup@Ibra_reco.com')
