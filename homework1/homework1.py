"""
Источник: https://5ka.ru/special_offers/

Задача организовать сбор данных,
необходимо иметь метод сохранения данных в .json файлы

результат: Данные скачиваются с источника, при вызове метода/функции сохранения в файл скачанные данные сохраняются в Json вайлы, для каждой категории товаров должен быть создан отдельный файл и содержать товары исключительно соответсвующие данной категории.

пример структуры данных для файла:
нейминг ключей можно делать отличным от примера

{
"name": "имя категории",
"code": "Код соответсвующий категории (используется в запросах)",
"products": [{PRODUCT}, {PRODUCT}........] # список словарей товаров соответсвующих данной категории
}
"""


import requests
import json
from pathlib import Path

url_categ = "https://5ka.ru/api/v2/categories/716/"  # категории товаров
url = "https://5ka.ru/api/v2/special_offers/"  # акции


def get_category_products(url):
    params = {
        "records_per_page": 20,
    }

    # Получить список всех категорий

    response_cat: requests.Response = requests.get(url_categ, params=params)
    # response.encoding = 'windows-1251'

    if response_cat.status_code == 200:
        categ_list = response_cat.json()

    for cat_name in categ_list:
        params = {
            "records_per_page": 12,
            "categories": cat_name['group_code']
        }
        response_prod: requests.Response = requests.get(url, params=params)
        if response_prod.status_code == 200:
            # путь к файлу
            html_file_categ = Path(__file__).parent.joinpath(f'{cat_name["group_code"]}.json')
            # создаем начальный словарь
            response_prod_json = {"category_name": [], "category_code": []}
            # добовляем значения с кодом и названием категории
            response_prod_json.update(
                {"category_name": cat_name['group_name'], "category_code": cat_name['group_code']})
            # добавляем результат запроса товаров
            response_prod_json.update(response_prod.json())
            # cохраняем файл
            html_file_categ.write_text(json.dumps(response_prod_json, ensure_ascii=False))


get_category_products("https://5ka.ru/api/v2/special_offers/")









