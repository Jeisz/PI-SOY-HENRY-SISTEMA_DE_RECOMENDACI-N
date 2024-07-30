from fastapi import FastAPI, HTTPException
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = FastAPI()

# Cargar el dataset (asegúrate de ajustar el path según tu archivo)
df_combines = pd.read_parquet('movies_dataset.parquet')

# Reducir el dataset a los títulos necesarios para la recomendación
df_sample = df_combines[['title']].dropna().reset_index(drop=True)

# Diccionarios de mapeo para meses y días
meses = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
}
dias_semana = {
    "lunes": 0, "martes": 1, "miércoles": 2, "jueves": 3,
    "viernes": 4, "sábado": 5, "domingo": 6
}

# Convertir las fechas en el dataframe al cargarlo
df_combines['release_date'] = pd.to_datetime(df_combines['release_date'], errors='coerce')

@app.get("/")
def read_root():
    return {"message": "Hola Mundo"}

@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    mes = mes.lower()
    if mes not in meses:
        raise HTTPException(status_code=400, detail="Mes inválido")
    
    mes_num = meses[mes]
    df_combines['mes'] = df_combines['release_date'].dt.month
    cantidad = df_combines[(df_combines['status'] == 'Released') & (df_combines['mes'] == mes_num)].shape[0]
    return {"message": f"{cantidad} películas fueron estrenadas en el mes de {mes.capitalize()}"}

@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    dia = dia.lower()
    if dia not in dias_semana:
        raise HTTPException(status_code=400, detail="Día de la semana inválido")
    
    dia_num = dias_semana[dia]
    df_combines['dia_semana'] = df_combines['release_date'].dt.dayofweek
    cantidad = df_combines[(df_combines['status'] == 'Released') & (df_combines['dia_semana'] == dia_num)].shape[0]
    return {"message": f"{cantidad} películas fueron estrenadas en los días {dia.capitalize()}"}

@app.get("/score_titulo/{titulo_de_la_filmacion}")
def score_titulo(titulo_de_la_filmacion: str):
    film = df_combines[df_combines['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)]
    if not film.empty:
        film = film.iloc[0]
        if pd.notna(film['release_date']):
            anio = film['release_date'].year
            return {"message": f"La película {film['title']} fue estrenada en el año {anio} con un score/popularidad de {film['popularity']}"}
        else:
            return {"message": f"La película {film['title']} tiene una fecha de lanzamiento inválida con un score/popularidad de {film['popularity']}"}
    else:
        raise HTTPException(status_code=404, detail="Película no encontrada")

@app.get("/votos_titulo/{titulo_de_la_filmacion}")
def votos_titulo(titulo_de_la_filmacion: str):
    film = df_combines[df_combines['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)]
    if not film.empty:
        film = film.iloc[0]
        if film['vote_count'] >= 2000:
            if pd.notna(film['release_date']):
                anio = film['release_date'].year
                return {"message": f"La película {film['title']} fue estrenada en el año {anio}. La misma cuenta con un total de {film['vote_count']} valoraciones, con un promedio de {film['vote_average']}"}
            else:
                return {"message": f"La película {film['title']} tiene una fecha de lanzamiento inválida. La misma cuenta con un total de {film['vote_count']} valoraciones, con un promedio de {film['vote_average']}"}
        else:
            return {"message": "La película no cumple con la condición de tener al menos 2000 valoraciones"}
    else:
        raise HTTPException(status_code=404, detail="Película no encontrada")

@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    df_cast = df_combines.dropna(subset=['cast'])
    df_cast['cast_list'] = df_cast['cast'].str.lower().str.split(',').apply(lambda x: [actor.strip() for actor in x])
    df_actor_films = df_cast[df_cast['cast_list'].apply(lambda x: nombre_actor.lower() in x)]
    total_peliculas = df_actor_films.shape[0]
    total_retorno = (df_actor_films['revenue'] - df_actor_films['budget']).sum()
    
    if total_peliculas > 0:
        promedio_retorno = total_retorno / total_peliculas
        return {
            "message": f"El actor {nombre_actor} ha participado de {total_peliculas} cantidad de filmaciones, el mismo ha conseguido un retorno de {total_retorno} con un promedio de {promedio_retorno} por filmación"
        }
    else:
        return {"message": "Actor no encontrado o no tiene suficientes participaciones"}

@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str):
    df_director = df_combines[df_combines['director'].str.lower() == nombre_director.lower()]
    total_peliculas = df_director.shape[0]
    total_retorno = (df_director['revenue'] - df_director['budget']).sum()
    
    if total_peliculas > 0:
        promedio_retorno = total_retorno / total_peliculas
        peliculas_info = df_director[['title', 'release_date', 'revenue', 'budget']].copy()
        peliculas_info['retorno_individual'] = peliculas_info['revenue'] - peliculas_info['budget']
        peliculas_info.rename(columns={'title': 'titulo', 'release_date': 'fecha_lanzamiento', 'revenue': 'ganancia', 'budget': 'costo'}, inplace=True)
        
        return {
            "message": f"El director {nombre_director} ha participado de {total_peliculas} cantidad de filmaciones, el mismo ha conseguido un retorno de {total_retorno} con un promedio de {promedio_retorno} por filmación",
            "peliculas": peliculas_info.to_dict(orient='records')
        }
    else:
        return {"message": "Director no encontrado o no tiene suficientes participaciones"}

@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df_sample['title'])

    # Calcular la similitud de coseno entre todas las películas
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    # Obtener el índice de la película que coincide con el título
    idx = df_sample[df_sample['title'].str.contains(titulo, case=False, na=False)].index[0]
    
    # Obtener los índices de las películas con la mayor similitud
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Obtener las 5 más similares
    
    # Obtener los títulos de las películas más similares
    movie_indices = [i[0] for i in sim_scores]
    similar_movies = df_sample['title'].iloc[movie_indices]
    
    return {"recommendations": similar_movies.tolist()}
