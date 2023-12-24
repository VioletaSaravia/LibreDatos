DROP KEYSPACE IF EXISTS product_store;

CREATE KEYSPACE IF NOT EXISTS product_store WITH
        REPLICATION = {
            'class' : 'SimpleStrategy',
            'replication_factor' : '1'
            };

DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS baskets;

CREATE TYPE IF NOT EXISTS product_store.cat
    (
        source   text,
        country  text,
        category text
    );

CREATE TABLE IF NOT EXISTS product_store.products
(
    prod_url text,
    // TODO category frozen<list<text>> ???
    // category frozen<cat> static,
    source   text STATIC,
    country  text STATIC,
    category text STATIC,
    name     text,
    currency text,
    price    decimal,
    updated  timestamp,
    PRIMARY KEY ( prod_url, updated )
) WITH CLUSTERING ORDER BY (updated DESC);

CREATE INDEX ON products (country);
CREATE INDEX ON products (category);
CREATE INDEX ON products (source);

CREATE TABLE IF NOT EXISTS product_store.baskets
(
    name        text,
    prod_url    text,
    update_freq duration,
    PRIMARY KEY ( name )
    // influence float
);

CREATE INDEX ON baskets (prod_url);