-- Oracle init-script
-- Kjøres automatisk av gvenzl/oracle-free ved første oppstart
-- Alt kjøres i FREEPDB1 (pluggable database)

ALTER SESSION SET CONTAINER = FREEPDB1;

-- Opprett demo-bruker
CREATE USER demo_user IDENTIFIED BY password;
GRANT CREATE SESSION TO demo_user;
GRANT RESOURCE TO demo_user;
GRANT CREATE TABLE TO demo_user;
GRANT UNLIMITED TABLESPACE TO demo_user;
GRANT SELECT ANY DICTIONARY TO demo_user;
GRANT DATAPUMP_EXP_FULL_DATABASE TO demo_user;
GRANT DATAPUMP_IMP_FULL_DATABASE TO demo_user;
GRANT READ, WRITE ON DIRECTORY data_pump_dir TO demo_user;

-- Opprett katalog som peker på /backup (montert til oracle/backup/ på host)
CREATE OR REPLACE DIRECTORY backup_dir AS '/backup';
GRANT READ, WRITE ON DIRECTORY backup_dir TO demo_user;

-- Opprett schema: en enkel nettbutikk
CREATE TABLE demo_user.customers (
    id         NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name       VARCHAR2(100) NOT NULL,
    email      VARCHAR2(200) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE TABLE demo_user.products (
    id    NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name  VARCHAR2(100) NOT NULL,
    price NUMBER(10, 2) NOT NULL,
    stock NUMBER DEFAULT 0 NOT NULL
);

CREATE TABLE demo_user.orders (
    id          NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id NUMBER REFERENCES demo_user.customers(id),
    product_id  NUMBER REFERENCES demo_user.products(id),
    quantity    NUMBER NOT NULL,
    ordered_at  TIMESTAMP DEFAULT SYSTIMESTAMP
);

-- Aktiver ROW MOVEMENT (pakrevd for Flashback Table)
ALTER TABLE demo_user.orders ENABLE ROW MOVEMENT;
ALTER TABLE demo_user.customers ENABLE ROW MOVEMENT;

-- Testdata: kunder
INSERT INTO demo_user.customers (name, email) VALUES ('Alice Hansen',    'alice@example.com');
INSERT INTO demo_user.customers (name, email) VALUES ('Bob Nilsen',      'bob@example.com');
INSERT INTO demo_user.customers (name, email) VALUES ('Carol Olsen',     'carol@example.com');
INSERT INTO demo_user.customers (name, email) VALUES ('David Berg',      'david@example.com');
INSERT INTO demo_user.customers (name, email) VALUES ('Eva Kristiansen', 'eva@example.com');

-- Testdata: produkter
INSERT INTO demo_user.products (name, price, stock) VALUES ('Tastatur',   599.00, 50);
INSERT INTO demo_user.products (name, price, stock) VALUES ('Mus',        299.00, 80);
INSERT INTO demo_user.products (name, price, stock) VALUES ('Skjerm',    3499.00, 20);
INSERT INTO demo_user.products (name, price, stock) VALUES ('Headset',    899.00, 35);
INSERT INTO demo_user.products (name, price, stock) VALUES ('Webkamera',  749.00, 25);

-- Testdata: bestillinger
INSERT INTO demo_user.orders (customer_id, product_id, quantity) VALUES (1, 1, 1);
INSERT INTO demo_user.orders (customer_id, product_id, quantity) VALUES (1, 3, 2);
INSERT INTO demo_user.orders (customer_id, product_id, quantity) VALUES (2, 2, 1);
INSERT INTO demo_user.orders (customer_id, product_id, quantity) VALUES (3, 4, 1);
INSERT INTO demo_user.orders (customer_id, product_id, quantity) VALUES (4, 5, 2);
INSERT INTO demo_user.orders (customer_id, product_id, quantity) VALUES (5, 1, 1);
INSERT INTO demo_user.orders (customer_id, product_id, quantity) VALUES (2, 3, 1);
INSERT INTO demo_user.orders (customer_id, product_id, quantity) VALUES (3, 2, 3);

COMMIT;
