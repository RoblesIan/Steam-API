from pydantic import BaseModel, Field
from typing import List, Dict, Any

# PlaytimeGenre modelo .
class PlayTimeGenreResponse(BaseModel):
    año_mas_horas_jugadas: int

# UserForGenre modelo .
class PlayTimeByYear(BaseModel):
    Año: int
    Horas: int

class UserForGenreResponse(BaseModel):
    usuario: str = Field(..., alias='Usuario con más horas jugadas para género X')
    horas_jugadas: List[PlayTimeByYear] = Field(..., alias='Horas jugadas')

    class Config:
        # Allow population by field name for alias handling
        allow_population_by_field_name = True

# UsersRecommend modelo .
class GameRecommendation(BaseModel):
    puesto: int
    juego: str

class UsersRecommendResponse(BaseModel):
    top_recomendados: List[GameRecommendation]

# UsersWorstDeveloper modelo .
class DeveloperRanking(BaseModel):
    puesto: int
    desarrolladora: str

class UsersWorstDeveloperResponse(BaseModel):
    top_desarrolladoras: List[DeveloperRanking]

# SentimentAnalysis modelo
class SentimentAnalysisResponse(BaseModel):
    empresa_desarrolladora: str
    sentiment_counts: Dict[str, int]