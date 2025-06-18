import streamlit as st
import pandas as pd
from joblib import load
import os
from surprise import Dataset

# Configuración inicial
st.set_page_config(page_title="Sistema de Recomendación", layout="wide")

# Cargar datos y modelo
@st.cache_resource
def load_data():
    """Carga el dataset y el modelo con caché para mejor performance"""
    # Descargar dataset si no existe (solo en Colab)
    if not os.path.exists('data/ml-100k/u.data'):
        Dataset.load_builtin('ml-100k')
    
    # Cargar datos de películas
    movies = pd.read_csv(
        'data/ml-100k/u.item', 
        sep='|', 
        encoding='latin-1',
        header=None,
        names=['movie_id', 'title', 'release_date', 'video_release', 'imdb_url', 
               'unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy',
               'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
               'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    )
    
    # Cargar modelo pre-entrenado
    model = load('models/modelo_surprise.joblib')
    return movies, model

movies, model = load_data()

# Interfaz de usuario
st.title("🎬 Sistema de Recomendación de Películas")

# Selector de usuario
user_ids = list(range(1, 944))  # IDs de usuarios en MovieLens 100k
selected_user = st.selectbox("Selecciona un usuario:", user_ids)

# Selector de rigor de recomendación
rigor = st.radio("Nivel de rigor:", 
                 ["≥ 3.5 (Recomendaciones amplias)", 
                  "≥ 4.0 (Recomendaciones buenas)",
                  "≥ 4.5 (Recomendaciones excelentes)",
                  "Aleatorias (≥ 3.0)"])

# Botón de generación
if st.button("Generar Recomendaciones"):
    with st.spinner("Calculando recomendaciones..."):
        # Generar predicciones para todas las películas
        predictions = []
        for movie_id in movies['movie_id']:
            pred = model.predict(str(selected_user), str(movie_id))
            predictions.append((movie_id, pred.est))
        
        # Convertir a DataFrame
        recs = pd.DataFrame(predictions, columns=['movie_id', 'rating'])
        
        # Filtrar según rigor seleccionado
        if "Aleatorias" in rigor:
            recs = recs[recs['rating'] >= 3.0].sample(10)
        else:
            min_rating = float(rigor.split("≥ ")[1].split(" ")[0])
            recs = recs[recs['rating'] >= min_rating].nlargest(10, 'rating')
        
        # Unir con información de películas
        recs = pd.merge(recs, movies[['movie_id', 'title']], on='movie_id')
        
        # Mostrar resultados
        st.subheader(f"Top 10 Recomendaciones para Usuario {selected_user}")
        st.dataframe(
            recs[['title', 'rating']].rename(columns={'title': 'Película', 'rating': 'Rating Predicho'}),
            column_config={
                "Rating Predicho": st.column_config.NumberColumn(format="%.2f")
            },
            hide_index=True,
            use_container_width=True
        )

        # Gráfico adicional
        st.bar_chart(recs.set_index('title')['rating'])