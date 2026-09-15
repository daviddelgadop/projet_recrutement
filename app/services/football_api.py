import requests
import streamlit as st

BASE_URL = "https://live-football-api.com/api/v1"


def _api_key():
    try:
        return st.secrets["FOOTBALL_API_KEY"]
    except (KeyError, FileNotFoundError):
        return None


def api_configuree():
    return bool(_api_key())


@st.cache_data(ttl=3600, show_spinner=False)
def rechercher_joueurs(nom):
    cle = _api_key()
    if not cle:
        raise RuntimeError("Clé FOOTBALL_API_KEY absente de .streamlit/secrets.toml")

    r = requests.get(
        f"{BASE_URL}/player_search",
        params={"api_key": cle, "q": nom, "lang": "en"},
        timeout=15,
    )
    r.raise_for_status()
    payload = r.json()
    if not payload.get("success"):
        raise RuntimeError(payload.get("message", "Erreur lors de la recherche du joueur"))
    return payload.get("data", {}).get("players", [])


@st.cache_data(ttl=3600, show_spinner=False)
def recuperer_profil(player_id):
    cle = _api_key()
    if not cle:
        raise RuntimeError("Clé FOOTBALL_API_KEY absente de .streamlit/secrets.toml")

    r = requests.get(
        f"{BASE_URL}/player",
        params={"api_key": cle, "player_id": player_id, "lang": "en"},
        timeout=15,
    )
    r.raise_for_status()
    payload = r.json()
    if not payload.get("success"):
        raise RuntimeError(payload.get("message", "Erreur lors de la récupération du joueur"))
    return payload.get("data", {})
