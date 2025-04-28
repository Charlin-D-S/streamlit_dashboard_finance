

import streamlit as st
import streamlit_authenticator as stauth
from hashlib import sha256
import yaml
from yaml.loader import SafeLoader
import yfinance as yf
import wbdata
import pandas as pd
from datetime import datetime
import plotly.express as px
import locale
#locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')  # pour Linux/mac
locale.setlocale(locale.LC_ALL, '')  # ← Pour Windows, essayer sans param

############################################################

# ------------------
# Configuration utilisateurs (a remplacer par une base de donnees plus tard)
# ------------------
USERS = {
    "admin": sha256("adam".encode()).hexdigest(),
    "user1": sha256("ptti".encode()).hexdigest()
}

# ------------------
# Fonction d'authentification
# ------------------
def authenticate(username, password):
    if username in USERS:
        return USERS[username] == sha256(password.encode()).hexdigest()
    return False

########################################################",,,"


st.set_page_config(page_title="Dashboard Financier", layout="wide")
theme = st.toggle("🌗 Mode sombre", value=False)
# ────── AUTHENTIFICATION ──────
# Charger config YAML
# with open("config_auth.yaml") as file:
#     config = yaml.load(file, Loader=SafeLoader)

# # Initialiser authentificateur
# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days']
# )
# # 📍 Appel du formulaire de connexion
# fields = {
#     "Form name": "Connexion",
#     "Username": "Nom d’utilisateur",
#     "Password": "Mot de passe",
#     "Login": "Se connecter"
# }

# login_info = authenticator.login(location='unrendered')#,fields=fields)

# if login_info is None:
#     st.info("Veuillez entrer vos identifiants8888.")
#     #st.stop()

# # Sinon, déballer les valeurs
# name, authentication_status, username = login_info
# # Gérer les différents cas

# if authentication_status is None:
#     st.info("Veuillez entrer vos identifiants NONE.")
#     st.stop()

# if authentication_status is False:
#     st.error("Identifiants incorrects.")
#     st.stop()
# ───────── Thème & CSS de base ─────────
from theme_manager import inject_base_css, inject_theme_css, format_number_fr
inject_base_css("assets/style.css")
theme_class = "dark" if theme else "light"
inject_theme_css(theme_class)
#############################################################
 # Gestion de la session
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    with st.form("login_form"):
        st.subheader("Connexion")
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter")

    if submitted:
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.success("Connexion réussie !")
        else:
            st.error("Identifiants invalides. Veuillez réessayer.")
else:
    #st.success(f"Vous êtes connecté en tant que : {username}")
    # Bouton de déconnexion
    if st.button("Se déconnecter"):
        st.session_state.authenticated = False
        st.stop() #experimental_rerun()
    
