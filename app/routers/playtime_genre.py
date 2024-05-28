from fastapi import APIRouter
from app.models.schemas import PlayTimeGenreResponse

router = APIRouter()

@router.get("/PlayTimeGenre", response_model=PlayTimeGenreResponse)
async def PlayTimeGenre(genero: str):
    # lógica
    return {"Año de lanzamiento con más horas jugadas para Género X": 2013}