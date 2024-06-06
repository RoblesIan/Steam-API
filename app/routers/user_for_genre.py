from fastapi import APIRouter, HTTPException
from app.models.schemas import PlayTimeByYear, UserForGenreResponse
import pandas as pd
from app import database as db

"""
def UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista
de la acumulación de horas jugadas por año.
Ejemplo de retorno: 
{"Usuario con más horas jugadas para Género X" : "us213ndjss09sdf", 
"Horas jugadas":[{"Año": 2013, "Horas": 203}, {"Año": 2012, "Horas": 100}, {"Año": 2011, "Horas": 23}]}
"""

router = APIRouter()

@router.get("/UserForGenre", response_model=UserForGenreResponse)
async def UserForGenre(genero: str):
    # Lógica

    # Carga de datos con filtro de columnas: steam_games
    columns1 = ["item_id", "genres", "release_date"]
    steam_games_df = db.load_steam_games(columns1)

    # Filtrar las filas donde la columna 'genres' no es None
    steam_games_df = steam_games_df.dropna(subset=['genres'])

    # Filtrar steam_games_df por el género proporcionado
    steam_games_df = steam_games_df[steam_games_df['genres'].apply(lambda genres: genero in genres)]

    # Verificar si se encontraron datos para el género dado
    if steam_games_df.empty:
        raise HTTPException(status_code=404, detail="No se encontraron juegos para el género proporcionado")

    # Carga de datos con filtro de columnas: user_items
    columns2 = ["user_id", "item_id", "playtime_forever"]
    user_items_df = db.load_user_items(columns2)

    # Filtrar user_items_df por los item_id presentes en steam_games_df después de aplicar el filtro por género
    user_items_df = user_items_df[user_items_df['item_id'].isin(steam_games_df['item_id'])]

    # Verificar si se encontraron datos de horas jugadas para el género dado
    if user_items_df.empty:
        raise HTTPException(status_code=404, detail="No se encontraron datos de horas jugadas para el género proporcionado")

    # Obtener el registro con el máximo playtime_forever, luego de hacer groupby user_id sumando la columna playtime_forever
    user_max_playtime_forever_registered_df  = user_items_df.groupby('user_id')['playtime_forever'].sum().reset_index()
    user_max_playtime_forever_registered_df  = user_items_df.loc[user_items_df['playtime_forever'].idxmax()]

    # Extraer el usuario de user_max_playtime_forever_registered_df
    user_max_playtime_forever_registered = user_max_playtime_forever_registered_df['user_id']

    # Eliminar el DataFrame que contiene al usuario
    del user_max_playtime_forever_registered_df

    # Filtrar user_items_df por el user_id con el máximo playtime_forever
    user_items_df = user_items_df[user_items_df['user_id'] == user_max_playtime_forever_registered]

    # Filtrar steam_games_df por los items del usuario con mayor horas registradas para el género dado presentes en user_items_df
    steam_games_df = steam_games_df[steam_games_df['item_id'].isin(user_items_df['item_id'])]

    # Concatenar la columna release_date de steam_games_df a user_items_df
    user_items_df = pd.merge(user_items_df, steam_games_df[['item_id', 'release_date']], on='item_id', how='left')

    # Agrupar por release_date y sumar playtime_forever
    user_items_df = user_items_df.groupby('release_date')['playtime_forever'].sum().reset_index()

    # Eliminar el DataFrame steam_games_df que ya no tiene información relevante
    del steam_games_df

    # Preparar la respuesta con los años y las horas jugadas
    playtimes = [PlayTimeByYear(Año=row['release_date'], Horas=row['playtime_forever']) for _, row in user_items_df.iterrows()]
    
    # Devolver la respuesta utilizando el modelo UserForGenreResponse directamente
    return UserForGenreResponse(
        genero=genero,
        usuario_con_mas_horas_jugadas=user_max_playtime_forever_registered,
        horas_jugadas=playtimes
    )

