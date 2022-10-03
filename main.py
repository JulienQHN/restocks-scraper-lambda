import os
import requests as rq
import json
from dotenv import load_dotenv as env_load

env_load()

"""
scraper
"""

# Get the values of the variables from .env using the os library:
BASE = os.environ.get("BASE")
FILTERS = os.environ.get("FILTERS")
COUNTRY = os.environ.get('COUNTRY')

print("Scrapping in progress ...")
page = 1

def scrap(page):
    url = f"{BASE}/{COUNTRY}/shop/search?q=&page={page}&{FILTERS}"
    request = rq.get(url)
    data = request.json()
    total_results = []
    
    while data is not None:    
      url = f"{BASE}/{COUNTRY}/shop/search?q=&page={page}&{FILTERS}"  
      request = rq.get(url)
      data = request.json()
      print(f"Scraping page {page}, please wait...")
      
      if data['data'] == []:
          print(f'Successfully scraped everypage {page}')
          break
      elif data.status_code != 200:
          print(f"error happening during request, at page {page}")
          break
     
      # Stores particular details in array
    
      for product in data['data']:
          product_useful = {
              'id': product['id'], 
              'brand_id': product['brand_id'],
              'sku' :product['sku'],
              'name': product['name'], 
              'image': product['image']}
          total_results.append(product_useful)
    
      # iterate over all the pages                 
      page += 1
      
    # paste the results into a json file
    with open('datas.json', 'w') as f:
      json.dump(total_results, f)
    
if __name__ == '__main__':
  scrap(page)
