import streamlit as st

def afficher_kpi(df):
    cols = st.columns(5)
    cols[0].metric("Joueurs", f"{len(df):,}".replace(",", " "))
    for box, stat in zip(cols[1:], ["OVR","PAC","DRI","PHY"]):
        box.metric(f"{stat} moyen", "—" if df.empty else f"{df[stat].mean():.1f}")
