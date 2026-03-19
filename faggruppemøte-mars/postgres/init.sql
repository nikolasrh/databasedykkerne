-- Opprett demo-database og bruker
CREATE DATABASE demo_db;
CREATE USER demo_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE demo_db TO demo_user;

\connect demo_db

GRANT ALL ON SCHEMA public TO demo_user;

-- Opprett schema: en enkel nettbutikk
CREATE TABLE customers (
    id        SERIAL PRIMARY KEY,
    name      TEXT NOT NULL,
    email     TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE products (
    id          SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    price       NUMERIC(10, 2) NOT NULL,
    stock       INT NOT NULL DEFAULT 0
);

CREATE TABLE orders (
    id          SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    product_id  INT REFERENCES products(id),
    quantity    INT NOT NULL,
    ordered_at  TIMESTAMPTZ DEFAULT now()
);

-- Testdata: kunder
INSERT INTO customers (name, email) VALUES
    ('Alice Hansen',   'alice@example.com'),
    ('Bob Nilsen',     'bob@example.com'),
    ('Carol Olsen',    'carol@example.com'),
    ('David Berg',     'david@example.com'),
    ('Eva Kristiansen','eva@example.com');

-- Testdata: produkter
INSERT INTO products (name, price, stock) VALUES
    ('Tastatur',    599.00, 50),
    ('Mus',         299.00, 80),
    ('Skjerm',     3499.00, 20),
    ('Headset',     899.00, 35),
    ('Webkamera',   749.00, 25);

-- Testdata: bestillinger
INSERT INTO orders (customer_id, product_id, quantity) VALUES
    (1, 1, 1),
    (1, 3, 2),
    (2, 2, 1),
    (3, 4, 1),
    (4, 5, 2),
    (5, 1, 1),
    (2, 3, 1),
    (3, 2, 3);

