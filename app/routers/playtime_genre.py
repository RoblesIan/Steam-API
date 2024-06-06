from fastapi import APIRouter, HTTPException
from app.models.schemas import PlayTimeGenreResponse
import pandas as pd
from app import database as db

"""
def PlayTimeGenre( genero : str ): Debe devolver año con mas horas jugadas para dicho género.
Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}
"""

router = APIRouter()

@router.get("/PlayTimeGenre", response_model=PlayTimeGenreResponse)
async def PlayTimeGenre(genero: str):
    # Lógica

    # Carga de datos con filtro de columnas: steam_games
    columns1 = ["item_id", "genres", "release_date"]
    steam_games_df = db.load_steam_games(columns1)
    #print("steam_games_df:", steam_games_df.head())

    """No hacemos la carga de ambos dataframe juntos para optimizar las consultas de modo que si no encontramos
        el género dado no se cargue el segundo dataframe y ahorramos espacio"""

    # Filtrar las filas donde la columna 'genres' no es None
    steam_games_df = steam_games_df.dropna(subset=['genres'])
    #print("steam_games_df after dropna:", steam_games_df.head())

    # Filtrar steam_games_df por el género proporcionado
    steam_games_df = steam_games_df[steam_games_df['genres'].apply(lambda genres: genero in genres)]
    #print("Filtered steam_games_df:", steam_games_df.head())

    # Verificar si se encontraron datos para el género dado
    if steam_games_df.empty:
        raise HTTPException(status_code=404, detail="No se encontraron juegos para el género proporcionado")

    # Carga de datos con filtro de columnas: user_items
    columns2 = ["item_id", "playtime_forever"]
    user_items_df = db.load_user_items(columns2)
    #print("user_items_df:", user_items_df.head())

    # Filtrar user_items_df por los item_id presentes en steam_games_df después de aplicar el filtro por género
    user_items_df = user_items_df[user_items_df['item_id'].isin(steam_games_df['item_id'])]
    #print("Filtered user_items_df:", user_items_df.head())

    # Verificar si se encontraron datos de horas jugadas para el género dado
    if user_items_df.empty:
        raise HTTPException(status_code=404, detail="No se encontraron datos de horas jugadas para el género proporcionado")

    # Sumar la columna playtime_forever agrupada por item_id en user_items_df
    user_items_df = user_items_df.groupby('item_id')['playtime_forever'].sum().reset_index()
    #print("Aggregated user_items_df:", user_items_df.head())

    # Obtener el registro con el máximo playtime_forever
    user_items_df = user_items_df.loc[user_items_df['playtime_forever'].idxmax()]
    #print("Max playtime_forever user_items_df:", user_items_df)

    # Buscar el registro correspondiente en steam_games_df
    steam_games_df = steam_games_df[steam_games_df['item_id'] == user_items_df['item_id']]
    #print("Final steam_games_df:", steam_games_df.head())

    return PlayTimeGenreResponse(año_mas_horas_jugadas=steam_games_df['release_date'].values[0], genero=genero)