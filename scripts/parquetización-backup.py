# imports
import pandas as pd
import json
import ast
import os

# renombré a mano los json tal que:
# Definimos rutas
ruta_steam_games_json = '../backup/steam_games.json'
ruta_user_items_json = '../backup/user_items.json'
ruta_user_reviews_json = '../backup/user_reviews.json'

ruta_steam_games_parquet = '../backup/steam_games.parquet'
ruta_user_items_parquet = '../backup/user_items.parquet'
ruta_user_reviews_parquet = '../backup/user_reviews.parquet'

# Pasamos de JSON a dataframes
lista = []
with open(ruta_steam_games_json, 'r', encoding='utf-8') as file:
    for linea in file.readlines():
        lista.append(json.loads(linea))
df_steam_games = pd.DataFrame(lista)

lista = []
with open(ruta_user_items_json, 'r', encoding='utf-8') as file:
    for linea in file.readlines():
        lista.append(ast.literal_eval(linea))
df_user_items = pd.DataFrame(lista)

lista = []
with open(ruta_user_reviews_json, 'r', encoding='utf-8') as file:
    for linea in file.readlines():
        lista.append(ast.literal_eval(linea))
df_user_reviews = pd.DataFrame(lista)

# Pasar los archivos a parquet da error, los cuales vamos solucionando aca:

    # Pasamos la columna price a tipo str, porque pasarlo a int requiere una limpieza mayor
df_steam_games['price'] = df_steam_games['price'].astype(str)

# Pasamos de dataframes a parquet
df_steam_games.to_parquet(ruta_steam_games_parquet)
df_user_items.to_parquet(ruta_user_items_parquet)
df_user_reviews.to_parquet(ruta_user_reviews_parquet)

# Eliminamos los archivos JSON originales
os.remove(ruta_steam_games_json)
os.remove(ruta_user_items_json)
os.remove(ruta_user_reviews_json)

# Eliminamos de memoria los DataFrames
del df_steam_games
del df_user_items
del df_user_reviews