# st.success(f"Bienvenue {name}")
# authenticator.logout("Se déconnecter", "sidebar")
# # --- authentification réussie ---

    st.title("📊 Dashboard Financier - Données Réelles")

    # ----------------------------
    # 📈 Données Boursières (facultatif)
    # ----------------------------
    st.subheader("📉 Données Boursières (Yahoo Finance)")
    tickers = st.multiselect("Actions à suivre :", ["AAPL", "MSFT", "TSLA", "GOOG", "AMZN"], default=["AAPL"])
    start = st.date_input("Date de début", datetime(2015, 1, 1))
    end = st.date_input("Date de fin", datetime.today())

    @st.cache_data(ttl=86400)
    def load_all_yahoo_data(tickers, start, end):
        df = yf.download(tickers, start=start, end=end)["Close"]
        return df

    df = load_all_yahoo_data(tickers, start, end)
    st.line_chart(df)
    st.dataframe(df.tail())


    # ----------------------------
    # 🌍 Paramètres
    # ----------------------------
    # Pays valides : top 10 + pays africains
    countries = ['USA', 'CHN', 'JPN', 'DEU', 'IND', 'GBR', 'FRA', 'ITA', 'BRA', 'CAN',
                'NGA', 'ZAF', 'CMR', 'CIV', 'GHA', 'SEN', 'BEN']

    # Indicateurs macro et IA
    indicators = {
        'NY.GDP.MKTP.CD': 'PIB ($)',
        'FP.CPI.TOTL.ZG': 'Inflation (%)',
        'SL.UEM.TOTL.ZS': 'Chômage (%)',
        'IT.NET.USER.ZS': 'Utilisateurs Internet (%)',
        'GB.XPD.RSDV.GD.ZS': 'Dépenses R&D (% PIB)',
        'SP.POP.TECH.RD.P6': 'Chercheurs en R&D (par million)',
        'SE.TER.ENRL': 'Étudiants en enseignement supérieur',
        'IP.JRN.ARTC.SC': 'Articles scientifiques',
    }
    reverse_indicators = {v: k for k, v in indicators.items()}

    # ----------------------------
    # 📥 Téléchargement unique des données (caché)
    # ----------------------------
    @st.cache_data(ttl=86400)
    def load_all_macro_data(indicators_dict, countries):
        df = wbdata.get_dataframe(
            indicators=indicators_dict,
            country=countries,
            date=(datetime(2010, 1, 1), datetime.today())
        ).reset_index().rename(columns={"date": "Date", "country": "Pays"})
        return df



    with st.spinner("📡 Téléchargement des données World Bank..."):
        macro_df_full = load_all_macro_data(indicators, countries)

    #
    # ----------------------------
    # 📌 KPIs : Afficher tous les indicateurs pour 1 pays
    # ----------------------------
    st.subheader("📌 Indicateurs récents pour un pays")
    pays_kpi = st.selectbox("🌍 Choisir un pays :", sorted(macro_df_full["Pays"].dropna().unique()))

    df_pays = macro_df_full[macro_df_full["Pays"] == pays_kpi]

    # Génération dynamique des colonnes
    columns = st.columns(3)

    for i, indicator in enumerate(indicators.values()):
        df_ind = df_pays[["Date", indicator]].dropna().sort_values("Date")
        if not df_ind.empty:
            last_val = df_ind.iloc[-1][indicator]
            last_date = df_ind.iloc[-1]["Date"]#.strftime("%Y")
            formatted = format_number_fr(last_val)#f"{value:,.2f}".replace(",", " ").replace(".", ",")

            # HTML stylisé dans st.markdown
            columns[i % 3].markdown(f"""
        <div class="kpi-box {theme_class}">
            <div class="kpi-label">{indicator} <span style="color:#888">({last_date})</span></div>
            <div class="kpi-value">{formatted}</div>
        </div>
        """, unsafe_allow_html=True)

    # ----------------------------
    # 📊 Sélection d’un indicateur pour la suite
    # ----------------------------
    selected_metric = st.selectbox("📈 Choisir un indicateur à analyser :", list(indicators.values()))

    # Préparer les données pour la courbe et carte
    macro_df = macro_df_full[["Date", "Pays", selected_metric]].dropna()

    # ----------------------------
    # 📈 Évolution temporelle
    # ----------------------------
    st.subheader("📈 Évolution temporelle")
    selected_countries = st.multiselect("Pays :", sorted(macro_df["Pays"].unique()), default=["France", "Germany", "Nigeria"])
    df_line = macro_df[macro_df["Pays"].isin(selected_countries)]

    fig = px.line(df_line, x="Date", y=selected_metric, color="Pays", title=f"Évolution de {selected_metric}")
    st.plotly_chart(fig, use_container_width=True)


    # ----------------------------
    # 🗺️ Carte mondiale
    # ----------------------------
    st.subheader("🗺️ Carte du monde — Dernière valeur disponible")

    # Pour chaque pays, récupérer la dernière valeur non nulle
    latest_values = macro_df.sort_values("Date").dropna().groupby("Pays").tail(1)

    fig_map = px.choropleth(
        latest_values,
        locations="Pays",
        locationmode="country names",
        color=selected_metric,
        hover_name="Pays",
        color_continuous_scale="Viridis",
        title=f"{selected_metric} par pays (valeur la plus récente)",
        labels={selected_metric: selected_metric}
    )
    fig_map.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth',
            showland=True,
            landcolor="rgb(217, 217, 217)",
            showcountries=True
        )
    )
    st.plotly_chart(fig_map, use_container_width=True)

