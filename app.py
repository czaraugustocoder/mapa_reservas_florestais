import folium
import geopandas as gpd
import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import json
import os

st.set_page_config(page_title="MAPA",
                   layout="wide"
)

current_working_directory = os.getcwd()

path_logo = os.path.join(current_working_directory, "cest_logo.jpeg")

locations_path = os.path.join(current_working_directory, "UC_Estadual.shp.xlsx")

geo_path = os.path.join(current_working_directory, "UC_Estadual.geojson")

glebas_path = os.path.join(current_working_directory, "GLEBAS_AMAZONAS.geojson")

st.title("RESERVAS FLORESTAIS DO AMAZONAS")

st.sidebar.image(path_logo)

locations = pd.read_excel(locations_path)

fig = folium.Map(location=[-4.699395, -62.155688], zoom_start=6.25)

geo_json_map = json.load(open(glebas_path))
folium.Choropleth(
    geo_data = geo_json_map,
    fill_color = "purple",
    fill_opacity = 0.4,
    line_color = "purple",
    line_opacity = 0.9
).add_to(fig)

geo_json_map = json.load(open(geo_path))
folium.Choropleth(
    geo_data = geo_json_map,
    fill_color = "green",
    fill_opacity = 0.4,
    line_color = "green",
    line_opacity = 0.9
).add_to(fig)

# add marker one by one of state schools on the map
for i in range(0,len(locations)):
   folium.Marker(
      location=[locations.iloc[i]['y'], locations.iloc[i]['x']],
      icon=folium.Icon(color="blue", icon="info-sign"),
      popup=locations.iloc[i]['nome']
   ).add_to(fig)

dados_reserva = locations[['nome', 'categoria', 'uso']]

# Adicionar um controle de camadas
folium.LayerControl().add_to(fig)

col1, col2 = st.columns([2, 1.25])
with col1:
    st.write("MAPA DAS RESERVAS FLORESTAIS")
    st_data = st_folium(fig, width=1000, height=700)

with col2:
    st.write("TABELA DE RESERVAS FLORESTAIS")
    st.dataframe(dados_reserva, width=700, height=700)
