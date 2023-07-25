import streamlit as st
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

def cluster_data():
    df_total = pd.read_csv('prod_normalizados_nltk.csv')

    tfidf_vectorizer = TfidfVectorizer()

    tfidf_matrix = tfidf_vectorizer.fit_transform(df_total['Lista de Productos Normalizados'])

    num_clusters = 10
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(tfidf_matrix)

    df_total['Cluster'] = kmeans.labels_

    df_total.drop(columns=['Image URL'], inplace=True)

    df_total.to_csv('productos_clustering_kmeans.csv', index=False)

    st.sidebar.success('¡Clusterización completada! Los resultados se han guardado en "productos_clustering_kmeans.csv".')

def show_clusters():
    df_clusters = pd.read_csv('productos_clustering_kmeans.csv')

    if not df_clusters.empty:
        st.subheader('Resultados de Clusterización')
        st.dataframe(df_clusters)

def main():
    image_path = './img/custer.png'  
    st.sidebar.image(image_path, use_column_width=True)

    if st.sidebar.button('Iniciar Clusterización'):
        cluster_data()

    if st.sidebar.button('Mostrar Resultados de Clusterización'):
        show_clusters()

if __name__ == '__main__':
    main()
