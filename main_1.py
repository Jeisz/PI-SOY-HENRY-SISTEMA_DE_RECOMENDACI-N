from fastapi import FastAPI, HTTPException
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = FastAPI()

# Cargar el dataset (asegúrate de ajustar el path según tu archivo)
df_combines = pd.read_parquet('movies_dataset.parquet')
# Cargar el dataset del modelo de recomendacion
df_sample = pd.read_parquet('movies_dataset_reduced_sample.parquet')

@app.get("/")
def read_root():
    return {"message": "Hola Mundo"}

@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    # Filtrar por el estado 'Released'
    df_released = df_combines[df_combines['status'] == 'Released']
    
    # Contar las películas por mes
    mes = mes.lower()
    cantidad = df_released[df_released['mes'] == mes].shape[0]
    return {"message": f"{cantidad} películas fueron estrenadas en el mes de {mes.capitalize()}"}

@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    # Filtrar por el estado 'Released'
    df_released = df_combines[df_combines['status'] == 'Released']
    
    # Contar las películas por día de la semana
    dia = dia.lower()
    cantidad = df_released[df_released['dia_semana'] == dia].shape[0]
    return {"message": f"{cantidad} películas fueron estrenadas en los días {dia.capitalize()}"}

@app.get("/score_titulo/{titulo_de_la_filmacion}")
def score_titulo(titulo_de_la_filmacion: str):
    # Filtrar por el título de la filmación (hacemos la comparación más flexible)
    film = df_combines[df_combines['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)]
    
    if not film.empty:
        film = film.iloc[0]
        titulo = film['title']
        anio = film['release_date'].year
        score = film['popularity']
        return {"message": f"La película {titulo} fue estrenada en el año {anio} con un score/popularidad de {score}"}
    else:
        raise HTTPException(status_code=404, detail="Película no encontrada")

@app.get("/votos_titulo/{titulo_de_la_filmacion}")
def votos_titulo(titulo_de_la_filmacion: str):
    # Filtrar por el título de la filmación
    film = df_combines[df_combines['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)]
    
    if not film.empty:
        film = film.iloc[0]
        if film['vote_count'] >= 2000:
            titulo = film['title']
            anio = film['release_date'].year
            total_votos = film['vote_count']
            promedio_votos = film['vote_average']
            return {"message": f"La película {titulo} fue estrenada en el año {anio}. La misma cuenta con un total de {total_votos} valoraciones, con un promedio de {promedio_votos}"}
        else:
            return {"message": "La película no cumple con la condición de tener al menos 2000 valoraciones"}
    else:
        raise HTTPException(status_code=404, detail="Película no encontrada")

@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    # Filtrar por las filas que contienen información del elenco (cast)
    df_cast = df_combines.dropna(subset=['cast'])

    # Crear variables para almacenar la cantidad de películas y el retorno total
    total_peliculas = 0
    total_retorno = 0

    # Iterar sobre las filas del dataframe
    for index, row in df_cast.iterrows():
        # Separar la cadena de actores por comas y verificar si el actor está en la lista
        cast_list = [actor.strip() for actor in row['cast'].split(',')]
        if nombre_actor.lower() in [actor.lower() for actor in cast_list]:
            total_peliculas += 1
            total_retorno += row['revenue'] - row['budget']

    # Calcular el promedio de retorno
    if total_peliculas > 0:
        promedio_retorno = total_retorno / total_peliculas
        return {
            "message": f"El actor {nombre_actor} ha participado de {total_peliculas} cantidad de filmaciones, el mismo ha conseguido un retorno de {total_retorno} con un promedio de {promedio_retorno} por filmación"
        }
    else:
        return {"message": "Actor no encontrado o no tiene suficientes participaciones"}

@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str):
    # Filtrar por las filas que contienen información del equipo (crew)
    df_director = df_combines[df_combines['director'].str.lower() == nombre_director.lower()]

    # Crear variables para almacenar la cantidad de películas y el retorno total
    total_peliculas = df_director.shape[0]
    total_retorno = (df_director['revenue'] - df_director['budget']).sum()
    peliculas_info = df_director[['title', 'release_date', 'revenue', 'budget']].copy()
    peliculas_info['retorno_individual'] = peliculas_info['revenue'] - peliculas_info['budget']
    peliculas_info.rename(columns={'title': 'titulo', 'release_date': 'fecha_lanzamiento', 'revenue': 'ganancia', 'budget': 'costo'}, inplace=True)

    # Calcular el promedio de retorno
    if total_peliculas > 0:
        promedio_retorno = total_retorno / total_peliculas
        return {
            "message": f"El director {nombre_director} ha participado de {total_peliculas} cantidad de filmaciones, el mismo ha conseguido un retorno de {total_retorno} con un promedio de {promedio_retorno} por filmación",
            "peliculas": peliculas_info.to_dict(orient='records')
        }
    else:
        return {"message": "Director no encontrado o no tiene suficientes participaciones"}

