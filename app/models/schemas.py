from pydantic import BaseModel, Field
from typing import List, Dict, Any

# PlaytimeGenre modelo .
class PlayTimeGenreResponse(BaseModel):
    año_mas_horas_jugadas: int
    genero: str

# PlayTimeByYear modelo.
class PlayTimeByYear(BaseModel):
    Año: int
    Horas: int

class UserForGenreResponse(BaseModel):
    genero: str
    usuario_con_mas_horas_jugadas: str
    horas_jugadas: List[PlayTimeByYear]

# UsersRecommend modelo .
class GameRecommendation(BaseModel):
    puesto: int
    juego: str

class UsersRecommendResponse(BaseModel):
    top_recomendados_para_el_año: int
    top_recomendados: List[GameRecommendation]

# UsersWorstDeveloper modelo .
class DeveloperRanking(BaseModel):
    puesto: int
    desarrolladora: str

class UsersWorstDeveloperResponse(BaseModel):
    top_peores_desarrolladoras_para_el_año: int
    top_peores_desarrolladoras: List[DeveloperRanking]

# SentimentAnalysis modelo
class SentimentAnalysisResponse(BaseModel):
    empresa_desarrolladora: str
    sentiment_counts: Dict[str, int]