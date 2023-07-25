import streamlit as st
import pandas as pd
df_clusters = pd.read_csv('productos_clustering_kmeans_con_etiquetas.csv')

image_path = './img/banner.png'  
st.image(image_path, use_column_width=True)

opciones_busqueda = ['Arroz', 'Aceite', 'Atún', 'Leche', 'Queso', 'Mantequilla']

busqueda_manual = st.text_input('Buscar en la columna "Lista de Productos"', '')

if st.checkbox('Buscar por opción predefinida'):
    opcion_elegida = st.radio('Selecciona un producto:', opciones_busqueda, format_func=lambda x: x, key='opciones')
    mask = df_clusters['Lista de Productos'].str.contains(opcion_elegida, case=False)
    df_filtrado = df_clusters[mask]
    st.subheader(f'Resultados filtrados para "{opcion_elegida}"')
    st.dataframe(df_filtrado)
if busqueda_manual:
    palabras = busqueda_manual.strip().split()
    mask_manual = df_clusters['Lista de Productos'].apply(lambda x: all(palabra.lower() in x.lower() for palabra in palabras))
    df_filtrado_manual = df_clusters[mask_manual]
    st.subheader('Resultados de la búsqueda')
    st.dataframe(df_filtrado_manual)
