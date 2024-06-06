import pandas as pd
import os

# Obtener la ruta absoluta del directorio actual (donde está este archivo)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Funciones que cargan los datos desde los parquets hacia df's con columnas específicas
def load_steam_games(columns=None):
    path = os.path.join(BASE_DIR, "..", "data", "steam_games.parquet")
    return pd.read_parquet(path, engine='pyarrow', columns=columns)

def load_user_items(columns=None):
    path = os.path.join(BASE_DIR, "..", "data", "user_items.parquet")
    return pd.read_parquet(path, engine='pyarrow', columns=columns)

def load_user_info(columns=None):
    path = os.path.join(BASE_DIR, "..", "data", "user_info.parquet")
    return pd.read_parquet(path, engine='pyarrow', columns=columns)

def load_user_reviews(columns=None):
    path = os.path.join(BASE_DIR, "..", "data", "user_reviews.parquet")
    return pd.read_parquet(path, engine='pyarrow', columns=columns)
