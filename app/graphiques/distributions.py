import plotly.express as px

def histogramme(df, col):
    return px.histogram(df, x=col, marginal="box", title=f"Distribution de {col}")

def barres_effectifs(df, col, top_n=20):
    vc = df[col].fillna("Non renseigné").value_counts().head(top_n).rename_axis(col).reset_index(name="Effectif")
    return px.bar(vc, x="Effectif", y=col, orientation="h", title=f"Effectifs par {col}").update_layout(yaxis={'categoryorder':'total ascending'})
