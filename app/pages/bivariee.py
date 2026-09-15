import streamlit as st
from app.utils.types_variables import type_variable
from app.graphiques.relations import scatter
from app.graphiques.comparaisons import boxplot, quali_quali

def afficher(df):
    st.header("Analyse bivariée")
    candidates=[c for c in df.columns if c not in ["Name","url"]]
    c1,c2=st.columns(2); x=c1.selectbox("Variable X",candidates,index=candidates.index("PAC") if "PAC" in candidates else 0); y=c2.selectbox("Variable Y",candidates,index=candidates.index("OVR") if "OVR" in candidates else 1)
    tx,ty=type_variable(df,x),type_variable(df,y); st.caption(f"{x} : {tx} | {y} : {ty}")
    if tx==ty=="quantitative":
        r=df[[x,y]].corr().iloc[0,1]; st.metric("Corrélation de Pearson",f"{r:.3f}")
        tendance=st.checkbox("Afficher la droite de régression",True)
        st.plotly_chart(scatter(df,x,y,tendance=tendance),use_container_width=True)
    elif tx!=ty:
        cat,num=(x,y) if tx=="qualitative" else (y,x)
        maxcat=st.slider("Limiter aux catégories les plus représentées",3,20,10)
        tops=df[cat].value_counts().head(maxcat).index; d=df[df[cat].isin(tops)]
        st.plotly_chart(boxplot(d,cat,num),use_container_width=True)
    else:
        maxcat=st.slider("Limiter chaque variable au Top N",3,15,8)
        dx=df[df[x].isin(df[x].value_counts().head(maxcat).index) & df[y].isin(df[y].value_counts().head(maxcat).index)]
        st.plotly_chart(quali_quali(dx,x,y),use_container_width=True)
