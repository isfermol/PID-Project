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
import matplotlib.ticker as ticker
import random
import matplotlib.pyplot as plt
import networkx as nx
import myMain

#título e icono de la página
st.set_page_config(page_title= "Graficas", page_icon = ":hotel:", layout = 'wide', initial_sidebar_state = 'auto')

#cargo los controles

def display_origen_filter():
    return st.sidebar.radio('Caegoría de gráficos', ['Origen_turismo', 'Personal_empleado'])

def display_year(df):
    year_list = list(df['año'].unique())
    year_list.sort(reverse = True )
    year = st.sidebar.selectbox('año', year_list, 0)
    return year

def display_year_mes(df):
    year_list = list(df['año'].unique())
    year_list.sort(reverse = True )
    year = st.sidebar.selectbox('año', year_list, 0)
    df_anyo= df[df['año']==year]
    month_list = list(df_anyo['mes'].unique())
    mes = st.sidebar.selectbox('mes', month_list, 0)

    return year, mes


# método para mostrar los datos de ocupación turística nacional e internacional en las top 15 provincias como si fuera una pirámide poblacional con graficos de barras
def display_pyramid_top15(df, year):
    df = df[(df['año'] == year)]

    top15_provincias = df.groupby('Provincias')['Ambos_origenes'].mean().nlargest(15).index
    df_top15 = df[df['Provincias'].isin(top15_provincias)]

    df_top15 = df_top15.sort_values(by='Ambos_origenes', ascending=False)   
    colores = ['deepskyblue', 'limegreen']

  
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

  
    sns.barplot(data=df_top15, x=-df_top15['Nacional'], y=df_top15['Provincias'].str[3:], ax=ax1, color=colores[0])
    ax1.set_xlim(-df_top15['Nacional'].max(), 0)  
    ax1.set_xlabel('Origen Nacional', fontsize=12)
    ax1.set_ylabel('') 
    ax1.set_yticklabels([])  

    ax1.set_xticklabels(ax1.get_xticks() * -1)
    ax1.xaxis.set_tick_params(width=0.5)
    ax1.spines['left'].set_color('none')
    ax1.spines['right'].set_color('gray')
    ax1.spines['bottom'].set_color('gray')
    ax1.spines['top'].set_color('none')
    ax1.yaxis.tick_right()
    ax1.xaxis.tick_bottom()
    ax1.yaxis.set_tick_params(width=0.5)

    sns.barplot(data=df_top15, x='Internacional', y=df_top15['Provincias'].str[3:], ax=ax2, color=colores[1])
    ax2.set_xlim(0, df_top15['Internacional'].max())  
    ax2.set_xlabel(f'Origen Internacional', fontsize=12)
    ax2.set_ylabel('')  

    ax2.spines['left'].set_color('none')
    ax2.spines['right'].set_position('zero')
    ax2.spines['right'].set_linewidth(0.5)
    ax2.spines['left'].set_color('none')
    ax2.yaxis.set_label_coords(-0.1, 0.5)
    ax1.xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    ax1.tick_params(axis='x', labelrotation=45, labelsize=10)
    ax2.xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    ax2.tick_params(axis='x', labelrotation=45, labelsize=10)
    plt.subplots_adjust(wspace=0.5)
    plt.suptitle(f'Top 15 provincias con mayor ocupación ({year})', fontsize=15, ha='center')
    st.pyplot(fig)

#gráfico comparativo evolución turismo nacional e internaicional
def display_evolucion_turismo(df, codProv):
    df = df[df['codProv'] == codProv] 
    print(df)

    df_n = df.groupby('año')['Nacional'].mean().reset_index()
    df_i = df.groupby('año')['Internacional'].mean().reset_index()
    df_s = df.groupby('año')['Ambos_origenes'].mean().reset_index()
    sns.set(style='darkgrid')

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_n, x='año', y='Nacional',  palette='Set1',color='deepskyblue', label='Nacional')
    sns.lineplot(data=df_i, x='año', y='Internacional',  palette='Set2',color = 'limegreen', label='Internacional')
    sns.lineplot(data=df_s, x='año', y='Ambos_origenes', palette='Set3',color = 'gold', label='Suma')

    plt.title(f'Evolución del turismo en {prov_dict[codProv][3:]}', fontsize=14)
    plt.xlabel('Año', fontsize=12)
    plt.xticks(rotation=45)
    plt.ylabel('Ocupación', fontsize=12)
    plt.legend(title='Tipo', fontsize=10, title_fontsize=12)

    st.pyplot(plt.gcf())
#gráfico comparativo de evolución del empleo en hostelería y num de turistas
def display_evolucion_empleo(df, df_empl, codProv, provin):
    df = df[df['codProv'] == codProv] 
    df_empl = df_empl[df_empl['codProv'] == codProv] 
    print(df)

    df_e = df_empl.groupby('año')['Personal empleado'].mean().reset_index()
    df_o = df.groupby('año')['Ambos_origenes'].mean().reset_index()
    sns.set(style='darkgrid')
    plt.figure(figsize=(12, 6))
    ax1 = sns.lineplot(data=df_o, x='año', y='Ambos_origenes',color='gold')
    # ax1.set_xticklabels(rotation=45)
    ax2 = ax1.twinx()
    ax2 = sns.barplot(data=df_e, x='año', y='Personal empleado', color='lightblue', alpha=0.4, ax=ax2)
    ax1.set_ylabel('Turismo', color='gold')
    ax2.set_ylabel('Personal empleado', color='lightblue')
    # ax2.set_xticklabels(rotation=45)
    plt.title(f'Evolución temporal de Turismo y Personal empleado en hostelería en {provin}')
    plt.xlabel('Año')
    for item in ax2.get_xticklabels():
        item.set_rotation(45)
    for item in ax1.get_xticklabels():
        item.set_rotation(45)
    st.pyplot(plt.gcf())

