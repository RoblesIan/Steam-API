from fastapi import APIRouter, HTTPException
from app.models.schemas import UsersWorstDeveloperResponse
import pandas as pd
from app import database as db

"""
def UsersWorstDeveloper( año : int ): Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios 
para el año dado. (reviews.recommend = False y comentarios negativos)
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
"""

router = APIRouter()

@router.get("/UsersWorstDeveloper", response_model=UsersWorstDeveloperResponse)
async def UsersWorstDeveloper(año: int):
    # lógica

    # Carga de datos con filtro de columnas: user_reviews
    user_reviews_df = db.load_user_reviews(["item_id", "posted", "sentiment_analysis"])

    # Filtrar por año dado y reseñas no vacías
    user_reviews_df = user_reviews_df[user_reviews_df['posted'] == año]
    user_reviews_df = user_reviews_df[user_reviews_df['sentiment_analysis'].notna()]

    # Verificar si se encontraron datos para el año dado
    if user_reviews_df.empty:
        raise HTTPException(status_code=404, detail="No se encontraron reseñas para el año dado")

    # Carga de datos con filtro de columnas: steam_games
    steam_games_df = db.load_steam_games(["item_id", "developer"])

    # Unir user_reviews_df con steam_games_df para obtener los nombres de las desarrolladoras
    user_reviews_df = pd.merge(user_reviews_df[['item_id', 'sentiment_analysis']], steam_games_df, on='item_id', how='left')

    # Calcular el total de reseñas y el número de reseñas negativas para cada desarrolladora
    reviews_summary = user_reviews_df.groupby('developer').agg(
        total_reviews=('sentiment_analysis', 'count'),
        negative_reviews=('sentiment_analysis', lambda x: (x == 0).sum())
    ).reset_index()

    # Calcular la proporción de reseñas negativas
    reviews_summary['negative_proportion'] = reviews_summary['negative_reviews'] / reviews_summary['total_reviews']

    # Ordenar por la proporción de reseñas negativas de forma descendente y seleccionar las top 3 desarrolladoras
    top_worst_developers_df = reviews_summary.sort_values(by='negative_proportion', ascending=False).head(3).reset_index(drop=True)

    # Crear lista de desarrolladores con mayor proporción de reseñas negativas
    
    top_worst_developers_list = [
        {"puesto": i + 1, "desarrolladora": row['developer']}
        for i, row in top_worst_developers_df.iterrows()
    ]

    return UsersWorstDeveloperResponse(
        top_peores_desarrolladoras_para_el_año=año,
        top_peores_desarrolladoras=top_worst_developers_list
    )