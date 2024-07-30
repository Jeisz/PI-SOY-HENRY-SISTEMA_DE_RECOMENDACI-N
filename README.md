<a href="https://github.com/user-attachments/assets/5d6e9107-fb3d-44a1-878e-30c37d6699d5">
    <img src="https://github.com/user-attachments/assets/5d6e9107-fb3d-44a1-878e-30c37d6699d5" alt="Proyecto de Recomendación de Películas" width="600">
</a>

# Sistema de Recomendación de Películas con FastAPI
Descripción del Proyecto
Contexto
Trabajas como Data Scientist en una start-up de servicios de agregación de plataformas de streaming. El objetivo es desarrollar un sistema de recomendación de películas desde cero, que incluye la limpieza de datos y el despliegue de una API para recomendaciones de películas.

Objetivo
El objetivo principal es crear un flujo de trabajo eficiente que incluya la recopilación y transformación de datos, análisis exploratorio, desarrollo de modelos y su implementación utilizando prácticas de MLOps.

Conjunto de Datos
El proyecto parte de un conjunto de datos de películas que incluye detalles como títulos, fechas de estreno, ingresos, presupuestos, entre otros. Este dataset fue limpiado y transformado para facilitar el análisis y la creación del modelo de recomendación.

Transformaciones de Datos
Para preparar los datos y crear un MVP (Producto Mínimo Viable), se realizaron las siguientes transformaciones:

Desanidar Campos: Campos como belongs_to_collection y production_companies fueron desanidados para facilitar el acceso y manipulación de datos.
Relleno de Valores Nulos: Los valores nulos en los campos revenue y budget se reemplazaron con 0.
Eliminación de Valores Nulos en Fechas: Se eliminaron los registros con valores nulos en release_date.
Formato de Fechas: release_date se convirtió al formato AAAA-mm-dd y se creó la columna release_year.
Cálculo de Retorno de Inversión: Se añadió la columna return calculando revenue / budget, reemplazando valores nulos con 0.
Eliminación de Columnas No Utilizadas: Se eliminaron columnas innecesarias como video, imdb_id, adult, original_title, poster_path, y homepage.
Desarrollo de la API
Se desarrolló una API usando FastAPI con los siguientes endpoints:

cantidad_filmaciones_mes(mes: str): Devuelve la cantidad de películas estrenadas en un mes específico.
cantidad_filmaciones_dia(dia: str): Devuelve la cantidad de películas estrenadas en un día específico.
score_titulo(titulo_de_la_filmacion: str): Devuelve el título, año de estreno y score de una película.
votos_titulo(titulo_de_la_filmacion: str): Devuelve el título, cantidad de votos y promedio de votaciones de una película.
get_actor(nombre_actor: str): Devuelve el éxito de un actor medido a través del retorno de inversión y cantidad de películas.
get_director(nombre_director: str): Devuelve el éxito de un director medido a través del retorno de inversión y detalles de cada película dirigida.
recomendacion(titulo: str): Devuelve una lista de 5 películas similares a la ingresada utilizando TfidfVectorizer y cosine_similarity.
Sistema de Recomendación
El sistema de recomendación se basa en la similitud de títulos utilizando TfidfVectorizer y cosine_similarity. Este enfoque permite calcular la similitud entre los títulos de las películas y recomendar las más similares.

Despliegue
La API se desplegó en Render para que pueda ser consumida desde la web.

Instalación
Para instalar y ejecutar el proyecto localmente:

Clona el repositorio desde GitHub.
Navega al directorio del proyecto.
Instala las dependencias listadas en requirements.txt.
Corre el servidor de FastAPI utilizando Uvicorn.
Estructura del Repositorio
/datasets: Archivos necesarios donde consultará nuestro código principal.
/notebooks: Notebooks de Jupyter utilizados para la exploración y desarrollo.
main.py: Código principal del proyecto para la API.
README.md: Guía rápida para comprender el proyecto y contribuir eficientemente.
requirements.txt: Librerías necesarias para que el modelo funcione en render.
Contribución
Para contribuir al proyecto, abre un issue primero para discutir los cambios que deseas realizar. Las contribuciones son bienvenidas.

Licencia
Este proyecto está bajo la Licencia MIT.

