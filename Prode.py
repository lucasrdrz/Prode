import pandas as pd
import streamlit as st

st.title("🏆 Prode Mundial")

# URLs
url_partidos = "https://docs.google.com/spreadsheets/d/1q_1I2ShBwUFwqJ1RJ0SVjr-VnYbeQS8TiqB0hrSB5TM/gviz/tq?tqx=out:csv&gid=0"

url_predicciones = "https://docs.google.com/spreadsheets/d/1q_1I2ShBwUFwqJ1RJ0SVjr-VnYbeQS8TiqB0hrSB5TM/gviz/tq?tqx=out:csv&gid=299285810"

# Cargar datos
partidos = pd.read_csv(url_partidos)
predicciones = pd.read_csv(url_predicciones)

# Mostrar tablas originales
st.subheader("📅 Partidos")
st.dataframe(partidos)



# Filtrar solo partidos con resultado cargado
partidos_jugados = partidos.dropna(subset=["Resultado"])

# Merge
df = predicciones.merge(
    partidos_jugados,
    left_on="Partido_ID",
    right_on="ID"
)

# Calcular puntos
df["Puntos"] = (
    df["Prediccion"]
    .astype(str)
    .str.strip()
    .str.upper()
    ==
    df["Resultado"]
    .astype(str)
    .str.strip()
    .str.upper()
).astype(int)

# Ranking
tabla = (
    df.groupby("Usuario")["Puntos"]
    .sum()
    .reset_index()
    .sort_values(by="Puntos", ascending=False)
)

st.subheader("🏆 Tabla de posiciones")
st.dataframe(tabla)
