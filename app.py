import os
import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow  # 🔹 Importation nécessaire
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import sqlite3
import hashlib
import json
from add_user import add_user, hash_password, add_user_avec_photo
from Reconnaissance import reco, get_existence, get_nom_utilisateur
from Extraction import extraction_carac
import google.auth  # 🔹 Importation nécessaire pour google.auth
from google.auth.transport.requests import Request  # 🔹 Importation nécessaire pour Request

# Initialisation de la session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.switch_page("pages/acceuil.py")

# 🔹 Configuration OAuth
CLIENT_SECRET_FILE = 'mes_info.json'
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
TOKEN_FILE = 'token.json'

# Fonction pour hacher un mot de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Fonction d'authentification SQLite
def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        stored_password_hash = user[3]
        if stored_password_hash == hash_password(password):
            return True
    return False

# Fonction pour récupérer les infos Google
def google_login():
    creds = None

    # Vérifier si un token valide existe déjà
    if os.path.exists('token.json'):
        try:
            creds, _ = google.auth.load_credentials_from_file('token.json')  # 🔹 Correction ici
        except Exception:
            os.remove('token.json')
            creds = None

    # Si aucun token valide, lancer l'authentification
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # 🔹 Correction ici
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES  # 🔹 Correction ici
            )
            creds = flow.run_local_server(port=8501)  # 🔹 Redirection locale automatique

        # Sauvegarder les nouvelles infos d'authentification
        with open('token.json', 'w') as token:
            json.dump({
                'token': creds.token,
                'refresh_token': creds.refresh_token,
                'token_uri': creds.token_uri,
                'client_id': creds.client_id,
                'client_secret': creds.client_secret,
                'scopes': creds.scopes
            }, token)

    # 🔹 Connexion automatique si tout est bon
    if creds and creds.valid:
        service = build('oauth2', 'v2', credentials=creds)
        user_info = service.userinfo().get().execute()
        return user_info
    else:
        return None

# Interface Streamlit
def login_page():
    st.set_page_config(page_title="Connexion", page_icon="🔐", layout="centered")

    page_selection = st.radio("Choisissez une page", ("Connexion", "Inscription"))

    if page_selection == "Connexion":
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
        st.title("Connexion")

        username = st.text_input("Nom d'utilisateur", placeholder="Entrez votre nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password", placeholder="Entrez votre mot de passe")

        if st.button("Se connecter", key="login"):
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.switch_page("pages/acceuil.py")
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect")

        if st.button("Se connecter avec Google", key="google_login"):
            user_info = google_login()
            if user_info:
                st.session_state.logged_in = True
                st.session_state.username = user_info.get("name", "Utilisateur inconnu")
                st.switch_page("pages/acceuil.py")
            else:
                st.error("Échec de la connexion avec Google")

        if st.button("Se connecter avec Reconnaissance Faciale", key="reconnaissance_faciale"):
            reco()
            if get_existence():
                st.session_state.logged_in = True
                st.session_state.username = get_nom_utilisateur()
                st.switch_page("pages/acceuil.py")
            else:
                st.error("Échec de la reconnaissance faciale")

    elif page_selection == "Inscription":
        st.title("Inscription")

        signup_method = st.radio("Comment souhaitez-vous vous inscrire ?", 
                                 ("Inscription classique", "S'inscrire avec Google", "S'inscrire par photo"))

        if signup_method == "Inscription classique":
            username = st.text_input("Nom d'utilisateur", placeholder="Entrez votre nom d'utilisateur")
            email = st.text_input("Email", placeholder="Entrez votre email")
            password = st.text_input("Mot de passe", type="password", placeholder="Entrez votre mot de passe")

            if st.button("S'inscrire", key="signup"):
                add_user(username, email, password)
                st.success("Inscription réussie !")

        elif signup_method == "S'inscrire avec Google":
            user_info = google_login()
            if user_info:
                username = user_info.get("name", "Utilisateur")
                email = user_info.get("email", "")
                password = hash_password("google_auth")
                add_user(username, email, password)
                st.success(f"Inscription réussie avec Google ! Bienvenue, {username}")
            else:
                st.error("Échec de la connexion avec Google")

        elif signup_method == "S'inscrire par photo":
            username = st.text_input("Nom d'utilisateur", placeholder="Entrez votre nom d'utilisateur")
            email = st.text_input("Email", placeholder="Entrez votre email")
            uploaded_file = st.file_uploader("Téléversez votre photo", type=["png", "jpg", "jpeg"])

            if uploaded_file is not None:
                save_path = f"./capture/{username}.jpg"
                os.makedirs("./capture/", exist_ok=True)
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                st.success(f"Photo enregistrée sous {save_path}")
                add_user_avec_photo(username, email, hash_password("photo_auth"), save_path)
                st.warning("Extraction des caractéristiques en cours...")
                extraction_carac()
                st.success("Inscription réussie avec photo !")
                st.success("Caractéristiques extraites avec succès !")

        st.write("Retour à la page de connexion ? [Clique ici](./)")

if __name__ == "__main__":
    login_page()
