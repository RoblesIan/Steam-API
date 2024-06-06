from fastapi import APIRouter, HTTPException
from app.models.schemas import UsersRecommendResponse
import pandas as pd
from app import database as db

"""
def UsersRecommend( año : int ): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. 
(reviews.recommend = True y comentarios positivos/neutrales)
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
"""

router = APIRouter()

@router.get("/UsersRecommend", response_model=UsersRecommendResponse)
async def UsersRecommend(año: int):
    # lógica

    # Carga de datos con filtro de columnas: user_reviews
    columns1 = ["item_id", "posted", "sentiment_analysis"]
    user_reviews_df = db.load_user_reviews(columns1)
    print(f"shape: {user_reviews_df.shape} \n {user_reviews_df} carga")

    # Como solo dimos soporte a reviews en ingles y reviews vacias con recommend, filtramos los user_reviews_df != pd.NA
    user_reviews_df = user_reviews_df[user_reviews_df['sentiment_analysis'].notna()]
    print(f"shape: {user_reviews_df.shape} \n {user_reviews_df} filtro != pd.NA")

    # Filtrar user_reviews por el año proporcionado
    user_reviews_df = user_reviews_df[user_reviews_df['posted'] == año]
    print(f"shape: {user_reviews_df.shape} \n {user_reviews_df} filtro año dado")

    # Verificar si se encontraron datos para el género dado
    if user_reviews_df.empty:
        raise HTTPException(status_code=404, detail="No se encontraron reseñas para el año dado")

    # Carga de datos con filtro de columnas: steam_games
    columns2 = ["item_id", "app_name"]
    steam_games_df = db.load_steam_games(columns2)

    # Eliminamos la columna user_reviews.posted, ya que no la vamos a utilizar mas
    user_reviews_df.drop(columns=['posted'], inplace=True)
    print(f"shape: {user_reviews_df.shape} \n {user_reviews_df} eliminamos columna posted")

    # Agrupamos por user_reviews.item_id y sumamos por user_reviews_df.sentiment_analysis
    user_reviews_df  = user_reviews_df.groupby('item_id')['sentiment_analysis'].sum().reset_index()
    print(f"shape: {user_reviews_df.shape} \n {user_reviews_df} groupby sum")

    # Ordenar el DataFrame por la columna 'sentiment_analysis' de forma descendente
    user_reviews_df = user_reviews_df.sort_values(by='sentiment_analysis', ascending=False)
    print(f"shape: {user_reviews_df.shape} \n {user_reviews_df} sort ascendant")

    # Seleccionar solo los top 3 item_id
    user_reviews_df = user_reviews_df['item_id'].head(3)
    print(f"shape: {user_reviews_df.shape} \n {user_reviews_df} only first 3")

    # Unir user_reviews_df con steam_games_df para obtener los nombres de los juegos
    user_reviews_df = pd.merge(user_reviews_df, steam_games_df[['item_id', 'app_name']], on='item_id', how='left')
    print(f"shape: {user_reviews_df.shape} \n {user_reviews_df} merge")

    # Eliminar la columna 'item_id'
    user_reviews_df.drop(columns=['item_id'], inplace=True)
    print(f"shape: {user_reviews_df.shape} \n {user_reviews_df} drop item_id")

    # Crear lista de recomendaciones
    top_recomendados = [
        {"puesto": i + 1, "juego": game} for i, game in enumerate(user_reviews_df['app_name'])
    ]
    print(f"tipo de dato: {type(top_recomendados)} \ncontenido: {top_recomendados}")
    return UsersRecommendResponse(top_recomendados_para_el_año=año, top_recomendados=top_recomendados)


















    juegos_recomendados = [
        {"puesto": 1, "juego": "The Witcher 3: Wild Hunt"},
        {"puesto": 2, "juego": "Red Dead Redemption 2"},
        {"puesto": 3, "juego": "Grand Theft Auto V"}
    ]
    return {"top_recomendados": juegos_recomendados}