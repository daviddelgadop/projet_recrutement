import pandas as pd
import streamlit as st
from app.constants.colonnes import GLOBAL_CATEGORICAL, GLOBAL_NUMERIC
from app.utils.market_value import COL_VALEUR, formater_valeur


def afficher_sidebar(df):
    st.sidebar.header("Filtres globaux")
    if st.sidebar.button("Réinitialiser les filtres", use_container_width=True):
        for k in list(st.session_state):
            if k.startswith("gf_"):
                del st.session_state[k]
        st.rerun()

    cat = {}
    with st.sidebar.expander("Variables catégorielles", expanded=True):
        for col in GLOBAL_CATEGORICAL:
            if col not in df:
                continue
            if col == "Alternative.positions":
                vals = sorted({p.strip() for x in df[col].dropna().astype(str) for p in x.split(",") if p.strip()})
            else:
                vals = sorted(df[col].dropna().astype(str).unique().tolist())
            cat[col] = st.multiselect(col, vals, key=f"gf_cat_{col}")

    num = {}
    with st.sidebar.expander("Critères numériques principaux"):
        for col in GLOBAL_NUMERIC:
            if col not in df:
                continue
            lo, hi = float(df[col].min()), float(df[col].max())
            step = 1.0
            num[col] = st.slider(col, lo, hi, (lo, hi), step=step, key=f"gf_num_{col}")

    # Le filtre de valeur marchande est séparé : les valeurs inconnues ne doivent
    # jamais être assimilées à 0 € ni exclues tant que le filtre n'est pas activé.
    if COL_VALEUR in df.columns:
        valeurs_connues = pd.to_numeric(df[COL_VALEUR], errors="coerce").dropna()
        if not valeurs_connues.empty:
            with st.sidebar.expander("Valeur marchande"):
                st.caption(f"{len(valeurs_connues):,} joueur(s) enrichi(s)".replace(",", " "))
                actif = st.checkbox("Activer le filtre", key="gf_market_active")
                if actif:
                    lo, hi = float(valeurs_connues.min()), float(valeurs_connues.max())
                    if lo == hi:
                        st.caption(f"Valeur disponible : {formater_valeur(lo)}")
                        num[COL_VALEUR] = (lo, hi)
                    else:
                        selection = st.slider(
                            "Valeur Marchande (€)",
                            min_value=int(lo),
                            max_value=int(hi),
                            value=(int(lo), int(hi)),
                            step=max(100_000, int((hi - lo) / 100)),
                            format="%d €",
                            key="gf_market_range",
                        )
                        num[COL_VALEUR] = selection
                st.caption("Le filtre porte uniquement sur les joueurs dont la valeur marchande est connue.")

    with st.sidebar.expander("Critères numériques avancés"):
        all_num = [
            c for c in df.select_dtypes(include="number").columns
            if c not in GLOBAL_NUMERIC and c != COL_VALEUR
        ]
        choisis = st.multiselect("Ajouter des variables", all_num, key="gf_advanced_cols")
        for col in choisis:
            lo, hi = float(df[col].min()), float(df[col].max())
            if lo == hi:
                continue
            num[col] = st.slider(col, lo, hi, (lo, hi), step=1.0, key=f"gf_adv_{col}")
    return cat, num
