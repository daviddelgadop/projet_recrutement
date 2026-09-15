import pandas as pd

def resume_numerique(s):
    s = pd.to_numeric(s, errors="coerce").dropna()
    if s.empty: return {}
    return {"Minimum": s.min(), "Moyenne": s.mean(), "Médiane": s.median(), "Maximum": s.max(), "Écart-type": s.std()}

def percentile_joueur(df_ref, joueur, cols):
    out = {}
    for c in cols:
        if c not in df_ref or pd.isna(joueur.get(c)): continue
        s = df_ref[c].dropna()
        if len(s): out[c] = round((s <= joueur[c]).mean() * 100, 1)
    return out
