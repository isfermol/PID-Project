import streamlit as st
import pandas as pd
import folium
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import geopandas as gpd
from unidecode import unidecode
import datetime
import numpy as np
import seaborn as sns
import config
import sqlite3
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from sqlalchemy import create_engine
import sqlalchemy.pool

APP_TITLE = 'Ocupación hotelera en España'
APP_SUB_TITLE = 'Fuente: Ine'

#modeifico esta variable para que al hacer click en el mapa para seleccionar provincia no se inhabilite el desplegable provincia
if 'desplegable' not in st.session_state:
    st.session_state['desplegable'] = None
#muestro los controles
@st.cache_data
def get_keys_with_value(dic, value):
    
    return [key for key in dic if dic[key][3:] == value][0]

def display_filtros(df, origen):
    year_list = list(df['año'].unique())
    year_list.sort(reverse = True )
    year = st.sidebar.selectbox('año', year_list, 0)
    df_anyo= df[df['año']==year]
    month_list = list(df_anyo['mes'].unique())
    mes = st.sidebar.selectbox('mes', month_list, 0)
    st.header(f'{year}/{mes} - {origen}' )
    return year, mes

def display_provincia(df, prov):
    prov_name = st.sidebar.selectbox('Provincia', prov_list)
    return prov_name

def display_origen_filter():
    return st.sidebar.radio('origen', ['Ambos_origenes', 'Nacional', 'Internacional'])

def display_map(df, year, month, origen):

    df = df[(df['año'] == year) & (df['mes'] == month)]
    m = folium.Map(location=[40.42,  -3.7], zoom_start=5)
    print(df)

    df['log_' + origen] = np.log1p(df[origen])

    bins = np.linspace(df['log_' + origen].min(), df['log_' + origen].max(), num=12)
    coropletas = folium.Choropleth(
        geo_data=provincias,
        name="choropleth",
        data=df,
        columns=["codProv", 'log_' + origen],  
        key_on="properties.codProv",
        bins=bins,
        fill_color="Blues",
        fill_opacity=0.7,
        line_opacity=1.0,
        legend_name="Tasa de ocupacion"
    )
    coropletas.add_to(m)

    # st.markdown(m._repr_html_(), unsafe_allow_html=True)

    # valor_min = df[origen].min()
    # valor_max = df[origen].max()

    # # Crear los 10 intervalos para el mapa de coropletas
    # bins = np.linspace(valor_min, valor_max, num=8)
    # coropletas = folium.Choropleth(geo_data=provincias,name="choropleth",data=df,columns=["codProv", origen],key_on="properties.codProv", bins = bins,fill_color="Blues",fill_opacity=0.7,line_opacity=1.0,legend_name="Tasa de ocupacion")
    # coropletas.add_to(m)
    for feature in coropletas.geojson.data['features']:
       code = feature['properties']['codProv']
       #feature['properties']['Provincia'] = prov_dict[code]
    coropletas.geojson.add_child(folium.features.GeoJsonTooltip(['provincia'], labels=False))
    
    folium.LayerControl().add_to(m)
    st_map = st_folium(m, width=700, height=450)
    codigo = '00'
    if st_map['last_active_drawing']:
        codigo = st_map['last_active_drawing']['properties']['codProv']
    return codigo

def display_datos_ocup(df, year, month, origen, prov_code):
    df = df[(df['año'] == year) & (df['mes'] == month) & (df['codProv'] == prov_code)]    

    print(df[origen])
    print(origen)    
    st.subheader(f'Ocupación de tipo {origen} en {prov_name}:')   
    st.metric('valor', df[origen])
    
def display_grafica(df, year, month, origen, codProvin, provincia):
    df = df[(df['año'] == year) & (df['mes'] == month)]    
    print(df[origen])
    df_top = df.nlargest(10, origen)
    provincias_top = df_top['codProv']
    data_top = df_top[origen]

    provincias = list(provincias_top)
    if codProvin not in provincias:
        provincias.append(codProvin)
        data_top = list(data_top)
        data_top.append(df[df['codProv'] == codProvin][origen].values[0])

    chart_data = pd.DataFrame({'Provincias': provincias, 'Datos': data_top})

    sns.set(style="whitegrid")

    fig, ax = plt.subplots()
    colors = sns.color_palette("viridis", len(chart_data))
    sns.barplot(x='Provincias', y='Datos', data=chart_data, ax=ax, palette=colors)

    ax.set_xlabel('Provincias')
    ax.set_ylabel(origen)
    ax.set_title(f'Provincias en {year}/{month} con mayor ocupación "{format(origen)}" comparadas con {provincia}')
    ax.tick_params(axis='x', rotation=45)
    sns.despine()

    st.pyplot(fig)

    
#título e icono de la pagina
st.set_page_config(page_title= APP_TITLE, page_icon = ":hotel:", layout = 'wide', initial_sidebar_state = 'auto')
st.title(APP_TITLE)
st.caption(APP_SUB_TITLE)

#cargo y formateo los datos
df3 = pd.read_csv(r'2074.csv',sep=';',encoding="utf-8",on_bad_lines='skip')


provincias = gpd.read_file('provincias.geojson')

