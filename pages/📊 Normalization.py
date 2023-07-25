import pandas as pd
from transformers import BertTokenizer, BertModel
import torch
import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

def normalize_with_nltk(text):
    stop_words = set(stopwords.words('spanish'))
    stemmer = SnowballStemmer('spanish')

    tokens = word_tokenize(text)
    filtered_tokens = [stemmer.stem(token) for token in tokens if token not in stop_words]
    return " ".join(filtered_tokens)

def normalize_with_bert(text):
    tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
    model = BertModel.from_pretrained('bert-base-multilingual-cased')

    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    embeddings = torch.mean(outputs.last_hidden_state, dim=1)
    normalized_text = " ".join([token for token in tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])])
    return normalized_text

def main():
    df_supermercado1 = pd.read_csv('Plaza Vea.csv')
    df_supermercado2 = pd.read_csv('Tottus.csv')
    df_supermercado3 = pd.read_csv('Metro.csv')

    df_total = pd.concat([df_supermercado1, df_supermercado2, df_supermercado3])

    df_total['Lista de Productos'] = df_total['Lista de Productos'].str.lower()

    st.subheader('Datos originales')
    st.dataframe(df_total)

    if st.sidebar.button('Normalizar Data con NLTK'):
        df_total['Lista de Productos Normalizados'] = df_total['Lista de Productos'].apply(normalize_with_nltk)
        st.sidebar.success('¡Normalización de datos con NLTK completada!')

    if st.sidebar.button('Normalizar Data con BERT'):
        df_total['Lista de Productos Normalizados'] = df_total['Lista de Productos'].apply(normalize_with_bert)
        st.sidebar.success('¡Normalización de datos con BERT completada!')

    if 'Lista de Productos Normalizados' in df_total:
        st.subheader('Datos normalizados')
        st.dataframe(df_total[['Lista de Productos Normalizados']])

        df_total.to_csv('prod_normalizados.csv', index=False)

if __name__ == '__main__':
    main()
