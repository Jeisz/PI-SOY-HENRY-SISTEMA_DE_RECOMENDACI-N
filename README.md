<div align="center">
    <a href="https://github.com/user-attachments/assets/5d6e9107-fb3d-44a1-878e-30c37d6699d5">
        <img src="https://github.com/user-attachments/assets/5d6e9107-fb3d-44a1-878e-30c37d6699d5" alt="Proyecto de Recomendación de Películas" width="600">
    </a>
</div>


# Sistema de Recomendación de Películas con FastAPI
Descripción del Proyecto
Contexto
Trabajas como Data Scientist en una start-up de servicios de agregación de plataformas de streaming. El objetivo es desarrollar un sistema de recomendación de películas desde cero, que incluye la limpieza de datos y el despliegue de una API para recomendaciones de películas. Si alguna vez han interactuado con la plataforma Netflix , este proyecto nos mostrara como podemos relaciónar diferentes titulos con coincidencias similares. 

<div align="center">
    <a href="https://github.com/user-attachments/assets/68c4ff66-d869-4bdc-9c73-0b984949a897">
        <img src="https://github.com/user-attachments/assets/68c4ff66-d869-4bdc-9c73-0b984949a897" alt="Pelis" width="1000" height="500">
    </a>
</div>


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
Este apartado lo encontraremos en los archivos de ETL del presente repositorio en los cuales se explica de manera detallada el proceso de extracción y limpieza hecho posteriormente a la evaluación de las variables mediante un EDA inicial. 
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
# Analisis EDA
<div align="center">
    <a href="https://github.com/user-attachments/assets/d34a35cc-4c77-4180-9d45-b346a92c814b">
        <img src="https://github.com/user-attachments/assets/d34a35cc-4c77-4180-9d45-b346a92c814b" alt="Gráfica pi" width="800">
    </a>
</div>
La gráfica muestra la cantidad de filmaciones (películas) estrenadas por mes, basada en los datos procesados y transformados del conjunto de datos que utilizamos en el proyecto. Cada barra representa un mes del año, con la altura de la barra indicando el número total de películas estrenadas durante ese mes.

Enero tiene el mayor número de filmaciones, con aproximadamente 6000 películas estrenadas.
Febrero muestra una disminución significativa con cerca de 3000 filmaciones.
Los meses de Marzo a Junio tienen una cantidad similar de filmaciones, alrededor de 3000 a 4000.
Julio muestra una ligera caída en comparación con los meses anteriores.
Agosto y Septiembre tienen un repunte, especialmente Septiembre, con un número elevado de estrenos.
Octubre tiene un número considerable de estrenos, aunque ligeramente menor que septiembre.
Noviembre y Diciembre muestran un descenso en la cantidad de filmaciones, siendo noviembre el mes con menos estrenos del trimestre final.
Esta distribución puede indicar patrones estacionales en la industria cinematográfica, con picos en ciertos meses debido a festividades, vacaciones o estrategias de lanzamiento de las películas.
En base a este tipo de analisis se procede a desarrollar la función con FastApi 
Despliegue
La API se desplegó en Render para que pueda ser consumida desde la web.

Un sistema de recomendación de películas es una herramienta que sugiere películas a los usuarios basándose en sus preferencias y comportamientos previos. Estos sistemas son esenciales en plataformas de streaming para mejorar la experiencia del usuario, incrementando la satisfacción y el engagement. Los principales beneficios de un sistema de recomendación de películas incluyen:

Personalización: Ofrece recomendaciones personalizadas a cada usuario, lo que aumenta la relevancia del contenido sugerido.
Descubrimiento de Contenido: Ayuda a los usuarios a descubrir nuevas películas que de otra manera no encontrarían.
Retención de Usuarios: Mantiene a los usuarios interesados y comprometidos, lo que puede reducir la tasa de abandono.
Incremento de Visualizaciones: Al sugerir contenido que es probable que le guste al usuario, se incrementa el tiempo de visualización y el uso de la plataforma.
Análisis de Preferencias: Proporciona información valiosa sobre las preferencias y tendencias de los usuarios, lo que puede ser útil para la estrategia de contenido y marketing, por ejemplo si yo voy a ver Toy Story la popular pelicula de Disney Pixar puedo nuevas producciones en base a nuestro sistema de recomentación. 

<div align="center">
    <a href="https://github.com/user-attachments/assets/2a763cef-1378-4e91-a9ea-03aa29bd4798">
        <img src="https://github.com/user-attachments/assets/2a763cef-1378-4e91-a9ea-03aa29bd4798" alt="Toy Story" width="800">
    </a>
</div>

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
Este proyecto está bajo la Licencia y nombre de Jeison Stiven Zapata Pinzón.
<div align="center">
    <a href="https://github.com/user-attachments/assets/404fc7e4-33a0-4ace-946c-d428b54eb519">
        <img src="https://github.com/user-attachments/assets/404fc7e4-33a0-4ace-946c-d428b54eb519" alt="Green and Pink Aesthetic Page Border Doubled Sided Poster" width="800">
    </a>
</div>

