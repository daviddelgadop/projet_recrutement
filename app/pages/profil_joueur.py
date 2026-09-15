import pandas as pd
import streamlit as st

from app.constants.colonnes import MAIN_STATS, PROFILE_GROUPS
from app.services.statistiques import percentile_joueur
from app.graphiques.radar import radar, radar_comparaison
from app.services.football_api import api_configuree
from app.utils.market_value import (
    COL_API_ID,
    COL_VALEUR,
    actualiser_depuis_id,
    enregistrer_profil_api,
    formater_valeur,
    trouver_correspondances,
)


def _profil_depuis_candidat(candidat):
    profil = dict(candidat["profile"])
    profil["player_id"] = candidat["id"]
    return profil


def _obtenir_valeur(df, index_joueur, joueur, cle_widget):
    """Retourne la valeur stockée ou enrichit une seule fois la ligne via l'API."""
    valeur = joueur.get(COL_VALEUR)
    if pd.notna(valeur):
        return float(valeur)

    if not api_configuree():
        st.info(
            "Valeur marchande non renseignée. Ajoutez FOOTBALL_API_KEY dans "
            ".streamlit/secrets.toml pour activer l'enrichissement API."
        )
        return None

    api_id = joueur.get(COL_API_ID)
    try:
        if pd.notna(api_id) and str(api_id).strip():
            with st.spinner("Récupération de la valeur marchande..."):
                valeur, _ = actualiser_depuis_id(df, index_joueur, str(api_id))
            return valeur

        session_key = f"market_candidates_{cle_widget}_{index_joueur}"
        if session_key not in st.session_state:
            with st.spinner("Recherche de la valeur marchande..."):
                st.session_state[session_key] = trouver_correspondances(joueur)

        candidats = st.session_state[session_key]
        if not candidats:
            st.warning("Aucune correspondance trouvée dans Live Football API pour ce joueur.")
            return None

        # Correspondance automatique uniquement si elle est suffisamment forte
        # et nettement meilleure que la suivante.
        meilleur = candidats[0]
        ecart = meilleur["score"] - candidats[1]["score"] if len(candidats) > 1 else 100
        if meilleur["score"] >= 80 and ecart >= 15:
            valeur = enregistrer_profil_api(df, index_joueur, _profil_depuis_candidat(meilleur))
            del st.session_state[session_key]
            return valeur

        st.warning("Plusieurs joueurs peuvent correspondre. Confirmez le bon profil avant l'enregistrement.")
        options = {c["id"]: c for c in candidats}

        def libelle(pid):
            c = options[pid]
            nom = c.get("full_name") or c.get("name") or pid
            details = [c.get("team"), c.get("nationality"), c.get("birthdate")]
            details = [str(x) for x in details if x]
            return f"{nom} — {' | '.join(details)}"

        choix = st.selectbox(
            "Correspondance API",
            list(options),
            format_func=libelle,
            key=f"market_choice_{cle_widget}_{index_joueur}",
        )
        if st.button("Confirmer ce joueur", key=f"market_confirm_{cle_widget}_{index_joueur}"):
            valeur = enregistrer_profil_api(df, index_joueur, _profil_depuis_candidat(options[choix]))
            del st.session_state[session_key]
            st.rerun()
        return None

    except Exception as exc:
        st.warning(f"Impossible de récupérer la valeur marchande : {exc}")
        return None


