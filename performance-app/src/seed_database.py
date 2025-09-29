import random
import argparse
from datetime import datetime, timedelta
from database import create_db_pool
from seed_utils import get_random_product_price, get_seller_type, get_product_category, get_seller_city, get_random_product_rating, get_random_seller_rating

# Fixed seed for reproducible data
RANDOM_SEED = 42

NOW = datetime(2025, 9, 29)

# Data generation parameters
NUM_SELLERS = 10000
NUM_PRODUCTS = 2000000
NUM_PRODUCT_REVIEWS = 10000000
NUM_SELLER_REVIEWS = 2500000
NUM_INVENTORY = 6000000


def seed_sellers(pool, num_sellers):
    """Seed sellers table"""
    print(f"Inserting {num_sellers} sellers...")

    batch_size = 50000
    batch_data = []

    with pool.connection() as conn:
        conn.autocommit = False

        for seller_id in range(1, num_sellers + 1):
            seller_type = get_seller_type(seller_id)
            location = get_seller_city(seller_id).value
            days_ago = random.randint(0, 1825)
            join_date = NOW - timedelta(days=days_ago)

            batch_data.append(
                (seller_id, seller_type.value, location, join_date))

            if seller_id % batch_size == 0 or seller_id == num_sellers:
                with conn.cursor() as cur:
                    cur.executemany(
                        "INSERT INTO sellers (id, seller_type, location, join_date) VALUES (%s, %s, %s, %s)",
                        batch_data
                    )
                conn.commit()

                batch_end = seller_id
                batch_start = batch_end - len(batch_data) + 1
                print(f"Inserted sellers {batch_start}-{batch_end}")
                batch_data = []


def seed_products(pool, num_products):
    """Seed products table"""
    print(f"Inserting {num_products} products...")

    batch_size = 50000
    batch_data = []

    with pool.connection() as conn:
        conn.autocommit = False

        for product_id in range(1, num_products + 1):
            category = get_product_category(product_id)

            released_days_ago = random.randint(0, 3650)
            released_date = NOW - timedelta(days=released_days_ago)

            discontinued_date = None
            if random.random() < 0.5 and released_days_ago > 0:
                # Product can only be discontinued if it wasn't released today
                # discontinued_days_ago must be between 0 and released_days_ago (inclusive)
                discontinued_days_ago = random.randint(
                    0, released_days_ago)
                discontinued_date = NOW - timedelta(days=discontinued_days_ago)

            batch_data.append(
                (product_id, category.value, released_date, discontinued_date))

            if product_id % batch_size == 0 or product_id == num_products:
                with conn.cursor() as cur:
                    cur.executemany(
                        "INSERT INTO products (id, category, released_date, discontinued_date) VALUES (%s, %s, %s, %s)",
                        batch_data
                    )
                conn.commit()

                batch_end = product_id
                batch_start = batch_end - len(batch_data) + 1
                print(f"Inserted products {batch_start}-{batch_end}")
                batch_data = []


def seed_product_reviews(pool, num_reviews, max_product_id):
    """Seed product_reviews table"""
    print(f"Inserting {num_reviews} product reviews...")

    batch_size = 50000
    batch_data = []

    with pool.connection() as conn:
        conn.autocommit = False

        for review_id in range(1, num_reviews + 1):
            product_id = random.randint(1, max_product_id)
            rating = get_random_product_rating(product_id)
            review_days_ago = random.randint(0, 730)
            review_date = NOW - timedelta(days=review_days_ago)

            batch_data.append((review_id, product_id, rating, review_date))

            if review_id % batch_size == 0 or review_id == num_reviews:
                with conn.cursor() as cur:
                    cur.executemany(
                        "INSERT INTO product_reviews (id, product_id, rating, review_date) VALUES (%s, %s, %s, %s)",
                        batch_data
                    )
                conn.commit()

                batch_end = review_id
                batch_start = batch_end - len(batch_data) + 1
                print(f"Inserted product reviews {batch_start}-{batch_end}")
                batch_data = []


def seed_seller_reviews(pool, num_reviews, max_seller_id):
    """Seed seller_reviews table"""
    print(f"Inserting {num_reviews} seller reviews...")

    batch_size = 50000
    batch_data = []

    with pool.connection() as conn:
        conn.autocommit = False

        for review_id in range(1, num_reviews + 1):
            seller_id = random.randint(1, max_seller_id)
            rating = get_random_seller_rating(seller_id)
            review_days_ago = random.randint(0, 730)
            review_date = NOW - timedelta(days=review_days_ago)

            batch_data.append((review_id, seller_id, rating, review_date))

            if review_id % batch_size == 0 or review_id == num_reviews:
                with conn.cursor() as cur:
                    cur.executemany(
                        "INSERT INTO seller_reviews (id, seller_id, rating, review_date) VALUES (%s, %s, %s, %s)",
                        batch_data
                    )
                conn.commit()

                batch_end = review_id
                batch_start = batch_end - len(batch_data) + 1
                print(f"Inserted seller reviews {batch_start}-{batch_end}")
                batch_data = []


