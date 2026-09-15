import plotly.graph_objects as go


def radar(labels, values, titre="Profil", nom_serie=None):
    """Radar simple sur une échelle commune de 0 à 100."""
    labels = list(labels)
    values = [float(v) for v in values]
    serie = nom_serie or titre

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values + values[:1],
            theta=labels + labels[:1],
            fill="toself",
            fillcolor="rgba(31, 119, 180, 0.22)",
            line=dict(color="rgba(31, 119, 180, 0.95)", width=2),
            marker=dict(size=5),
            name=serie,
            hovertemplate="%{theta}: %{r:.1f}<extra>%{fullData.name}</extra>",
        )
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100], tick0=0, dtick=20)),
        showlegend=False,
        title=titre,
        margin=dict(l=45, r=45, t=70, b=35),
    )
    return fig


def radar_comparaison(labels, values_1, values_2, nom_1, nom_2, titre="Comparaison des profils"):
    """Radar superposé de deux joueurs avec remplissages transparents."""
    labels = list(labels)
    values_1 = [float(v) for v in values_1]
    values_2 = [float(v) for v in values_2]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values_1 + values_1[:1],
            theta=labels + labels[:1],
            fill="toself",
            fillcolor="rgba(31, 119, 180, 0.18)",
            line=dict(color="rgba(31, 119, 180, 0.95)", width=2),
            marker=dict(size=5),
            name=nom_1,
            hovertemplate="%{theta}: %{r:.1f}<extra>%{fullData.name}</extra>",
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=values_2 + values_2[:1],
            theta=labels + labels[:1],
            fill="toself",
            fillcolor="rgba(255, 127, 14, 0.18)",
            line=dict(color="rgba(255, 127, 14, 0.95)", width=2),
            marker=dict(size=5),
            name=nom_2,
            hovertemplate="%{theta}: %{r:.1f}<extra>%{fullData.name}</extra>",
        )
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100], tick0=0, dtick=20)),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.08, xanchor="center", x=0.5),
        title=titre,
        margin=dict(l=45, r=45, t=95, b=35),
    )
    return fig
