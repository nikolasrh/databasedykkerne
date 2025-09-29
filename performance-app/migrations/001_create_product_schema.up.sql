CREATE TYPE product_category AS ENUM ('electronics', 'books', 'clothing', 'rare_collectibles', 'vintage');

CREATE TYPE seller_type AS ENUM ('individual', 'professional', 'small_business', 'enterprise', 'wholesaler');

CREATE TYPE seller_location AS ENUM (
    'oslo', 'trondheim', 'bergen', 'stavanger', 'stockholm', 'gothenburg', 'malmo',
    'copenhagen', 'aarhus', 'helsinki', 'tampere', 'london', 'manchester', 'birmingham',
    'paris', 'lyon', 'marseille', 'berlin', 'munich', 'hamburg', 'madrid', 'barcelona',
    'valencia', 'rome', 'milan', 'naples', 'amsterdam', 'rotterdam', 'the_hague',
    'vienna', 'brussels', 'antwerp', 'zurich', 'geneva', 'dublin', 'prague', 'budapest',
    'warsaw', 'krakow', 'lisbon', 'porto', 'athens', 'thessaloniki'
);

CREATE TABLE sellers (
    id INTEGER PRIMARY KEY,
    seller_type seller_type NOT NULL,
    location seller_location NOT NULL,
    join_date DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    category product_category NOT NULL,
    released_date DATE NOT NULL,
    discontinued_date DATE,
    CHECK (
        discontinued_date IS NULL
        OR discontinued_date >= released_date
    )
);

CREATE TABLE product_reviews (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products (id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (
        rating >= 1
        AND rating <= 5
    ),
    review_date DATE NOT NULL
);

CREATE TABLE seller_reviews (
    id INTEGER PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES sellers (id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (
        rating >= 1
        AND rating <= 5
    ),
    review_date DATE NOT NULL
);

CREATE TABLE seller_inventory (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products (id) ON DELETE CASCADE,
    seller_id INTEGER NOT NULL REFERENCES sellers (id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 0,
    price DECIMAL(10, 2) NOT NULL,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (product_id, seller_id)
);