def seed_seller_inventory(pool, num_inventory, max_product_id, max_seller_id):
    """Seed seller_inventory table with realistic pricing using deterministic prices"""

    max_items_by_seller_type = {
        'individual': 50,
        'professional': 200,
        'small_business': 1000,
        'enterprise': 5000,
        'wholesaler': 10000
    }

    batch_size = 50000
    batch_data = []
    inventory_id = 0

    with pool.connection() as conn:
        conn.autocommit = False

        for seller_id in range(1, max_seller_id + 1):
            seller_type = get_seller_type(seller_id)
            max_items = max_items_by_seller_type[seller_type.value]

            # Random number of items from 0 to max for this seller type
            items_for_this_seller = random.randint(0, max_items)

            # Ensure we don't exceed available products
            items_for_this_seller = min(items_for_this_seller, max_product_id)

            # Skip sellers with 0 items
            if items_for_this_seller == 0:
                continue

            # Pick random unique products for this seller
            product_ids = random.sample(
                range(1, max_product_id + 1), items_for_this_seller)

            for product_id in product_ids:
                inventory_id += 1

                quantity = random.randint(0, 1000)
                price = get_random_product_price(product_id, seller_id)

                # Random last updated within 6 months
                last_updated_days_ago = random.randint(0, 180)
                last_updated = NOW - timedelta(days=last_updated_days_ago)

                batch_data.append(
                    (inventory_id, product_id, seller_id, quantity, price, last_updated))

                if len(batch_data) >= batch_size:
                    with conn.cursor() as cur:
                        cur.executemany(
                            "INSERT INTO seller_inventory (id, product_id, seller_id, quantity, price, last_updated) VALUES (%s, %s, %s, %s, %s, %s)",
                            batch_data
                        )
                    conn.commit()

                    batch_end = inventory_id
                    batch_start = batch_end - len(batch_data) + 1
                    print(
                        f"Inserted seller inventory {batch_start}-{batch_end}")
                    batch_data = []

        # Insert any remaining data
        if batch_data:
            with conn.cursor() as cur:
                cur.executemany(
                    "INSERT INTO seller_inventory (id, product_id, seller_id, quantity, price, last_updated) VALUES (%s, %s, %s, %s, %s, %s)",
                    batch_data
                )
            conn.commit()

            batch_end = inventory_id
            batch_start = batch_end - len(batch_data) + 1
            print(f"Inserted seller inventory {batch_start}-{batch_end}")

    print(f"Completed inserting {inventory_id} seller inventory records")


def main():
    """Main function to seed all tables with dummy data"""
    import time

    parser = argparse.ArgumentParser(
        description='Seed database with test data')
    parser.add_argument('--sample', action='store_true',
                        help='Use 1% sample of data for quick testing')
    args = parser.parse_args()

    # Apply sample scaling if requested
    scale_factor = 0.01 if args.sample else 1.0
    num_sellers = max(1, int(NUM_SELLERS * scale_factor))
    num_products = max(1, int(NUM_PRODUCTS * scale_factor))
    num_product_reviews = max(1, int(NUM_PRODUCT_REVIEWS * scale_factor))
    num_seller_reviews = max(1, int(NUM_SELLER_REVIEWS * scale_factor))
    num_inventory = max(1, int(NUM_INVENTORY * scale_factor))

    random.seed(RANDOM_SEED)
    print(f"Using random seed: {RANDOM_SEED}")
    if args.sample:
        print("Using sample mode (1% of data)")
    print(f"Generating data: {num_sellers} sellers, {num_products} products, {num_product_reviews} product reviews, {num_seller_reviews} seller reviews, {num_inventory} inventory records")

    pool = create_db_pool()

    try:
        start_time = time.time()

        seed_sellers(pool, num_sellers)
        seed_products(pool, num_products)
        seed_product_reviews(pool, num_product_reviews, num_products)
        seed_seller_reviews(pool, num_seller_reviews, num_sellers)
        seed_seller_inventory(pool, num_inventory, num_products, num_sellers)

        end_time = time.time()
        duration = end_time - start_time

        print(f"\nData seeding completed in {duration:.2f} seconds")
        total_records = num_sellers + num_products + \
            num_product_reviews + num_seller_reviews + num_inventory
        print(f"Total records created: {total_records}")

    except Exception as e:
        print(f"Error during data seeding: {e}")
        raise
    finally:
        pool.close()


if __name__ == "__main__":
    main()
