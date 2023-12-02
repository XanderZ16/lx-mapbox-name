from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from pymongo import MongoClient
import requests

password = 'Aa13245768'
db_cdn = f'mongodb+srv://xander:{password}@cluster0.hgsq4xy.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(db_cdn)
db = client.dbxander

driver = webdriver.Edge()
url = 'https://www.yelp.com/search?cflt=restaurants&find_loc=Bras+Brasah%2C+Singapore'

driver.get(url)
sleep(5)
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
sleep(3)

map_api_token = "pk.eyJ1Ijoibm9jdHlzcyIsImEiOiJjbDh2aTFqY2gwZTlsM3ZxcTRnOGZ0b3hmIn0.CDy8vkgqrviTRnZ-0SXeow"
long = -122.420679
lat = 37.772537

start = 0
listed = {}

for _ in range(5):
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    restaurats = soup.select('div[class*="arrange-unit__"]')
    for restaurant in restaurats:
        restaurant_name = restaurant.select_one('div[class*="businessName__"]')

        # Check is that iteration have restaurant data
        if not restaurant_name: continue
        name = restaurant_name.text.split('.')[1].strip()

        # Cheking listed restaurant
        if name in listed: continue
        listed[name] = True

        # Get restaurant info
        link = restaurant_name.select_one('a')['href']
        link = 'https://www.yelp.com' + link
        restaurant_info = restaurant.select_one('div[class*="priceCategory__"]')
        category = restaurant_info.select_one('span:first-child').text
        location = restaurant_info.select_one('span:last-child').text
        
        geo_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json?proximity={long},{lat}&access_token={map_api_token}"
        geo_res = requests.get(geo_url)
        geo_json = geo_res.json()
        center = geo_json['features'][0]['center']

        # Make Document Each Restaurant
        doc = {
            'name': name,
            'link': link,
            'category': category,
            'location': location,
            'center': center
        }

        db.restaurants.insert_one(doc)

    start += 10
    driver.get(f'{url}start={start}')
    sleep(3)

driver.quit()