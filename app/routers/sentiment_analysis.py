from fastapi import APIRouter, HTTPException
from app.models.schemas import SentimentAnalysisResponse
from app import database as db
import pandas as pd

"""
def sentiment_analysis( empresa desarrolladora : str ): Según la empresa desarrolladora, se devuelve un diccionario 
con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios
que se encuentren categorizados con un análisis de sentimiento como valor.
Ejemplo de retorno: {'Valve' : [Negative = 182, Neutral = 120, Positive = 278]}

"""
router = APIRouter()

@router.get("/SentimentAnalysis", response_model=SentimentAnalysisResponse)
async def SentimentAnalysis(empresa_desarrolladora: str):
    # lógica

    # Cargar los datos de juegos de Steam y filtrarlos por la empresa desarrolladora
    steam_games_df = db.load_steam_games(["item_id", "developer"])
    steam_games_df = steam_games_df[steam_games_df["developer"] == empresa_desarrolladora]
    print(f"carga y filtro por empresa_desarrolladora \n {empresa_desarrolladora}")

    # Verificar si se encontraron desarrolladoras para la empresa desarrolladora dada
    if steam_games_df.empty:
        raise HTTPException(status_code=404, detail="No se encontraron empresas desarrolladoras que coincidan con los datos dados")
    
    # Cargar los datos de reseñas de usuarios
    user_reviews_df = db.load_user_reviews(["item_id", "sentiment_analysis"])
    print(f"carga user_reviews \n {user_reviews_df}")

    # Filtrar las reseñas para que solo incluyan los juegos de la empresa desarrolladora dada
    user_reviews_df = user_reviews_df[user_reviews_df["item_id"].isin(steam_games_df["item_id"])]
    print(f"filtro para que solo incluyan los registros que item_id de la empresa desarrolladora dada \n {user_reviews_df}")

    # Verificar si se encontraron reseñas para los juegos de la empresa desarrolladora dada
    if user_reviews_df.empty:
        raise HTTPException(status_code=404, detail="No se encontraron reseñas para la empresa desarrolladora dada")

    # Mapear los valores de sentiment_analysis a categorías
    sentiment_map = {0.0: "Negative", 1.0: "Neutral", 2.0: "Positive"}
    user_reviews_df['sentiment_analysis'] = user_reviews_df['sentiment_analysis'].map(sentiment_map)
    print(f"Mapeo de sentimientos \n {user_reviews_df}")

    # Contar las reseñas por cada categoría de análisis de sentimiento
    sentiment_counts = user_reviews_df["sentiment_analysis"].value_counts().to_dict()
    print(f"calculamos sentiment_counts \n {sentiment_counts}")

    # Asegurar que todas las categorías de sentimiento estén presentes en el diccionario
    sentiment_counts = {sentiment: sentiment_counts.get(sentiment, 0) for sentiment in ["Negative", "Neutral", "Positive"]}
    print(f"aseguramos categorias \n {sentiment_counts}")

    return SentimentAnalysisResponse(empresa_desarrolladora=empresa_desarrolladora, sentiment_counts=sentiment_counts)
