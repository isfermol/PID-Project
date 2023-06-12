import streamlit as st
import pandas as pd
import folium
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import geopandas as gpd
from unidecode import unidecode
import pydeck as pdk
import numpy as np
import seaborn as sns
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt


st.set_page_config(page_title= "Puntos turísticos", page_icon = ":hotel:", layout = 'wide', initial_sidebar_state = 'auto')
st.title("Mapa de histórico de puntos turísticos")
@st.cache_data
def get_keys_with_value(dic, value):
    
    return [key for key in dic if dic[key][3:] == value][0]

# Muestro los controles
def display_year_month(df):
    year_list = list(df['año'].unique())
    year_list.sort(reverse = True )
    year = st.sidebar.selectbox('año', year_list, 0)
    df_anyo= df[df['año']==year]
    month_list = list(df_anyo['mes'].unique())
    mes = st.sidebar.selectbox('mes', month_list, 0)

    return year, mes

def display_ciudad(df):
    city_name = st.sidebar.selectbox('Punto Turístico', ciudad_list)
    return city_name

def display_origen_filter():
    return st.sidebar.radio('origen', ['Residentes en España', 'Residentes en el Extranjero'])


#cargo los datos relacionados con los puntos turísticos
ciudades = pd.read_excel("listado-longitud-latitud-municipios-espana.xls", header=2)
df4 = pd.read_csv(r'2078.csv',sep=';',encoding="utf-8",on_bad_lines='skip')
print(ciudades)
print('dd--', df4)

df4 = df4.rename(columns={"Puntos turísticos": 'Población'})
df4['Población'] = df4['Población'].str[6:]
print('dd33--', df4)
# df_ciu= ciudades['Población', 'Latitud', 'Longitud']
df_ciudades = pd.merge(df4, ciudades[['Población', 'Latitud', 'Longitud']], on='Población')
df_ciudades['año'] = df_ciudades['Periodo'].str[:4]
df_ciudades['mes'] = df_ciudades['Periodo'].str[5:]
df_ciudades =df_ciudades[df_ciudades['Viajeros y pernoctaciones']== "Pernoctaciones"]
df_ciudades_data = df_ciudades.pivot(index=['Periodo','Población', 'Latitud', 'Longitud', 'año', 'mes'], columns='Residencia', values='Total').reset_index()
df_ciudades_data['Residentes en España']=df_ciudades_data['Residentes en España'].str.replace(',', '').str.replace('.', '')
df_ciudades_data['Residentes en España']=pd.to_numeric(df_ciudades_data['Residentes en España'], errors='coerce')
df_ciudades_data['Residentes en el Extranjero']=df_ciudades_data['Residentes en el Extranjero'].str.replace(',', '').str.replace('.', '')
df_ciudades_data['Residentes en el Extranjero']=pd.to_numeric(df_ciudades_data['Residentes en el Extranjero'], errors='coerce')
df_ciudades_data = df_ciudades_data.dropna(subset=['Residentes en el Extranjero'])
df_ciudades_data = df_ciudades_data.dropna(subset=['Residentes en España'])
print(df_ciudades_data)

ciudad_list = list(df_ciudades_data['Población'].unique())

year, month = display_year_month(df_ciudades_data)   
ciudad = display_ciudad(df_ciudades_data)
origen = display_origen_filter()
#imprimo el mapa de puntos de interés
elevation_scale = st.slider("Escala de elevación", 0, 20, 65)
layer = pdk.Layer(
    "HexagonLayer",
    df_ciudades_data,
    get_position=['Longitud', 'Latitud'],
    get_elevation='log_' + origen,
    auto_highlight=True,
    elevation_scale=elevation_scale,
    pickable=True,
    elevation_range=[0, 3000],
    extruded=True,
    coverage=1,
  
)

view_state = pdk.ViewState(
    longitude=df_ciudades_data['Longitud'].mean(), latitude=df_ciudades_data['Latitud'].mean(), zoom=5, min_zoom=2, max_zoom=15, pitch=40.5, bearing=0,
)

r = pdk.Deck(layers=[layer], initial_view_state=view_state)

st.pydeck_chart(r)
df_ciu = df_ciudades_data[(df_ciudades_data['año'] == year) & (df_ciudades_data['mes'] == month)&(df_ciudades_data['Población'] == ciudad)]

#controlo que si para algun valor concreto nohay datos no salte un error en la interfaz
if df_ciu.empty:
        valor = 0
else:
    valor = df_ciu[origen] 
    

st.subheader(f'Visitantes {ciudad} en {year}/{month}:')   
st.metric(f'{origen}:', valor)
