import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsbombpy import sb
from mplsoccer import Pitch

# Configuración de página
st.set_page_config(page_title="Mapa de Pases - World Cup 2022", layout="wide")
st.title(" Visualizador de Pases por Minuto")

# Caché para evitar descargas repetidas de datos
@st.cache_data
def load_match_events(match_id):
    events = sb.events(match_id=match_id)
    passes = events[["minute", "second", "period", "location", "pass_end_location", "player", "pass_recipient", "team", "type"]].copy()
    
    final = passes[passes["type"] == "Pass"].dropna(subset=["location", "pass_end_location"]).copy()
    final.reset_index(drop=True, inplace=True)
    
    final["x0"] = final.location.apply(lambda x: x[0])
    final["y0"] = final.location.apply(lambda x: x[1])
    final["x1"] = final.pass_end_location.apply(lambda x: x[0])
    final["y1"] = final.pass_end_location.apply(lambda x: x[1])
    final.drop(columns=["location", "pass_end_location"], inplace=True)
    
    return final

# Cargar datos del partido (Japón vs partido selecccionado)
match_id = 3857255
df_passes = load_match_events(match_id)

# Control interactivo con Streamlit
max_minuto = int(df_passes["minute"].max())
minuto = st.slider("Selecciona el minuto del partido:", min_value=1, max_value=max_minuto, value=1)

# Función para dibujar la cancha y los pases
def plot_minute(minuto_sel):
    pitch = Pitch(pitch_color='#aabb97', line_color='white', stripe_color='#c2d59d', stripe=True)
    fig, ax = pitch.draw(figsize=(10, 7))
    
    data_filtered = df_passes[df_passes.minute == minuto_sel]
    
    if data_filtered.empty:
        ax.set_title(f"No hay pases en el minuto {minuto_sel}", fontsize=14)
    else:
        sns.scatterplot(
            data=data_filtered, 
            x="x0", 
            y="y0", 
            hue="team", 
            ax=ax, 
            s=100, 
            zorder=3
        )
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=2)
        ax.set_title(f"Pases registrados en el minuto {minuto_sel}", fontsize=14)
        
    return fig

# Renderizar el gráfico en Streamlit
fig = plot_minute(minuto)
st.pyplot(fig)
