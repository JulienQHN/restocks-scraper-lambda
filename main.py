import os
import requests as rq
import json
import sys
from dotenv import load_dotenv

load_dotenv()

# Get the values of the variables from .env using the os library:
BASE = os.environ.get("BASE")
FILTERS = os.environ.get("FILTERS")
COUNTRY = os.environ.get('COUNTRY')

current_collection = []
products_added = 0
page = 1

with open('datas.json', 'r') as f:
    current_collection = json.load(f)
    current_collection[::-1]

print("Scrapping in progress ...")


def scrap(page, current_collection, products_added):
    url = f"{BASE}/{COUNTRY}/shop/search?q=&page={page}&{FILTERS}"
    request = rq.get(url)
    data = request.json()

    while page != 0:
        url = f"{BASE}/{COUNTRY}/shop/search?q=&page={page}&{FILTERS}"
        request = rq.get(url)
        data = request.json()
        print(f"Scraping page {page}, please wait...")

        if data['data'] == []:
            print(f'Successfully scraped everypage {page}')
            break
        elif request.status_code != 200:
            print(f"error happening during request, at page {page}")
            break

        # Stores particular details in array
        for product in data['data']:
            if product['id'] == current_collection[products_added]['id']:

                # paste the results into a json file
                with open('datas.json', 'w') as f:
                    json.dump(current_collection, f)

                print(f'Number of items found : {products_added} !')
                print("Collection up to date !")
                os._exit(os.X_OK)

            else:
                product_useful = {
                    'id': product['id'],
                    'brand_id': product['brand_id'],
                    'sku': product['sku'],
                    'name': product['name'],
                    'image': product['image']}

                current_collection.insert(products_added, product_useful)
                products_added += 1
                print(f"Item {product['sku']} added in the collection !")

        # iterate over all the pages
        page += 1

    # paste the results into a json file
    with open('datas.json', 'w') as f:
        json.dump(current_collection, f)


if __name__ == '__main__':
    scrap(page, current_collection, products_added)
