import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

st.title("🏆 Prode Mundial")

# URLs
url_partidos = "https://docs.google.com/spreadsheets/d/1q_1I2ShBwUFwqJ1RJ0SVjr-VnYbeQS8TiqB0hrSB5TM/gviz/tq?tqx=out:csv&gid=0"
url_predicciones = "https://docs.google.com/spreadsheets/d/1q_1I2ShBwUFwqJ1RJ0SVjr-VnYbeQS8TiqB0hrSB5TM/gviz/tq?tqx=out:csv&gid=299285810"

# Cargar datos
partidos = pd.read_csv(url_partidos)
predicciones = pd.read_csv(url_predicciones)

# Limpiar nombres de columnas
partidos.columns = partidos.columns.str.strip()
predicciones.columns = predicciones.columns.str.strip()

# Limpiar valores de texto
for col in partidos.columns:
    partidos[col] = partidos[col].astype(str).str.strip()

for col in predicciones.columns:
    predicciones[col] = predicciones[col].astype(str).str.strip()

# Mostrar datos originales
st.subheader("📋 Partidos")
st.dataframe(partidos)

st.subheader("📝 Predicciones")
st.dataframe(predicciones)

# Filtrar partidos con resultado cargado
partidos_jugados = partidos[
    partidos["Resultado"].notna()
]

partidos_jugados = partidos_jugados[
    partidos_jugados["Resultado"].str.strip() != ""
]

st.write("Partidos con resultado:", len(partidos_jugados))

# Merge
df = predicciones.merge(
    partidos_jugados,
    left_on="Partido_ID",
    right_on="ID",
    how="inner"
)

# Calcular puntos
df["Puntos"] = (
    df["Prediccion"].str.upper().str.strip()
    ==
    df["Resultado"].str.upper().str.strip()
).astype(int)

# Debug completo
st.subheader("🔍 Verificación de puntos")

columnas_debug = [
    "Usuario",
    "Partido_ID",
    "Prediccion",
    "Resultado",
    "Puntos"
]

st.dataframe(
    df[columnas_debug].sort_values(
        ["Usuario", "Partido_ID"]
    ),
    use_container_width=True
)

# Ranking
tabla = (
    df.groupby("Usuario", as_index=False)["Puntos"]
    .sum()
    .sort_values("Puntos", ascending=False)
)

st.subheader("🏆 Tabla de posiciones")
st.dataframe(tabla, use_container_width=True)

# Opcional: selector para revisar un usuario
usuarios = sorted(df["Usuario"].unique())

usuario = st.selectbox(
    "Ver detalle de usuario",
    usuarios
)

st.subheader(f"Detalle de {usuario}")

detalle = df[df["Usuario"] == usuario][
    [
        "Partido_ID",
        "Local",
        "Visitante",
        "Resultado",
        "Prediccion",
        "Puntos"
    ]
]

st.dataframe(detalle, use_container_width=True)

st.write(
    "Total puntos:",
    detalle["Puntos"].sum()
)
