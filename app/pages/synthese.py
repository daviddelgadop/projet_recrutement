import streamlit as st
import plotly.express as px
from app.components.kpi import afficher_kpi
from app.services.recommandations import meilleurs_profils, synthese_textuelle
from app.graphiques.distributions import histogramme
from app.graphiques.relations import scatter

def afficher(df):
    st.header("Synthèse du recrutement")
    afficher_kpi(df)
    if df.empty: st.warning("Aucun joueur ne correspond aux filtres."); return
    st.subheader("Synthèse de l'analyse")
    for t in synthese_textuelle(df): st.write("- " + t)
    c1,c2 = st.columns(2)
    with c1: st.plotly_chart(histogramme(df,"OVR"), use_container_width=True)
    with c2: st.plotly_chart(scatter(df,"PAC","DRI",taille="OVR"), use_container_width=True)
    st.subheader("Profils à surveiller")
    st.dataframe(meilleurs_profils(df), use_container_width=True, hide_index=True)
