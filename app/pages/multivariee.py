import streamlit as st
from app.graphiques.correlations import heatmap_correlation
from app.graphiques.relations import scatter

def afficher(df):
    st.header("Analyse multivariée")
    mode=st.radio("Type d'analyse",["Corrélations","Relation multiple"],horizontal=True)
    nums=df.select_dtypes(include="number").columns.tolist(); cats=[c for c in df.select_dtypes(exclude="number").columns if c not in ["Name","url"]]
    if mode=="Corrélations":
        default=[c for c in ["OVR","PAC","SHO","PAS","DRI","DEF","PHY"] if c in nums]
        cols=st.multiselect("Variables quantitatives",nums,default=default)
        if len(cols)>=2: st.plotly_chart(heatmap_correlation(df,cols),use_container_width=True)
        else: st.info("Sélectionnez au moins deux variables.")
    else:
        c1,c2=st.columns(2); x=c1.selectbox("Axe X",nums,index=nums.index("PAC") if "PAC" in nums else 0); y=c2.selectbox("Axe Y",nums,index=nums.index("DRI") if "DRI" in nums else 1)
        couleur=st.selectbox("Couleur (variable qualitative)",["Aucune"]+cats)
        taille=st.selectbox("Taille (variable quantitative)",["Aucune"]+nums,index=(["Aucune"]+nums).index("OVR") if "OVR" in nums else 0)
        d=df
        if couleur!="Aucune":
            top=d[couleur].value_counts().head(8).index; d=d[d[couleur].isin(top)]
        st.plotly_chart(scatter(d,x,y,None if couleur=="Aucune" else couleur,None if taille=="Aucune" else taille),use_container_width=True)
