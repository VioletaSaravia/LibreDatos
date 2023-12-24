from cassandra.cluster import Cluster
import requests
import json
import re

sites = 'https://api.mercadolibre.com/sites'
sites = requests.get(sites)
sites_data = []
if sites.status_code == 200:
    sites_data = sites.json()
else:
    print("Error:", sites.status_code)
    print(sites.text)

pais = {}
for site in sites_data:
    pais[site['id']] = site['name']

with open("pais.json", "w", encoding='utf-8') as paisfile:
    json.dump(pais, paisfile)

cats_data = []
for site in sites_data:
    cats = f"https://api.mercadolibre.com/sites/{site['id']}/categories"
    cats = requests.get(cats)
    if cats.status_code == 200:
        cats_data.append(cats.json())
    else:
        print("Error:", cats.status_code)
        print(cats.text)

cats_data = cats_data[:1]

subcats = []
subcats_stack = [cat['id'] for site in cats_data for cat in site]

while len(subcats_stack) != 0:
    cat = subcats_stack.pop()
    subcats.append(cat)

    # TODO testing
    if len(subcats) > 100:
        break

    cat_data = requests.get(f"https://api.mercadolibre.com/categories/{cat}")
    if cat_data.status_code == 200:
        for subcat in cat_data.json()['children_categories']:
            subcats_stack.append(subcat['id'])
    else:
        print("Error:", cat_data.status_code)
        print(cat_data.text)

with open('subcats.txt', 'w', encoding='utf-8') as outfile:
    for cat in subcats:
        outfile.write(cat)
        outfile.write('\n')

products_data = []
with open('subcats.txt', 'r', encoding='utf-8') as subcatsfile:
    for cat in subcatsfile.read().splitlines():
        product = f"https://api.mercadolibre.com/sites/{cat[:3]}/search?category={cat}"
        product = requests.get(product)  # , params={'limit': 5000})
        if product.status_code == 200:
            products_data.append(product.json())
        else:
            print("Error:", product.status_code)
            print(product.text)

cluster = Cluster([('127.0.0.1', 55003)])
session = cluster.connect('product_store')

for search in products_data:
    for product in search['results']:
        url = re.search('^.*?-[0-9]*', product['permalink']).group()
        # TODO flatten
        session.execute(
            "INSERT INTO product_store.products (prod_url, updated, name, price, currency, source, country) "
            "VALUES (%(url)s, TOTIMESTAMP(NOW()), %(name)s, %(price)s, %(currency)s, %(source)s, %(country)s);",
            {"url": url, "name": product['title'], "price": product['price'],
             "currency": product['currency_id'], "source": 'MercadoLibre',
             "country": pais[product['site_id']]}
        )