import json
import os
from Product import Product
from Inventory import Inventory


def load_inventory(filename="inventory.json"):
    """Load products from JSON into an Inventory. Returns an empty Inventory if no file."""
    inventory = Inventory()
    if not os.path.exists(filename):
        return inventory
    try:
        with open(filename, "r") as file:
            for item in json.load(file):
                inventory.add_product(Product.from_dict(item))
    except (json.JSONDecodeError, KeyError, ValueError) as error:
        print(f"Could not read {filename} ({error}). Starting with an empty inventory.")
    return inventory


def save_inventory(inventory, filename="inventory.json"):
    with open(filename, "w") as file:
        json.dump([p.to_dict() for p in inventory.get_products()], file, indent=4)