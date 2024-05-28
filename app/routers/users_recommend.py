from fastapi import APIRouter
from app.models.schemas import UsersRecommendResponse
router = APIRouter()

@router.get("/UsersRecommend", response_model=UsersRecommendResponse)
async def UsersRecommend(año: int):
    # lógica
    juegos_recomendados = [
        {"puesto": 1, "juego": "The Witcher 3: Wild Hunt"},
        {"puesto": 2, "juego": "Red Dead Redemption 2"},
        {"puesto": 3, "juego": "Grand Theft Auto V"}
    ]
    return {"top_recomendados": juegos_recomendados}