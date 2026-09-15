import plotly.express as px

def boxplot(df, cat, num):
    return px.box(df, x=cat, y=num, points=False, title=f"{num} selon {cat}")

def quali_quali(df, x, y):
    tab = df.groupby([x,y]).size().reset_index(name="Effectif")
    return px.density_heatmap(tab, x=x, y=y, z="Effectif", histfunc="sum", title=f"{x} × {y}")
