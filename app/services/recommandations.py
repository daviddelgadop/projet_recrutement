from app.constants.colonnes import MAIN_STATS

def meilleurs_profils(df, n=15):
    cols = [c for c in ["Name","OVR","PAC","DRI","SHO","PAS","DEF","PHY","Position","League","Team","Nation"] if c in df.columns]
    return df.sort_values(["OVR","DRI","PAC"], ascending=False)[cols].head(n)

def synthese_textuelle(df):
    if df.empty: return ["Aucun joueur ne correspond aux filtres actuels."]
    lignes = [f"{len(df):,} joueurs correspondent aux critères actuels.".replace(",", " ")]
    lignes.append(f"OVR médian : {df['OVR'].median():.1f} ; OVR moyen : {df['OVR'].mean():.1f}.")
    top = df.sort_values("OVR", ascending=False).iloc[0]
    lignes.append(f"Meilleur OVR de la sélection : {top['Name']} ({int(top['OVR'])}).")
    elite = df[(df['PAC'] >= 85) & (df['DRI'] >= 85)]
    lignes.append(f"{len(elite)} joueurs combinent PAC ≥ 85 et DRI ≥ 85.")
    if "Position" in df: lignes.append(f"Poste le plus représenté : {df['Position'].mode().iloc[0]}.")
    return lignes
