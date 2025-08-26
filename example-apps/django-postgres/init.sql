CREATE USER django_user WITH PASSWORD 'password';

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

GRANT ALL PRIVILEGES ON TABLE items TO django_user;
