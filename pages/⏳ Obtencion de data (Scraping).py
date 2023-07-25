import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup as bs
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import requests
import os
from datetime import datetime

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

url_list = ['https://www.plazavea.com.pe/abarrotes?page=1']

item_names = []
item_prices = []
item_discounts = []
item_brand = []
image_urls = []

def scrape_data(url):
    page = requests.get(url)
    soup = bs(page.content, 'html.parser')

    prod_name = soup.find_all('a', {'class': 'Showcase__name'})
    price = soup.find_all('div', {'class': 'Showcase__salePrice'})
    brand_name = soup.find_all('div', {'class': 'Showcase__brand'})
    image_urls.extend([img['src'] for img in soup.select('figure.Showcase__photo img[src]')])

    item_data = []
    for name, price, brand in zip(prod_name, price, brand_name):
        price_text = price.text.strip()
        discount = None

        if '-' in price_text:
            price_parts = price_text.split('-')
            price_text = price_parts[0].strip()
            discount = price_parts[1].strip()

        item_data.append((name.text, price_text, discount, brand.text))

    return item_data

def scrape_plaza_vea():
    num_threads = 8
    supermarket_name = 'Plaza Vea'
    with st.spinner('Realizando web scraping en Plaza Vea...'):
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            results = executor.map(scrape_data, url_list)
            for result in results:
                item_names.extend([item[0] for item in result])
                item_prices.extend([item[1] for item in result])
                item_discounts.extend([item[2] for item in result])
                item_brand.extend([item[3] for item in result])

        df = pd.DataFrame({'Lista de Productos': item_names, 'Precios': item_prices, 'Descuento': item_discounts, 'Marca': item_brand, 'Supermercado': supermarket_name, 'Image URL': image_urls})
        df.to_csv('Plaza Vea.csv', index=False)

    st.success('¡Web scraping de Plaza Vea completado! Los datos se han guardado en "data_productos_plaza_vea_streamlit.csv".')

def scrape_tottus():
    url_list = ['https://tottus.falabella.com.pe/tottus-pe/category/cat13380487/Despensa?subdomain=tottus&page=' + str(i)for i in range(1, 20)]
    item_names = []
    item_prices = []
    item_discounts = []
    item_brand = []

    def scrape_data(url):
        page = requests.get(url)
        soup = bs(page.content, 'html.parser')

        prod_name = soup.find_all('b', {'class': 'jsx-1833870204 copy2 primary jsx-2889528833 normal pod-subTitle subTitle-rebrand'})
        prices = soup.find_all('li', {'class': 'jsx-2112733514 prices-0'})
        brand_name = soup.find_all('b', {'class': 'jsx-1833870204'})

        item_data = []
        for name, price, brand in zip(prod_name, prices, brand_name):
            price_text = price.text.strip()
            discount = None

            if '-' in price_text:
                price_parts = price_text.split('-')
                price_text = price_parts[0].strip()
                discount = price_parts[1].strip()

            item_data.append((name.text, price_text, discount, brand.text))

        return item_data

    num_threads = 8
    supermarket_name = 'Tottus'
    with st.spinner('Realizando web scraping en Tottus...'):
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            results = executor.map(scrape_data, url_list)
            for result in results:
                item_names.extend([item[0] for item in result])
                item_prices.extend([item[1] for item in result])
                item_discounts.extend([item[2] for item in result])
                item_brand.extend([item[3] for item in result])

        df = pd.DataFrame({'Lista de Productos': item_names,'Precios': item_prices,'Descuento': item_discounts,'Marca': item_brand,'Supermercado': supermarket_name})
        df.to_csv('Tottus.csv', index=False)

    st.success('¡Web scraping de Tottus completado! Los datos se han guardado en "data_productos_tottus.csv".')

def scrape_metro():
    driver = webdriver.Chrome()
    url = 'https://www.metro.pe/abarrotes'
    driver.get(url)

    def scroll_down():
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    scroll_down()
    page_source = driver.page_source
    driver.quit()

    item_names = []
    item_prices = []
    item_discounts = []
    item_brand = []

    soup = bs(page_source, 'html.parser')
    prod_name = soup.find_all('a', {'class': 'product-item__name'})
    prices = soup.find_all('span', {'class': 'product-prices__value product-prices__value--best-price'})
    brand_name = soup.find_all('div', {'class': 'product-item__brand'})
    discounts = soup.find_all('div', {'class': 'flag discount-percent'})
    supermarket_name = 'Metro'

    for name, price, brand, discount in zip(prod_name, prices, brand_name, discounts):
        item_names.append(name.text)
        item_prices.append(price.text.strip())
        item_discounts.append(discount.text.strip())
        item_brand.append(brand.text)

    df = pd.DataFrame({'Lista de Productos': item_names, 'Precios': item_prices, 'Descuento': item_discounts, 'Marca': item_brand, 'Supermercado': supermarket_name})
    df.to_csv('Metro.csv', index=False)

    st.success('¡Web scraping de Metro completado! Los datos se han guardado en "data_productos_metro.csv".')

def main():
    image_path = './img/price.png' 
    st.sidebar.image(image_path, use_column_width=True)
    with st.sidebar:
        if st.button('Obtener datos de Plaza Vea'):
            scrape_plaza_vea()
        if st.button('Obtener datos de Tottus'):
            scrape_tottus()
        if st.button('Obtener datos de Metro'):
            scrape_metro()
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    selected_file = st.sidebar.selectbox("Seleccionar archivo CSV:", csv_files)
    if selected_file:
        df = pd.read_csv(selected_file)
        if st.button('Mostrar Data'):
            st.write("Contenido del archivo CSV:")
            st.write(df)
        if st.button('Guardar Data en nuevo CSV'):
            csv_files = [f for f in os.listdir('data') if f.endswith('.csv')]
            current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
            new_csv_file = f'data/data_productos_{current_datetime}.csv'
            df.to_csv(new_csv_file, index=False)
            st.success(f'¡Datos guardados en el nuevo archivo CSV: {new_csv_file}!')
if __name__ == '__main__':
    main()