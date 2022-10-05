import os
import requests as rq
import json
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Get the values of the variables from .env using the os library:
BASEURL = os.environ.get("BASEURL")
FILTERS = os.environ.get("FILTERS")
COUNTRY = os.environ.get('COUNTRY')

# Initialize useful variables
page = 1
products_added = 0
current_collection = []
url = f"{BASEURL}/{COUNTRY}/shop/search?q=&page={page}&{FILTERS}"

# Open the json file where the collection is stored
with open('datas.json', 'r') as f:
    current_collection = json.load(f)
    current_collection[::-1]


def scrap(page, products_added, current_collection, url):
    print("Scrapping in progress ...")
    while page != 0:
        url = f"{BASEURL}/{COUNTRY}/shop/search?q=&page={page}&{FILTERS}"
        try:
            request = rq.get(url)
            request.raise_for_status()
            data = request.json()

        # Check if the request fail, exit immediately and return the error in the console
        except rq.exceptions.HTTPError as err:
            print(f"error happening during request, at page {page}")
            raise SystemExit(err) from err

        print(f"Scraping page {page}, please wait...")

        # If first time scraping then this print will appear in the console after the last page scraped
        if data['data'] == []:
            print(f'Successfully scraped everypage, last page was {page}')
            break

        # Stores particular details in array
        for product in data['data']:
            # If next product scraper match with last first product saved in json file then update and exit
            if product['id'] == current_collection[products_added]['id'] and products_added != 0:

                # paste the new collection of current_collection object into json file
                with open('datas.json', 'w') as f:
                    json.dump(current_collection, f)

                print(f'Number of items found : {products_added}')
                print("Collection up to date !")
                os._exit(os.X_OK)

            # If first product scraper match with first product saved in json file then exit
            elif product['id'] == current_collection[products_added]['id']:
                print("Collection is already up to date !")
                os._exit(os.X_OK)

            # If new product scraped restructure to keep usefull informations and insert in the collection array
            else:
                product_useful = {
                    'id': product['id'],
                    'brand_id': product['brand_id'],
                    'sku': product['sku'],
                    'name': product['name'],
                    'image': product['image']}

                # Insert product in  the collection array, product_added ensures the insertion of the product in the right direction
                current_collection.insert(products_added, product_useful)
                products_added += 1
                print(f"Item {product['sku']} added in the collection !")

        # Iterate over all the pages by incrementing page variable after each request
        page += 1

    # Paste result into json file
    with open('datas.json', 'w') as f:
        json.dump(current_collection, f)


# Start scraping fuction after everything loaded
if __name__ == '__main__':
    scrap(page, products_added, current_collection, url)
