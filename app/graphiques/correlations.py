import plotly.express as px

def heatmap_correlation(df, cols):
    corr = df[cols].corr(numeric_only=True)
    return px.imshow(corr, text_auto=".2f", zmin=-1, zmax=1, color_continuous_scale="RdBu_r", title="Matrice de corrélation")
