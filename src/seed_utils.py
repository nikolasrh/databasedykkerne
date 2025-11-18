"""
Utility functions for deterministic data generation in seed_database.py
"""

import random
from enum import Enum
from typing import List, Tuple, TypeVar

T = TypeVar('T')


class ProductCategory(Enum):
    """Product category enum matching the database enum"""
    ELECTRONICS = 'electronics'
    BOOKS = 'books'
    CLOTHING = 'clothing'
    VINTAGE = 'vintage'
    RARE_COLLECTIBLES = 'rare_collectibles'


class SellerType(Enum):
    """Seller type enum matching the database enum"""
    INDIVIDUAL = 'individual'
    PROFESSIONAL = 'professional'
    SMALL_BUSINESS = 'small_business'
    ENTERPRISE = 'enterprise'
    WHOLESALER = 'wholesaler'


class City(Enum):
    """European city enum matching the database values"""
    LONDON = 'london'
    PARIS = 'paris'
    BERLIN = 'berlin'
    MADRID = 'madrid'
    ROME = 'rome'
    AMSTERDAM = 'amsterdam'
    STOCKHOLM = 'stockholm'
    COPENHAGEN = 'copenhagen'
    OSLO = 'oslo'
    VIENNA = 'vienna'
    BRUSSELS = 'brussels'
    DUBLIN = 'dublin'
    PRAGUE = 'prague'
    BUDAPEST = 'budapest'
    WARSAW = 'warsaw'
    ATHENS = 'athens'
    LISBON = 'lisbon'
    MILAN = 'milan'
    BARCELONA = 'barcelona'
    MUNICH = 'munich'
    HAMBURG = 'hamburg'
    LYON = 'lyon'
    MARSEILLE = 'marseille'
    BIRMINGHAM = 'birmingham'
    MANCHESTER = 'manchester'
    NAPLES = 'naples'
    VALENCIA = 'valencia'
    GOTHENBURG = 'gothenburg'
    ROTTERDAM = 'rotterdam'
    ANTWERP = 'antwerp'
    HELSINKI = 'helsinki'
    KRAKOW = 'krakow'
    PORTO = 'porto'
    THESSALONIKI = 'thessaloniki'
    TRONDHEIM = 'trondheim'
    BERGEN = 'bergen'
    STAVANGER = 'stavanger'
    MALMO = 'malmo'
    AARHUS = 'aarhus'
    TAMPERE = 'tampere'
    THE_HAGUE = 'the_hague'
    ZURICH = 'zurich'
    GENEVA = 'geneva'


PRICE_RANGES = {
    ProductCategory.ELECTRONICS: (50.00, 2000.00),
    ProductCategory.CLOTHING: (10.00, 500.00),
    ProductCategory.BOOKS: (5.00, 100.00),
    ProductCategory.RARE_COLLECTIBLES: (100.00, 5000.00),
    ProductCategory.VINTAGE: (50.00, 1500.00),
}

WEIGHTED_PRODUCT_CATEGORIES = [
    (ProductCategory.ELECTRONICS, 30),      # 30%
    (ProductCategory.BOOKS, 30),            # 30%
    (ProductCategory.CLOTHING, 30),         # 30%
    (ProductCategory.VINTAGE, 9),           # 9%
    (ProductCategory.RARE_COLLECTIBLES, 1),  # 1%
]

WEIGHTED_SELLER_TYPES = [
    (SellerType.INDIVIDUAL, 40),        # 40%
    (SellerType.PROFESSIONAL, 25),      # 25%
    (SellerType.SMALL_BUSINESS, 20),    # 20%
    (SellerType.ENTERPRISE, 10),        # 10%
    (SellerType.WHOLESALER, 5),         # 5%
]

WEIGHTED_CITIES = [
    (City.LONDON, 1000),
    (City.PARIS, 900),
    (City.BERLIN, 800),
    (City.MADRID, 700),
    (City.ROME, 650),
    (City.AMSTERDAM, 600),
    (City.STOCKHOLM, 500),
    (City.COPENHAGEN, 450),
    (City.OSLO, 400),
    (City.VIENNA, 400),
    (City.MILAN, 400),
    (City.WARSAW, 350),
    (City.BARCELONA, 350),
    (City.BRUSSELS, 350),
    (City.DUBLIN, 300),
    (City.PRAGUE, 300),
    (City.BUDAPEST, 300),
    (City.MUNICH, 300),
    (City.ATHENS, 300),
    (City.LISBON, 250),
    (City.HAMBURG, 250),
    (City.LYON, 200),
    (City.BIRMINGHAM, 200),
    (City.HELSINKI, 200),
    (City.MARSEILLE, 180),
    (City.MANCHESTER, 180),
    (City.ROTTERDAM, 150),
    (City.NAPLES, 150),
    (City.KRAKOW, 150),
    (City.ZURICH, 150),
    (City.VALENCIA, 140),
    (City.GOTHENBURG, 120),
    (City.ANTWERP, 120),
    (City.PORTO, 120),
    (City.GENEVA, 120),
    (City.THE_HAGUE, 100),
    (City.THESSALONIKI, 100),
    (City.TRONDHEIM, 80),
    (City.MALMO, 80),
    (City.BERGEN, 70),
    (City.AARHUS, 70),
    (City.TAMPERE, 60),
    (City.STAVANGER, 50),
]

