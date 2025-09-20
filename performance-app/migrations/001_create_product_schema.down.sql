-- Drop tables in reverse order (children first, then parents)
DROP TABLE IF EXISTS seller_inventory;
DROP TABLE IF EXISTS seller_reviews;
DROP TABLE IF EXISTS product_reviews;
DROP TABLE IF EXISTS sellers;
DROP TABLE IF EXISTS products;

-- Drop enum types
DROP TYPE IF EXISTS seller_location;
DROP TYPE IF EXISTS seller_type;
DROP TYPE IF EXISTS product_category;