from fastapi import APIRouter
from app.models.schemas import UserForGenreResponse
router = APIRouter()

@router.get("/UserForGenre", response_model=UserForGenreResponse)
async def UserForGenre(genero: str):
    # lógica
    user_id = "us213ndjss09sdf"
    playtimes = [
        {"Año": 2013, "Horas": 203},
        {"Año": 2012, "Horas": 100},
        {"Año": 2011, "Horas": 23}
    ]
    response_data = {
        f"Usuario con más horas jugadas para género {genero}": user_id,
        "Horas jugadas": playtimes
    }
    return response_data