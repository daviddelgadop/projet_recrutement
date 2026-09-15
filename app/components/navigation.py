import streamlit as st

PAGES = [
    "Synthèse",
    "Analyse univariée",
    "Analyse bivariée",
    "Analyse multivariée",
    "Profil joueur",
]


def afficher_navigation():
    """Navigation principale horizontale, toujours visible sous l'en-tête."""
    st.markdown(
        """
        <style>
        /* Barre de navigation principale */
        div[data-testid="stSegmentedControl"] {
            margin-top: 0.35rem;
            margin-bottom: 1.15rem;
        }
        div[data-testid="stSegmentedControl"] > div {
            width: 100%;
        }
        div[data-testid="stSegmentedControl"] button {
            min-height: 2.8rem;
            font-weight: 600;
        }
        /* Réduit l'espace supérieur pour une apparence dashboard */
        .block-container {
            padding-top: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    page = st.segmented_control(
        "Navigation principale",
        options=PAGES,
        default="Synthèse",
        selection_mode="single",
        key="navigation_principale",
        label_visibility="collapsed",
    )
    return page or "Synthèse"
