from fastapi import APIRouter
from ..models.schemas import SentimentAnalysisResponse
router = APIRouter()

@router.get("/SentimentAnalysis", response_model=SentimentAnalysisResponse)
async def SentimentAnalysis(empresa_desarrolladora: str):
    # lógica
    analisis_sentimiento = {
        "Negative": 182,
        "Neutral": 120,
        "Positive": 278
    }
    return SentimentAnalysisResponse(empresa_desarrolladora=empresa_desarrolladora, sentiment_counts=analisis_sentimiento)
