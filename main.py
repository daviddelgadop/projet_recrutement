import streamlit as st

from app.constants.config import APP_TITLE
from app.utils.chargement import charger_donnees
from app.components.sidebar import afficher_sidebar
from app.components.navigation import afficher_navigation
from app.services.filtres import appliquer_filtres
from app.pages import synthese, univariee, bivariee, multivariee, profil_joueur

st.set_page_config(page_title=APP_TITLE, page_icon=None, layout="wide")

# En-tête principal
st.title(APP_TITLE)
st.caption("Tableau de bord interactif d'aide au recrutement de joueurs")

# Navigation horizontale visible en permanence
affichage = afficher_navigation()

# Données et filtres globaux : ils s'appliquent à toutes les pages
df = charger_donnees()
f_cat, f_num = afficher_sidebar(df)
df_filtre = appliquer_filtres(df, f_cat, f_num)

# Contexte de sélection toujours visible dans la barre latérale
st.sidebar.divider()
st.sidebar.metric("Joueurs sélectionnés", f"{len(df_filtre):,}".replace(",", " "))
st.sidebar.caption("Les filtres s'appliquent à l'ensemble des onglets.")

# Affichage de la page sélectionnée
if affichage == "Synthèse":
    synthese.afficher(df_filtre)
elif affichage == "Analyse univariée":
    univariee.afficher(df_filtre)
elif affichage == "Analyse bivariée":
    bivariee.afficher(df_filtre)
elif affichage == "Analyse multivariée":
    multivariee.afficher(df_filtre)
elif affichage == "Profil joueur":
    profil_joueur.afficher(df, df_filtre)
