from fastapi import APIRouter
from ..models.schemas import UsersWorstDeveloperResponse
router = APIRouter()

@router.get("/UsersWorstDeveloper", response_model=UsersWorstDeveloperResponse)
async def UsersWorstDeveloper(año: int):
    # lógica
    desarrolladoras_menos_recomendadas = [
        {"puesto": 1, "desarrolladora": "EA"},
        {"puesto": 2, "desarrolladora": "Ubisoft"},
        {"puesto": 3, "desarrolladora": "Bethesda"}
    ]
    return {"top_desarrolladoras": desarrolladoras_menos_recomendadas}