provincias['pName'] = provincias['provincia']
provincias.loc[provincias['pName'] == 'La Rioja', 'pName'] = 'Rioja, La'
provincias.loc[provincias['pName'] == 'A Coruña', 'pName'] = 'Coruña, A '
provincias.loc[provincias['pName'] == 'Las Palmas', 'pName'] = 'Palmas, Las'
provincias.loc[provincias['pName'] == 'Illes Balears', 'pName'] = 'Balears, Illes'
provincias.loc[provincias['pName'] == 'Alacant', 'pName'] = 'Alicante/Alacant'

def quitar_acentos(texto):
    return unidecode(texto)

### turismo español vs extranjero
pernoct= df3[df3['Viajeros y pernoctaciones']=='Pernoctaciones']
df_nacional_inter = pernoct.pivot(index=['Periodo','Comunidades y Ciudades Autónomas', 'Provincias'], columns='Residencia: Nivel 2', values='Total').reset_index()
df_nacional_inter['año'] = df_nacional_inter['Periodo'].str[:4]
df_nacional_inter['mes'] = df_nacional_inter['Periodo'].str[5:]
df_nacional_inter = df_nacional_inter.rename(columns={np.nan: 'Ambos_origenes'})

df_nacional_inter = df_nacional_inter.dropna(subset=['Provincias', 'Comunidades y Ciudades Autónomas'])

eliminar = ['18 Ceuta','19 Melilla', '01 Andalucía', '02 Aragón', '05 Canarias', '07 Castilla y León', '08 Castilla - La Mancha', '09 Cataluña','10 Comunitat Valenciana','11 Extremadura','12 Galicia', '16 País Vasco', ]
# eliminar = ['01 Andalucía', '02 Aragón', '05 Canarias', '07 Castilla y León', '08 Castilla - La Mancha', '09 Cataluña','10 Comunitat Valenciana','11 Extremadura','12 Galicia', '16 País Vasco', ]
df_nacional_inter = df_nacional_inter[~df_nacional_inter.Provincias.isin(eliminar)]

df_nacional_inter['codProv'] = df_nacional_inter['Provincias'].str.upper()
df_nacional_inter['codProv'] = df_nacional_inter['codProv'].str.strip()
df_nacional_inter['codProv'] = df_nacional_inter['codProv'].str[3:7].apply(quitar_acentos)

provincias['codProv'] = provincias['pName'].str.upper()
provincias['codProv'] = provincias['codProv'].str.strip()
provincias['codProv'] = provincias['codProv'].str[:4].apply(quitar_acentos)

df_nacional_inter['Ambos_origenes']=df_nacional_inter['Ambos_origenes'].str.replace(',', '').str.replace('.', '')
df_nacional_inter['Ambos_origenes']=pd.to_numeric(df_nacional_inter['Ambos_origenes'], errors='coerce')
df_nacional_inter['Residentes en España']=df_nacional_inter['Residentes en España'].str.replace(',', '').str.replace('.', '')
df_nacional_inter['Residentes en España']=pd.to_numeric(df_nacional_inter['Residentes en España'], errors='coerce')
df_nacional_inter['Residentes en el Extranjero']=df_nacional_inter['Residentes en el Extranjero'].str.replace(',', '').str.replace('.', '')
df_nacional_inter['Residentes en el Extranjero']=pd.to_numeric(df_nacional_inter['Residentes en el Extranjero'], errors='coerce')
df_nacional_inter = df_nacional_inter.rename(columns={'Residentes en España': 'Nacional'})
df_nacional_inter = df_nacional_inter.rename(columns={'Residentes en el Extranjero': 'Internacional'})

prov_list = list(df_nacional_inter['Provincias'].str[3:].unique())

prov_dict = pd.Series(df_nacional_inter[df_nacional_inter["mes"]=="12"].Provincias.values,index=df_nacional_inter[df_nacional_inter["mes"]=="12"].codProv).to_dict()
origen = display_origen_filter()

year, month = display_filtros(df_nacional_inter, origen)
prov_name = display_provincia(df_nacional_inter, '')
prov_code= display_map(df_nacional_inter, year, month, origen)

#compruebo si ha cambiado el valor del desplegable o si la modificación de la provincia se ha hecho en el mapa
if st.session_state['desplegable'] != prov_name or prov_code == '00':
        # prov_name = prov_dict[]
        prov_code = get_keys_with_value(prov_dict, prov_name)
        st.session_state['desplegable'] = prov_name
else: 
     prov_name = prov_dict[prov_code][3:]


display_datos_ocup(df_nacional_inter, year, month, origen, prov_code)

display_grafica(df_nacional_inter, year, month, origen, prov_code,prov_dict[prov_code][3:])

#consulto base de datos con openIA para contestar preguntas
def answer():
    uri = "file::memory:?cache=shared"
    table_name = 'prov_datadb'

    conn = sqlite3.connect(':memory:')

    df_nacional_inter.to_sql(table_name, conn, if_exists='replace', index=False)

    eng = create_engine(
        url='sqlite:///file:memdb1?mode=memory&cache=shared', 
        poolclass=sqlalchemy.pool.StaticPool, 
        creator=lambda: conn)
    db = SQLDatabase(engine=eng)

    if config.openai_api_key:
      llm = OpenAI(
          openai_api_key=config.openai_api_key,
          temperature=0, 
          max_tokens=300)
      db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

    if config.openai_api_key:
        config.answer_text = db_chain.run(st.session_state.question)
        st.write(config.answer_text)

#Query IA
user_q = st.text_input(
    "Pregunta: ", 
    help="Haz una pregunta relativa al Dataset", key='question', on_change=answer)

st.write(config.answer_text)

