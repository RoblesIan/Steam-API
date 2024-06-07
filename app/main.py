# Imports
from fastapi import FastAPI
from app.routers import playtime_genre, user_for_genre, users_recommend, users_worst_developer, sentiment_analysis

# Instanciamos FastAPI
app = FastAPI()

# Ruta raíz
@app.get("/")
def root():
    return {"mensaje": "Bienvenidos a la API de Steam"}

# Importa routers desde archivos de rutas y añadirlos en la aplicación
app.include_router(playtime_genre.router)
app.include_router(user_for_genre.router)
app.include_router(users_recommend.router)
app.include_router(users_worst_developer.router)
app.include_router(sentiment_analysis.router)