import pandas as pd

def load_steam_games():
    return pd.read_parquet("../data/steam_games.parquet")

def load_user_items():
    return pd.read_parquet("../data/user_items.parquet")

def load_user_info():
    return pd.read_parquet("../data/user_info.parquet")

def load_user_reviews():
    return pd.read_parquet("../data/user_reviews.parquet")