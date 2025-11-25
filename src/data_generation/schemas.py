"""Data generation schemas and configurations."""

from typing import List, Dict

# Automotive makes and their common models
AUTOMOTIVE_CATALOG = {
    "Toyota": ["Camry", "Corolla", "RAV4", "Highlander", "Tacoma", "Tundra", "4Runner"],
    "Honda": ["Civic", "Accord", "CR-V", "Pilot", "Ridgeline", "HR-V"],
    "Ford": ["F-150", "Mustang", "Explorer", "Escape", "Bronco", "Ranger", "Edge"],
    "Chevrolet": ["Silverado", "Equinox", "Tahoe", "Malibu", "Traverse", "Colorado"],
    "Nissan": ["Altima", "Rogue", "Sentra", "Pathfinder", "Frontier", "Murano"],
    "BMW": ["3 Series", "5 Series", "X3", "X5", "7 Series", "X1"],
    "Mercedes-Benz": ["C-Class", "E-Class", "GLE", "GLC", "S-Class", "GLA"],
    "Audi": ["A4", "Q5", "A6", "Q7", "A3", "Q3"],
    "Hyundai": ["Elantra", "Sonata", "Tucson", "Santa Fe", "Palisade", "Kona"],
    "Jeep": ["Wrangler", "Grand Cherokee", "Cherokee", "Gladiator", "Compass"],
}

# Vehicle categories mapping
CATEGORY_MAPPING = {
    "sedan": ["Camry", "Corolla", "Civic", "Accord", "Altima", "Malibu", "Sentra", "3 Series", "5 Series", "7 Series", "C-Class", "E-Class", "S-Class", "A4", "A6", "A3", "Elantra", "Sonata"],
    "suv": ["RAV4", "Highlander", "CR-V", "Pilot", "Explorer", "Escape", "Equinox", "Tahoe", "Traverse", "Rogue", "Pathfinder", "Murano", "X3", "X5", "X1", "GLE", "GLC", "GLA", "Q5", "Q7", "Q3", "Tucson", "Santa Fe", "Palisade", "Kona", "Grand Cherokee", "Cherokee", "Compass"],
    "truck": ["F-150", "Silverado", "Tacoma", "Tundra", "Ridgeline", "Ranger", "Frontier", "Colorado", "Gladiator"],
    "sports": ["Mustang"],
    "offroad": ["Wrangler", "Bronco", "4Runner"],
    "compact": ["HR-V", "Kona", "Compass"],
}

# MSRP ranges by category
MSRP_RANGES = {
    "sedan": (22000, 55000),
    "suv": (28000, 75000),
    "truck": (30000, 70000),
    "sports": (28000, 65000),
    "offroad": (35000, 60000),
    "compact": (20000, 35000),
}

# Trim levels
TRIM_LEVELS = ["Base", "LE", "XLE", "Limited", "Sport", "Touring", "Premium", "Luxury", "Ultimate"]

# Warehouse locations with regions
WAREHOUSE_LOCATIONS = [
    {"location": "Los Angeles Warehouse", "region": "West"},
    {"location": "San Francisco Warehouse", "region": "West"},
    {"location": "Chicago Warehouse", "region": "Midwest"},
    {"location": "Detroit Warehouse", "region": "Midwest"},
    {"location": "Houston Warehouse", "region": "South"},
    {"location": "Dallas Warehouse", "region": "South"},
    {"location": "New York Warehouse", "region": "Northeast"},
    {"location": "Boston Warehouse", "region": "Northeast"},
    {"location": "Atlanta Warehouse", "region": "Southeast"},
    {"location": "Miami Warehouse", "region": "Southeast"},
]

# Regions
REGIONS = ["West", "Midwest", "South", "Northeast", "Southeast"]

# Customer segments
CUSTOMER_SEGMENTS = ["individual", "fleet", "dealer"]

# Segment distribution (weights for random selection)
SEGMENT_WEIGHTS = [0.70, 0.20, 0.10]  # 70% individual, 20% fleet, 10% dealer

# Seasonal factors for sales (by month)
SEASONAL_FACTORS = {
    1: 0.85,   # January - slow
    2: 0.88,   # February
    3: 0.95,   # March - picking up
    4: 1.05,   # April
    5: 1.10,   # May - strong
    6: 1.15,   # June - peak
    7: 1.12,   # July
    8: 1.08,   # August
    9: 0.98,   # September
    10: 1.02,  # October
    11: 1.05,  # November
    12: 1.20,  # December - year-end push
}

# Regional preferences (some regions prefer certain categories)
REGIONAL_PREFERENCES = {
    "West": {"suv": 0.40, "sedan": 0.35, "truck": 0.15, "sports": 0.05, "offroad": 0.03, "compact": 0.02},
    "Midwest": {"truck": 0.40, "suv": 0.35, "sedan": 0.20, "sports": 0.03, "offroad": 0.02, "compact": 0.00},
    "South": {"truck": 0.45, "suv": 0.30, "sedan": 0.20, "sports": 0.03, "offroad": 0.02, "compact": 0.00},
    "Northeast": {"sedan": 0.45, "suv": 0.35, "compact": 0.10, "truck": 0.05, "sports": 0.03, "offroad": 0.02},
    "Southeast": {"suv": 0.35, "truck": 0.30, "sedan": 0.25, "sports": 0.05, "offroad": 0.03, "compact": 0.02},
}


def get_category_for_model(model: str) -> str:
    """Determine category for a given model."""
    for category, models in CATEGORY_MAPPING.items():
        if model in models:
            return category
    return "sedan"  # default


def get_msrp_range(category: str) -> tuple:
    """Get MSRP range for a category."""
    return MSRP_RANGES.get(category, (25000, 50000))

