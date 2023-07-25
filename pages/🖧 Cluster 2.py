import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def cluster_data():
    df_total = pd.read_csv('prod_normalizados_nltk.csv')

    df_total.drop(columns=['Image URL'], inplace=True)

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(df_total['Lista de Productos Normalizados'])

    num_clusters = 12
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(tfidf_matrix)

    df_total['Cluster'] = kmeans.labels_

    centroids = kmeans.cluster_centers_

    top_features_indices = centroids.argsort()[:, ::-1]

    feature_names = tfidf_vectorizer.get_feature_names_out()

    cluster_names = {}
    for cluster_num in range(num_clusters):
        top_terms = [feature_names[i] for i in top_features_indices[cluster_num][:3]]  # Mostrar las 3 palabras más importantes
        cluster_names[cluster_num] = ", ".join(top_terms)

    df_total['Nombre Cluster'] = df_total['Cluster'].map(cluster_names)

    df_total.to_csv('productos_clustering_kmeans_con_etiquetas.csv', index=False)

    return df_total

def show_clusters(df_clusters):
    if not df_clusters.empty:
        st.subheader('Resultados de Clusterización')
        st.dataframe(df_clusters)
    else:
        st.write('No se encontraron datos clusterizados. Por favor, realiza la clusterización primero.')

def main():
    image_path = './img/custer.png'  
    st.sidebar.image(image_path, use_column_width=True)

    st.sidebar.title('Aplicación de Clusterización de Productos')

    if st.sidebar.button('Iniciar Clusterización'):
        df_clusters = cluster_data()
        show_clusters(df_clusters)
if __name__ == '__main__':
    main()
