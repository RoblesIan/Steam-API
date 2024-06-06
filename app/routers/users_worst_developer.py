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
    columns1 = ["item_id", "posted", "sentiment_analysis"]
    user_reviews_df = db.load_user_reviews(columns1)
    print(f" carga \n shape: {user_reviews_df.shape} \n {user_reviews_df}")

    # Como solo dimos soporte a reviews en ingles y reviews vacias con recommend, filtramos los user_reviews_df != pd.NA
    user_reviews_df = user_reviews_df[user_reviews_df['sentiment_analysis'].notna()]
    print(f" filtro != pd.NA \n shape: {user_reviews_df.shape} \n {user_reviews_df}")

    # Filtrar user_reviews por el año proporcionado
    user_reviews_df = user_reviews_df[user_reviews_df['posted'] == año]
    print(f" filtro año dado \n shape: {user_reviews_df.shape} \n {user_reviews_df}")

    # Verificar si se encontraron datos para el género dado
    if user_reviews_df.empty:
        raise HTTPException(status_code=404, detail="No se encontraron reseñas para el año dado")

    # Carga de datos con filtro de columnas: steam_games
    columns2 = ["item_id", "developer"]
    steam_games_df = db.load_steam_games(columns2)

    # Eliminamos la columna user_reviews.posted, ya que no la vamos a utilizar mas
    user_reviews_df.drop(columns=['posted'], inplace=True)
    print(f" eliminamos columna posted \n shape: {user_reviews_df.shape} \n {user_reviews_df}")

    # Unir user_reviews_df con steam_games_df para obtener los nombres de las desarrolladoras
    user_reviews_df = pd.merge(user_reviews_df, steam_games_df[['item_id', 'developer']], on='item_id', how='left')
    print(f" merge \n shape: {user_reviews_df.shape} \n {user_reviews_df}")

    # Calcular el total de reseñas y el número de reseñas negativas para cada desarrolladora
    total_reviews = user_reviews_df.groupby('developer')['sentiment_analysis'].count().reset_index(name='total_reviews')
    negative_reviews = user_reviews_df[user_reviews_df['sentiment_analysis'] == 0].groupby('developer')['sentiment_analysis'].count().reset_index(name='negative_reviews')
    print(f" calculo de reseñas \n shapes: {total_reviews.shape}, {negative_reviews.shape} \n total reviews \n {user_reviews_df} \n \n negative reviews \n {negative_reviews}")

    # Unir ambos DataFrames por la columna 'developer'
    developers_reviews_df = pd.merge(total_reviews, negative_reviews, on='developer', how='left')
    print(f"unimos total con negative \n {developers_reviews_df}")

    # Rellenar NaN en negative_reviews con 0
    developers_reviews_df['negative_reviews'] = developers_reviews_df['negative_reviews'].fillna(0)

    # Calcular la proporción de reseñas negativas
    developers_reviews_df['negative_proportion'] = developers_reviews_df['negative_reviews'] / developers_reviews_df['total_reviews']
    print(f"calculamos la proporcion de reseñas negativas \n {developers_reviews_df}")

    # Ordenar por la proporción de reseñas negativas de forma descendente (mayor a menor)
    developers_reviews_df = developers_reviews_df.sort_values(by='negative_proportion', ascending=False)
    print(f"ordenamos de forma descendente \n {developers_reviews_df}")

    # Seleccionar solo las top 3 desarrolladoras con mayor proporción de reseñas negativas
    developers_reviews_df = developers_reviews_df.head(3).reset_index(drop=True)
    print(f"top 3 {developers_reviews_df}")

    # Crear lista de desarrolladores con mayor proporción de reseñas negativas
    top_worst_developers_list = [
        {"puesto": i + 1, "desarrolladora": row['developer']} 
        for i, row in developers_reviews_df.iterrows()
    ]

    return UsersWorstDeveloperResponse(
        top_peores_desarrolladoras_para_el_año=año,
        top_peores_desarrolladoras=top_worst_developers_list
    )