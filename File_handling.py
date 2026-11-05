import json
import os
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from Inventory import Inventory

PRODUCT_TYPES = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}

def product_from_dict(item):
    """Build the right Product subclass from a saved dictionary."""
    product_type = item.get("type")
    if product_type is None:
        # Older files saved before "type" existed: infer it from the fields
        if "weight" in item:
            product_type = "physical"
        elif "download_size" in item:
            product_type = "digital"
    if product_type not in PRODUCT_TYPES:
        raise ValueError(f"Unknown product type: {product_type}")
    return PRODUCT_TYPES[product_type].from_dict(item)

def load_inventory(filename="inventory.json"):
    """Load products from JSON into an Inventory. Returns an empty Inventory if no file."""
    inventory = Inventory()
    if not os.path.exists(filename):
        return inventory
    try:
        with open(filename, "r") as file:
            for item in json.load(file):
                inventory.add_product(product_from_dict(item))
    except (json.JSONDecodeError, KeyError, ValueError) as error:
        print(f"Could not read {filename} ({error}). Starting with an empty inventory.")
    return inventory


def save_inventory(inventory, filename="inventory.json"):
    with open(filename, "w") as file:
        json.dump([p.to_dict() for p in inventory.get_products()], file, indent=4)