SELLER_TYPE_PRICE_FACTORS = {
    SellerType.WHOLESALER: (0.75, 1.05),      # -25% to +5%
    SellerType.ENTERPRISE: (0.95, 1.10),      # -5% to +10%
    SellerType.SMALL_BUSINESS: (0.85, 1.20),  # -15% to +20%
    SellerType.PROFESSIONAL: (0.90, 1.15),    # -10% to +15%
    SellerType.INDIVIDUAL: (0.80, 1.25),      # -20% to +25%
}


def weighted_choice(seed: int, choices: List[Tuple[T, int]]) -> T:
    """
    Generic weighted selection from any type of choices.

    Args:
        seed: Seed for deterministic random generation
        choices: List of (item, weight) tuples

    Returns:
        Selected item of type T

    Raises:
        ValueError: If choices is empty, any weight is non-positive, or selection fails
    """
    if not choices:
        raise ValueError("Cannot select from empty choices")

    total_weight = 0
    for item, weight in choices:
        if weight <= 0:
            raise ValueError(
                f"Weight must be positive, got {weight} for {item}")
        total_weight += weight

    target = random.Random(seed).uniform(0, total_weight)

    cumulative = 0
    for item, weight in choices:
        cumulative += weight
        if cumulative >= target:
            return item

    raise ValueError(f"Failed to select item: target={target}")


def get_product_category(product_id: int) -> ProductCategory:
    """
    Get deterministic category for a product.

    Args:
        product_id: Product ID

    Returns:
        Product category enum
    """
    seed = product_id
    return weighted_choice(seed, WEIGHTED_PRODUCT_CATEGORIES)


def get_random_product_price(product_id: int, seller_id: int) -> float:
    """
    Generate a price for a product based on its category and seller type.

    Args:
        product_id: Product ID
        seller_id: Seller ID

    Returns:
        Price as a float rounded to 2 decimal places
    """
    category = get_product_category(product_id)
    min_price, max_price = PRICE_RANGES[category]
    base_price = random.Random(product_id).uniform(min_price, max_price)

    seller_type = get_seller_type(seller_id)
    min_factor, max_factor = SELLER_TYPE_PRICE_FACTORS[seller_type]

    # Generate price factor using global random
    price_factor = random.uniform(min_factor, max_factor)

    price = base_price * price_factor
    return round(price, 2)


def get_seller_type(seller_id: int) -> SellerType:
    """
    Get deterministic seller type for a seller.

    Args:
        seller_id: Seller ID

    Returns:
        Seller type enum
    """
    return weighted_choice(seller_id, WEIGHTED_SELLER_TYPES)


def get_seller_city(seller_id: int) -> City:
    """
    Get deterministic city for a seller based on European city distribution.

    Args:
        seller_id: Seller ID

    Returns:
        City enum value
    """
    return weighted_choice(seller_id, WEIGHTED_CITIES)


def get_random_rating(seed: int) -> int:
    """Generate a single rating instance (1-5 stars)"""
    # Generate deterministic avg and stddev for seed
    deterministic_random = random.Random(seed)
    avg = deterministic_random.uniform(1.0, 5.0)
    stddev = deterministic_random.uniform(0.5, 1.5)

    # Generate the final rating with global random
    rating = random.gauss(avg, stddev)

    # Clamp to valid range and round to integer
    rating = max(1.0, min(5.0, rating))
    return round(rating)


def get_random_product_rating(product_id: int) -> int:
    """Generate a single rating instance for a product (1-5 stars)"""
    # Seed differently for products and sellers
    seed = product_id | (1 << 30)
    return get_random_rating(seed)


def get_random_seller_rating(seller_id: int) -> int:
    """Generate a single rating instance for a seller (1-5 stars)"""
    # Seed differently for products and sellers
    seed = seller_id | (2 << 30)
    return get_random_rating(seed)
