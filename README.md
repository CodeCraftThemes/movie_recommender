# 🎥 Sistema de Recomendación de Películas

## 📌 Descripción
Aplicación web que recomienda películas usando filtrado colaborativo basado en el dataset MovieLens 100k.

## 🛠️ Funcionalidades
- Selector de usuario con 943 opciones
- 4 niveles de rigor para recomendaciones
- Tabla interactiva con top 10 recomendaciones
- Visualización gráfica de ratings

## 🚀 Cómo Usarlo
1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Descargar dataset:
```bash
mkdir -p data/ml-100k
wget https://files.grouplens.org/datasets/movielens/ml-100k.zip -O data/ml-100k.zip
unzip data/ml-100k.zip -d data/
```

3. Ejecutar la app:
```bash
streamlit run app.py
```

## 🔍 Estructura del Código
- `load_data()`: Carga el dataset y modelo con caché
- Interfaz Streamlit: Selectores + botón de acción
- Lógica de filtrado: 4 modos diferentes de recomendación
- Visualización: Tabla + gráfico de barras

## 📊 Lógica de Recomendación
1. Para el usuario seleccionado, predice el rating de todas las películas
2. Filtra según el nivel de rigor elegido:
   - ≥ 3.5: 35% mejores ratings
   - ≥ 4.0: 20% mejores ratings
   - ≥ 4.5: 10% mejores ratings
   - Aleatorias: Muestra 10 películas al azar con rating ≥ 3.0