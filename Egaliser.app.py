import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Configuration de la page Streamlit (ce que l'utilisateur voit en ouvrant le lien)
st.set_page_config(page_title="Index Tracker Universel Absolu", layout="wide")

st.title("🧬 L'Agent Autonome d'Égalisation Mondiale")
st.write("Cette infrastructure Python utilise Internet pour mettre à plat les actifs mondiaux en temps réel sur la base de la **Voix** et du **Capital**.")

# 1. Liste des actifs en cours connectés à Internet
TICKERS_MONDIAUX = {
    "Apple (Tech USA)": "AAPL",
    "Belfius / Indices Belges (BEL20)": "^BFX",
    "TotalEnergies (Énergie)": "TTE.PA",
    "LVMH (Luxe Europe)": "MC.PA",
    "iShares MSCI World (Global)": "URTH"
}

# Fonction autonome pour aspirer la réalité financière du web
@st.cache_data(ttl=60) # Rafraîchit les chiffres sur Internet toutes les 60 secondes automatiquement
def aspirer_les_actifs_du_web():
    donnees_temps_reel = {}
    for nom, ticker in TICKERS_MONDIAUX.items():
        try:
            tick = yf.Ticker(ticker)
            historique = tick.history(period="1d")
            if not historique.empty:
                dernier_prix = historique['Close'].iloc[-1]
                donnees_temps_reel[nom] = {"Capital Réel ($)": round(dernier_prix, 2)}
        except Exception:
            pass
    return pd.DataFrame(donnees_temps_reel).T

# --- CHARGEMENT ET CONFIGURATION DE L'APPLICATION ---
df_marche = aspirer_les_actifs_du_web()

if not df_marche.empty:
    # 2. La brique de la VOIX (L'interface démocratique interactive)
    st.subheader("🗳️ Le Pôle de la Voix Humaine")
    st.write("Attribuez le soutien des Voix citoyennes à chaque structure (0 à 100 %).")
    
    # Création de curseurs interactifs Streamlit pour simuler les Voix
    voix_utilisateurs = {}
    cols = st.columns(len(df_marche))
    for idx, (nom, row) in enumerate(df_marche.iterrows()):
        with cols[idx]:
            voix_utilisateurs[nom] = st.slider(f"Voix pour {nom.split(' ')[0]}", 0, 100, 70)

    # Injection des Voix dans notre matrice de calcul
    df_marche["Voix Humaines (%)"] = pd.Series(voix_utilisateurs)

    # 3. La brique de la REMISE À PLAT (Le calcul statistique d'égalisation)
    # Calcul du rang brut combinant le capital réel aspiré et les voix accordées
    df_marche["Rang Brut"] = df_marche["Capital Réel ($)"] * (df_marche["Voix Humaines (%)"] / 100)
    
    # Normalisation stricte pour forcer toutes les entités à exister au même rang (entre 0 et 1)
    df_marche["Rang Stabilisé"] = (df_marche["Rang Brut"] - df_marche["Rang Brut"].min()) / (df_marche["Rang Brut"].max() - df_marche["Rang Brut"].min() + 1e-9)

    # 4. L'affichage final en direct sur l'application Web
    st.subheader("📊 Tableau de Bord de la Globalité Stabilisée")
    st.dataframe(df_marche[["Capital Réel ($)", "Voix Humaines (%)", "Rang Stabilisé"]], use_container_width=True)

    # Calcul de la valeur finale de l'Action Unique Mondiale
    valeur_action_unique = df_marche["Rang Stabilisé"].mean()
    
    st.metric(label="🧬 Valeur de la Single-Action Mondiale Égalisée", value=f"{valeur_action_unique:.4f}")
    
    # Graphique visuel généré automatiquement par Streamlit pour matérialiser la plaine horizontale
    st.bar_chart(df_marche["Rang Stabilisé"])
else:
    st.error("Impossible de se connecter aux lignes internet pour le moment.")

