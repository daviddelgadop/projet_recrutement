import plotly.express as px

def scatter(df, x, y, couleur=None, taille=None, tendance=False):
    kwargs = dict(data_frame=df, x=x, y=y, hover_name="Name" if "Name" in df else None, color=couleur, size=taille, title=f"{x} × {y}")
    if tendance and couleur is None: kwargs["trendline"] = "ols"
    return px.scatter(**kwargs)
