# home.py
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


def show_home():
    # ──────────────────────────────────────────────
    #  Charger la configuration des utilisateurs
    # ──────────────────────────────────────────────
    with open("config_auth.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )

    # ──────────────────────────────────────────────
    #  Page d’accueil publique
    # ──────────────────────────────────────────────
    st.markdown(
        "<h1 style='text-align:center;'>📊 Dashboard Financier International</h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style='text-align:center;'>
            Bienvenue dans le dashboard financier !<br>
            Visualisez les indicateurs économiques mondiaux, l’innovation et les marchés boursiers.<br><br>
            <i>Merci de vous connecter pour accéder aux données 🔐</i>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # ──────────────────────────────────────────────
    #  Formulaire de connexion  ➜  on récupère
    #  les trois valeurs retournées par .login()
    # ──────────────────────────────────────────────
    fields = {
    "Form name": "Connexion",
    "Username": "Nom d’utilisateur",
    "Password": "Mot de passe",
    "Login": "Se connecter"
    }
    name, auth_status, username = authenticator.login(location="main")#, fields=fields)

    # on renvoie les infos utiles au « main »
    return authenticator, name, auth_status, username
