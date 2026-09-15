import pandas as pd
from app.constants.config import DATA_PATH
from app.utils.market_value import garantir_colonnes_marche


def charger_donnees():
    df = pd.read_csv(DATA_PATH)
    return garantir_colonnes_marche(df, sauvegarder=True)