def afficher(df_complet, df_filtre):
    st.header("Profil du joueur")
    st.caption(
        "Analyse individuelle d'un joueur, positionnement par rapport à un groupe de référence "
        "et comparaison directe avec un autre profil."
    )

    base = df_filtre if not df_filtre.empty else df_complet
    noms = sorted(base["Name"].dropna().unique())
    nom = st.selectbox("Rechercher un joueur", noms)
    joueur = base[base["Name"] == nom].sort_values("OVR", ascending=False).iloc[0]
    index_joueur = joueur.name

    st.subheader(nom)
    st.caption(
        " | ".join(
            str(joueur.get(c, ""))
            for c in ["Team", "League", "Position", "Nation"]
            if str(joueur.get(c, "")) != "nan"
        )
    )

    boxes = st.columns(7)
    for b, c in zip(boxes, MAIN_STATS):
        b.metric(c, int(joueur[c]))

    valeur_1 = _obtenir_valeur(df_complet, index_joueur, joueur, "principal")
    st.metric("Valeur marchande", formater_valeur(valeur_1))
    if valeur_1 is not None:
        st.caption("Valeur enregistrée dans le fichier local. Source initiale : Live Football API.")

    st.markdown("### Lecture du profil")
    ref_mode = st.radio(
        "Groupe de référence pour le percentile",
        ["Même poste", "Même championnat", "Tous les joueurs"],
        horizontal=True,
        help="Le groupe de référence sert uniquement au radar en percentiles. Les notes absolues restent les notes du joueur sur 100.",
    )

    if ref_mode == "Même poste":
        ref = df_complet[df_complet["Position"] == joueur["Position"]]
    elif ref_mode == "Même championnat":
        ref = df_complet[df_complet["League"] == joueur["League"]]
    else:
        ref = df_complet

    pct = percentile_joueur(ref, joueur, MAIN_STATS)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            radar(MAIN_STATS, [float(joueur[c]) for c in MAIN_STATS], "Notes absolues", nom),
            use_container_width=True,
        )
        st.caption(
            "Notes absolues : valeurs EA directement sur 100. Elles permettent de voir le niveau "
            "du joueur dans chaque grande caractéristique. Aucune normalisation supplémentaire n'est nécessaire."
        )

    with c2:
        st.plotly_chart(
            radar(list(pct.keys()), list(pct.values()), "Positionnement en percentiles", nom),
            use_container_width=True,
        )
        st.caption(
            f"Percentiles : position du joueur par rapport au groupe « {ref_mode.lower()} ». "
            "Par exemple, un percentile de 87 en PAC signifie que le joueur a une PAC supérieure "
            "ou égale à environ 87 % des joueurs du groupe de référence."
        )

    with st.expander("Comment lire les deux radars ?"):
        st.markdown(
            """
**Radar des notes absolues**  
Il répond à la question : *quel est le niveau du joueur ?* Les statistiques OVR, PAC, SHO, PAS, DRI, DEF et PHY sont déjà exprimées sur une échelle de 0 à 100.

**Radar des percentiles**  
Il répond à une autre question : *comment ce joueur se situe-t-il par rapport à des joueurs comparables ?* Une valeur de **90** ne signifie pas une note de 90/100 : elle signifie que le joueur se situe approximativement au-dessus de **90 % du groupe de référence** pour cette statistique.

Le choix **Même poste** est généralement le plus pertinent pour le recrutement : comparer la défense d'un attaquant à celle de tous les joueurs peut être moins informatif que de le comparer aux autres attaquants.
            """
        )

    st.subheader("Caractéristiques détaillées")
    for groupe, cols in PROFILE_GROUPS.items():
        vals = {
            c: joueur[c]
            for c in cols
            if c in joueur.index
            and not st.session_state.get("x", False)
            and str(joueur[c]) != "nan"
        }
        if vals:
            with st.expander(groupe, expanded=(groupe == "Général")):
                st.dataframe(
                    {"Statistique": list(vals.keys()), "Valeur": [round(float(v), 1) for v in vals.values()]},
                    use_container_width=True,
                    hide_index=True,
                )

    st.divider()
    st.subheader("Comparer avec un autre joueur")
    st.caption(
        "Sélectionnez un deuxième joueur pour comparer les mêmes indicateurs. "
        "Le radar superpose les deux profils avec des zones transparentes afin de conserver la lisibilité des recouvrements."
    )

    autre = st.selectbox(
        "Joueur de comparaison",
        [n for n in noms if n != nom],
        index=None,
        placeholder="Choisir un joueur",
    )

    if autre:
        j2 = base[base["Name"] == autre].sort_values("OVR", ascending=False).iloc[0]
        index_j2 = j2.name
        valeur_2 = _obtenir_valeur(df_complet, index_j2, j2, "comparaison")

        valeurs_1 = [float(joueur[c]) for c in MAIN_STATS]
        valeurs_2 = [float(j2[c]) for c in MAIN_STATS]

        st.plotly_chart(
            radar_comparaison(
                MAIN_STATS,
                valeurs_1,
                valeurs_2,
                nom,
                autre,
                "Comparaison des caractéristiques principales",
            ),
            use_container_width=True,
        )

        st.caption(
            "Plus le contour est éloigné du centre, plus la note est élevée. "
            "Les surfaces sont volontairement transparentes : les zones de chevauchement restent visibles."
        )

        lignes = []
        for stat in MAIN_STATS:
            v1, v2 = float(joueur[stat]), float(j2[stat])
            lignes.append(
                {"Indicateur": stat, nom: int(v1), autre: int(v2), "Différence": int(v1 - v2)}
            )

        diff_marche = None
        if valeur_1 is not None and valeur_2 is not None:
            diff_marche = formater_valeur(abs(valeur_1 - valeur_2))
            if valeur_1 - valeur_2 > 0:
                diff_marche = "+" + diff_marche
            elif valeur_1 - valeur_2 < 0:
                diff_marche = "-" + diff_marche
            else:
                diff_marche = "0 €"

        lignes.append(
            {
                "Indicateur": "Valeur Marchande",
                nom: formater_valeur(valeur_1),
                autre: formater_valeur(valeur_2),
                "Différence": diff_marche or "Non disponible",
            }
        )
        st.dataframe(lignes, use_container_width=True, hide_index=True)
        st.caption("Différence = joueur principal − joueur de comparaison. La valeur marchande n'est pas intégrée au radar.")
