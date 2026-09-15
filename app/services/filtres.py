import pandas as pd

def appliquer_filtres(df, filtres_cat, filtres_num):
    sel = df.copy()
    for col, valeurs in filtres_cat.items():
        if not valeurs:
            continue
        if col == "Alternative.positions":
            pattern = "|".join(map(str, valeurs))
            sel = sel[sel[col].fillna("").str.contains(pattern, regex=True)]
        else:
            sel = sel[sel[col].isin(valeurs)]
    for col, (mini, maxi) in filtres_num.items():
        sel = sel[sel[col].between(mini, maxi)]
    return sel
