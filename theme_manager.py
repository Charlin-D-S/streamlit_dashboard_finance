# theme_manager.py

import streamlit as st

def format_number_fr(value):
    """Format français : espace pour les milliers, virgule pour décimale."""
    try:
        return f"{value:,.2f}".replace(",", " ").replace(".", ",")
    except:
        return str(value)

def inject_base_css(file_path: str = "style.css"):
    """Charge un fichier CSS statique."""
    try:
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ Le fichier style.css est introuvable.")

def inject_theme_css(theme: str):
    """Injecte le CSS du thème clair ou sombre."""
    if theme == "dark":
        st.markdown("""
        <style>
            .stApp {
                background-color: #121212;
                color: #e0e0e0;
            }
            .css-1d391kg, .css-1kyxreq, .st-bx, .st-c6, .st-dp, .st-cg {
                background-color: #1e1e1e !important;
                color: #e0e0e0 !important;
            }
            button {
                background-color: #333333;
                color: #ffffff;
            }
        </style>
        """, unsafe_allow_html=True)
