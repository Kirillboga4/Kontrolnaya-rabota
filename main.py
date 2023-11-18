import requests
from bs4 import BeautifulSoup
import openpyxl
import pandas as pd

def parse_category(category_url, output_txt, output_excel):
    response = requests.get(category_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        products = soup.find_all('div', class_='product')

        with open(output_txt, 'w', encoding='utf-8') as txt_file:
            for product in products:
                product_name = product.find('h2').text.strip()
                review_count = product.find('span', class_='review-count').text.strip()
                price = product.find('span', class_='price').text.strip()

                print(f'Назва товару: {product_name}, Кількість відгуків: {review_count}, Ціна: {price}')

                txt_file.write(f'Назва товару: {product_name}, Кількість відгуків: {review_count}, Ціна: {price}\n')

        df = pd.DataFrame(columns=['Назва товару', 'Кількість відгуків', 'Ціна'])
        for product in products:
            product_name = product.find('h2').text.strip()
            review_count = product.find('span', class_='review-count').text.strip()
            price = product.find('span', class_='price').text.strip()

            df = df.append({'Назва товару': product_name, 'Кількість відгуків': review_count, 'Ціна': price},
                           ignore_index=True)

        df.to_excel(output_excel, index=False)

    else:
        print(f'Помилка {response.status_code}. Спробуйте пізніше.')

# Приклад використання
category_url_televizory = 'https://allo.ua/ua/televizory/'
parse_category(category_url_televizory, 'televizory.txt', 'televizory.xlsx')

category_url_zarjadnye_stancii = 'https://allo.ua/ua/zarjadnye-stancii/'
parse_category(category_url_zarjadnye_stancii, 'zarjadnye-stancii.txt', 'zarjadnye-stancii.xlsx')
