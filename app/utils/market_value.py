import re
import unicodedata
from difflib import SequenceMatcher

import pandas as pd

from app.constants.config import DATA_PATH
from app.services.football_api import rechercher_joueurs, recuperer_profil

COL_VALEUR = "Valeur Marchande"
COL_API_ID = "API_Player_ID"


def garantir_colonnes_marche(df, sauvegarder=False):
    modifie = False
    if COL_VALEUR not in df.columns:
        df[COL_VALEUR] = pd.Series(pd.NA, index=df.index, dtype="Float64")
        modifie = True
    else:
        df[COL_VALEUR] = pd.to_numeric(df[COL_VALEUR], errors="coerce").astype("Float64")

    if COL_API_ID not in df.columns:
        df[COL_API_ID] = pd.Series(pd.NA, index=df.index, dtype="string")
        modifie = True
    else:
        df[COL_API_ID] = df[COL_API_ID].astype("string")

    if modifie and sauvegarder:
        sauvegarder_donnees(df)
    return df


def sauvegarder_donnees(df):
    df.to_csv(DATA_PATH, index=False)


def valeur_connue(joueur):
    return COL_VALEUR in joueur.index and pd.notna(joueur.get(COL_VALEUR))


def formater_valeur(valeur):
    if valeur is None or pd.isna(valeur):
        return "Non disponible"
    valeur = float(valeur)
    if valeur >= 1_000_000_000:
        return f"{valeur / 1_000_000_000:.1f} Md€".replace(".0 ", " ")
    if valeur >= 1_000_000:
        return f"{valeur / 1_000_000:.1f} M€".replace(".0 ", " ")
    if valeur >= 1_000:
        return f"{valeur / 1_000:.0f} k€"
    return f"{valeur:,.0f} €".replace(",", " ")


def parser_valeur_marche(texte):
    if texte is None or pd.isna(texte):
        return None
    if isinstance(texte, (int, float)):
        return float(texte)
    chiffres = re.sub(r"[^0-9]", "", str(texte))
    return float(chiffres) if chiffres else None


def _norm(texte):
    texte = "" if texte is None or pd.isna(texte) else str(texte)
    texte = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", texte.lower()).strip()


def _sim(a, b):
    a, b = _norm(a), _norm(b)
    return SequenceMatcher(None, a, b).ratio() if a and b else 0.0


def _score_profil(joueur, profil):
    nom_api = " ".join(
        x for x in [profil.get("first_name"), profil.get("last_name")] if x
    ) or profil.get("name", "")
    score = 55 * _sim(joueur.get("Name"), nom_api)

    if _norm(joueur.get("Nation")) and _norm(joueur.get("Nation")) == _norm(profil.get("nationality")):
        score += 15
    if _norm(joueur.get("Team")) and _norm(joueur.get("Team")) == _norm((profil.get("current_team") or {}).get("name")):
        score += 25

    age = joueur.get("Age")
    naissance = profil.get("birthdate")
    if pd.notna(age) and naissance:
        try:
            # Tolérance d'un an : l'âge du dataset peut correspondre à une date de référence différente.
            age_api_approx = pd.Timestamp.now().year - int(str(naissance)[:4])
            if abs(float(age) - age_api_approx) <= 1:
                score += 5
        except (ValueError, TypeError):
            pass
    return round(score, 2)


def trouver_correspondances(joueur, limite=5):
    """Recherche puis qualifie les candidats API pour gérer les homonymes.

    La recherche coûte 1 crédit. Les profils des meilleurs candidats sont ensuite
    récupérés afin de comparer nom complet, nationalité, club et âge. Ces appels
    ne sont faits que lorsque la valeur n'est pas déjà stockée dans le CSV.
    """
    candidats = rechercher_joueurs(str(joueur.get("Name", "")))
    if not candidats:
        return []

    nation = _norm(joueur.get("Nation"))
    tries = sorted(
        candidats,
        key=lambda c: (
            _norm(c.get("country")) == nation,
            _sim(joueur.get("Name"), c.get("name")),
        ),
        reverse=True,
    )[:limite]

    resultats = []
    for candidat in tries:
        profil = recuperer_profil(candidat["id"])
        resultats.append(
            {
                "id": candidat["id"],
                "name": profil.get("name") or candidat.get("name"),
                "full_name": " ".join(
                    x for x in [profil.get("first_name"), profil.get("last_name")] if x
                ).strip(),
                "nationality": profil.get("nationality") or candidat.get("country"),
                "team": (profil.get("current_team") or {}).get("name"),
                "birthdate": profil.get("birthdate"),
                "market_value": profil.get("market_value"),
                "score": _score_profil(joueur, profil),
                "profile": profil,
            }
        )
    return sorted(resultats, key=lambda x: x["score"], reverse=True)


def enregistrer_profil_api(df, index_joueur, profil):
    valeur = parser_valeur_marche(profil.get("market_value"))
    df.at[index_joueur, COL_API_ID] = profil.get("player_id")
    if valeur is not None:
        df.at[index_joueur, COL_VALEUR] = valeur
    sauvegarder_donnees(df)
    return valeur


def actualiser_depuis_id(df, index_joueur, player_id):
    profil = recuperer_profil(player_id)
    return enregistrer_profil_api(df, index_joueur, profil), profil
