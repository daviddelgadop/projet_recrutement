import streamlit as st
from app.utils.types_variables import colonnes_quantitatives, colonnes_qualitatives, type_variable
from app.services.statistiques import resume_numerique
from app.graphiques.distributions import histogramme, barres_effectifs

def afficher(df):
    st.header("Analyse univariée")
    cols = colonnes_quantitatives(df) + colonnes_qualitatives(df)
    var = st.selectbox("Variable à analyser", cols)
    typ = type_variable(df,var); st.caption(f"Type détecté : {typ}")
    if typ == "quantitative":
        r=resume_numerique(df[var]); boxes=st.columns(len(r))
        for b,(k,v) in zip(boxes,r.items()): b.metric(k,f"{v:.1f}")
        st.plotly_chart(histogramme(df,var), use_container_width=True)
    else:
        topn=st.slider("Nombre de modalités affichées",5,30,15)
        st.metric("Nombre de modalités", df[var].nunique(dropna=True))
        st.plotly_chart(barres_effectifs(df,var,topn), use_container_width=True)