# top 10 provincias y top5 Comunidades con más empleados en hostelería(2 graficas de donut en una)
def grafica_donut(df, year, month):
    df_year = df[(df['año'] == year) & (df['mes'] == month)]
    print('yeye',df_year)
    top_provincias = df_year.nlargest(10, 'Personal empleado')
    print(top_provincias)
    top_comunidades = df_year.groupby('Comunidades y Ciudades Autónomas')['Personal empleado'].sum().nlargest(5).index.tolist()
    colores_provincias = sns.color_palette('pastel', len(top_provincias))
    colores_comunidades = sns.color_palette('Set2', len(top_comunidades))
    mapa_colores_provincias = dict(zip(top_provincias['Provincias'], colores_provincias))
    mapa_colores_comunidades = dict(zip(top_comunidades, colores_comunidades))
    data_provincias = top_provincias['Personal empleado']
    for data in data_provincias:
        if data == 0.0:
            data = 1.0

    data_comunidades = df_year[df_year['Comunidades y Ciudades Autónomas'].isin(top_comunidades)].groupby('Comunidades y Ciudades Autónomas')['Personal empleado'].sum()
    try:
            
        fig, ax = plt.subplots(figsize=(10, 8))
        wedges, text, autotexts = ax.pie(data_provincias, colors=[mapa_colores_provincias[prov] for prov in top_provincias['Provincias']],radius=1.2, wedgeprops=dict(width=0.3), startangle=-40, autopct='%1.1f%%')
        ax.set_title(f'Provincias y CCAA con más empleo en hosteleria en {year}\{month}')
        ax2 = plt.gcf().add_axes([0.41, 0.4, 0.2, 0.2])
        wedges2, text2,autotexts2 = ax2.pie(data_comunidades, colors=[mapa_colores_comunidades[com] for com in data_comunidades.index], radius=2.2,wedgeprops=dict(width=0.3), startangle=-40, autopct='%1.1f%%')
        nameProv = [ptov[3:] for ptov in top_provincias['Provincias']]
        namecom = [com[3:] for com in data_comunidades.index]
        ax.legend(wedges, nameProv, loc="upper right", title='Provincias', bbox_to_anchor=(1.4, 1))
        ax2.legend(wedges2,namecom, loc="center right", title='Comunidades Autónomas', bbox_to_anchor=(3.9,0.3))
        for autotext in autotexts2:
            autotext.set_horizontalalignment('center')
            autotext.set_verticalalignment('center')
        print('auto--------  ',autotexts)
    
        st.pyplot(fig)
    except:
        st.write(f"No hay datos para Provincias y CCAA con más empleo en hosteleria en {year}\{month}")


#cargo y formateo los datos
provincias = myMain.provincias

df3 = pd.read_csv(r'2074.csv',sep=';',encoding="utf-8",on_bad_lines='skip')
df_nacional_inter = myMain.df_nacional_inter
prov_list = myMain.prov_list
prov_dict = myMain.prov_dict
quitar_acentos = myMain.quitar_acentos

#dataframeEmpleo
df2 = pd.read_csv(r'2066.csv',sep=';',encoding="utf-8",on_bad_lines='skip')

df_OcupHabitProv = df2.pivot(index=['Periodo','Comunidades y Ciudades Autónomas', 'Provincias'], columns='Establecimientos y personal empleado (plazas)', values='Total').reset_index()

df_empleo = df_OcupHabitProv[['Periodo', 'Personal empleado','Comunidades y Ciudades Autónomas', 'Provincias']]
df_empleo['año'] = df_empleo['Periodo'].str[:4]
df_empleo['mes'] = df_empleo['Periodo'].str[5:]
# df_nacional_inter_empleo = pd.merge(df_nacional_inter, df_toMerge, on='Periodo', how='left')

df_empleo['Personal empleado']=df_empleo['Personal empleado'].str.replace(',', '').str.replace('.', '')
df_empleo['Personal empleado'] = pd.to_numeric(df_empleo['Personal empleado'], errors='coerce')
df_empleo = df_empleo.dropna(subset=['Personal empleado','Comunidades y Ciudades Autónomas', 'Provincias'])
df_empleo['codProv'] = df_empleo['Provincias'].str.upper()
df_empleo['codProv'] = df_empleo['codProv'].str.strip()
df_empleo['codProv'] = df_empleo['codProv'].str[3:7].apply(quitar_acentos)

print(df_empleo)
#depende del tipo de geáfico seleccionado muestro unas gráficas u otras
tipo = display_origen_filter()
provincia = myMain.display_provincia(df_nacional_inter, '')
codProvin = myMain.get_keys_with_value(prov_dict, provincia)
if tipo == "Origen_turismo":
    st.header('Gráficas Ocupación')
    year = display_year(df_nacional_inter)
    st.subheader(f'Provincias con mayor ocupación turística')   
    display_pyramid_top15(df_nacional_inter, year)
    st.subheader(f'Evolución de la ocupación turística')   
    display_evolucion_turismo(df_nacional_inter, codProvin)
else:
     st.header('Gráficas Empleo')
     year, month = display_year_mes(df_empleo)
     st.subheader(f'Comparativa evolución ocupación turística y personal empleado en hostelería')   
     try:
        display_evolucion_empleo(df_nacional_inter,df_empleo, codProvin, provincia)
     except:
        st.write(f"No hay datos suficientes relativos a {provincia}")
     st.subheader(f'provincias y comunidades con mayor empleo en el sector de hostelería')   
     grafica_donut(df_empleo, year, month)