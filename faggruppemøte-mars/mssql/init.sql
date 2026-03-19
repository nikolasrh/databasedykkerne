-- Opprett demo-database
CREATE DATABASE demo_db;
GO

USE demo_db;
GO

-- Opprett bruker
CREATE LOGIN demo_user WITH PASSWORD = 'Password123!';
CREATE USER demo_user FOR LOGIN demo_user;
ALTER ROLE db_owner ADD MEMBER demo_user;
GO

-- Opprett schema: en enkel nettbutikk
CREATE TABLE customers (
    id         INT IDENTITY(1,1) PRIMARY KEY,
    name       NVARCHAR(100) NOT NULL,
    email      NVARCHAR(200) NOT NULL UNIQUE,
    created_at DATETIME2 DEFAULT GETDATE()
);
GO

CREATE TABLE products (
    id    INT IDENTITY(1,1) PRIMARY KEY,
    name  NVARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0
);
GO

CREATE TABLE orders (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    product_id  INT REFERENCES products(id),
    quantity    INT NOT NULL,
    ordered_at  DATETIME2 DEFAULT GETDATE()
);
GO

-- Testdata: kunder
INSERT INTO customers (name, email) VALUES
    ('Alice Hansen',    'alice@example.com'),
    ('Bob Nilsen',      'bob@example.com'),
    ('Carol Olsen',     'carol@example.com'),
    ('David Berg',      'david@example.com'),
    ('Eva Kristiansen', 'eva@example.com');
GO

-- Testdata: produkter
INSERT INTO products (name, price, stock) VALUES
    ('Tastatur',  599.00, 50),
    ('Mus',       299.00, 80),
    ('Skjerm',   3499.00, 20),
    ('Headset',   899.00, 35),
    ('Webkamera', 749.00, 25);
GO

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
GO
