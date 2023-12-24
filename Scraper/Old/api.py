from cassandra.cluster import Cluster
import requests
import re
import json

with open('pais.json', 'r') as paisfile:
    pais = json.loads(paisfile.read())

cluster = Cluster([('127.0.0.1', 55003)])
session = cluster.connect('product_store')


def get_prod(prod_url: str):
    prod = session.execute('SELECT * FROM product_store.products WHERE prod_url = %(prod_url)s',
                           {'prod_url': prod_url}).one()
    return prod


def add_prod(prod_url: str) -> bool:
    if get_prod(prod_url):
        return False

    prod_id = re.search('^.*?-[0-9]*', prod_url).group()[:-11]  # TODO checkear
    data = requests.get(f"https://api.mercadolibre.com/items?ids={prod_id}")
    if data.status_code == 200:
        data = data.json()
        # TODO handle error
        session.execute(
            "INSERT INTO product_store.products (prod_url, updated, name, price, currency, source, country) "
            "VALUES (%(url)s, TOTIMESTAMP(NOW()), %(name)s, %(price)s, %(currency)s, %(source)s, %(country)s);",
            {"url": prod_url, "name": data['title'], "price": data['price'], "currency": data['currency_id'],
             "source": 'MercadoLibre', "country": pais[data['site_id']]}
        )
        return True
    else:
        print("Error:", data.status_code)
        print(data.text)
        return False


def get_basket(name: str) -> list:
    basket = session.execute("SELECT * FROM product_store.baskets "
                             "WHERE name = %(name)s",
                             {"name": name}).all()
    return basket
