import streamlit as st
from config import page_config
page_config()

image_path = './img/logo.png'
st.sidebar.image(image_path, use_column_width=True)

st.write("# Welcome to aplication  ")

st.markdown(
    """
    This study presents a Streamlit-based approach to address the lack of standardisation in product names and units
of measurement used by different supermarkets in Peru. Using machine learning and data mining techniques, it
seeks to achieve name normalisation, which facilitates direct price comparisons between supermarkets. The
results show that price standardisation and product name normalisation can improve price comparison between
supermarkets. In conclusion, this study provides a framework for future research on supermarket price analysis
in Latin America
"""
)
