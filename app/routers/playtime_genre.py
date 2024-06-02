from fastapi import APIRouter, HTTPException
from app.models.schemas import PlayTimeGenreResponse
from app.database import load_steam_games, load_user_items
import pandas as pd

router = APIRouter()

@router.get("/PlayTimeGenre", response_model=PlayTimeGenreResponse)
async def PlayTimeGenre(genero: str):
    # lógica

    # carga de datos con filtro de columnas
    columns = ["item_id", "genres", "release_date"]
    steam_games_df = load_steam_games(columns)

    columns = ["item_id", "playtime_forever"]
    user_items_df = load_user_items(columns)

    # Filtrar las filas donde la columna 'genres' no es None
    steam_games_df = steam_games_df.dropna(subset=['genres'])

    # Filtrar steam_games_df por el género proporcionado
    steam_games_df = steam_games_df[steam_games_df['genres'].apply(lambda genres: genero in genres)]

    # Verificar si se encontraron datos para el género dado
    if steam_games_df.empty:
        raise HTTPException(status_code=404, detail="No se encontraron juegos para el género proporcionado")

    # Filtrar user_items_df por los item_id presentes en steam_games_df después de aplicar el filtro por género
    user_items_df = user_items_df[user_items_df['item_id'].isin(steam_games_df['item_id'])]

    # Verificar si se encontraron datos de horas jugadas para el género dado
    if user_items_df.empty:
        raise HTTPException(status_code=404, detail="No se encontraron datos de horas jugadas para el género proporcionado")

    # Sumar la columna playtime_forever agrupada por item_id en user_items_df
    user_items_df = user_items_df.groupby('item_id')['playtime_forever'].sum().reset_index()

    # Obtener el registro con el máximo playtime_forever
    user_items_df = user_items_df.loc[user_items_df['playtime_forever'].idxmax()]

    # Buscar el registro correspondiente en steam_games_df
    steam_games_df = steam_games_df[steam_games_df['item_id'] == user_items_df['item_id']]

    return PlayTimeGenreResponse(año_mas_horas_jugadas=steam_games_df['release_date'], genero=genero)