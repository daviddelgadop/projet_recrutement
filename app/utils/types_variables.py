import pandas as pd
from app.constants.colonnes import ID_COLUMNS

def colonnes_quantitatives(df):
    return [c for c in df.select_dtypes(include="number").columns if c not in ID_COLUMNS]

def colonnes_qualitatives(df):
    return [c for c in df.select_dtypes(exclude="number").columns if c not in ID_COLUMNS]

def type_variable(df, col):
    return "quantitative" if pd.api.types.is_numeric_dtype(df[col]) else "qualitative"
