import pandas as pd

# Funciones que cargan los datos desde los parquets hacia df's con columnas especificas
def load_steam_games(columns=None):
    return pd.read_parquet("../../data/steam_games.parquet", columns=columns)

def load_user_items(columns=None):
    return pd.read_parquet("../../data/user_items.parquet", columns=columns)

def load_user_info(columns=None):
    return pd.read_parquet("../../data/user_info.parquet", columns=columns)

def load_user_reviews(columns=None):
    return pd.read_parquet("../../data/user_reviews.parquet", columns=columns)