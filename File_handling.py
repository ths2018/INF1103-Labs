import json
import os
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from Supplier import Supplier
from Inventory import Inventory

PRODUCT_TYPES = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}

def product_from_dict(item, suppliers):
    """Build the right Product subclass from a saved dictionary.

    suppliers is a {supplier_id: Supplier} dictionary used to link each product.
    """
    product_type = item.get("type")
    if product_type is None:
        # Older files saved before "type" existed: infer it from the fields
        if "weight" in item:
            product_type = "physical"
        elif "download_size" in item:
            product_type = "digital"
    if product_type not in PRODUCT_TYPES:
        raise ValueError(f"Unknown product type: {product_type}")

    supplier_id = item.get("supplier_id")
    if supplier_id not in suppliers:
        raise ValueError(f"Unknown supplier ID: {supplier_id}")

    return PRODUCT_TYPES[product_type].from_dict(item, suppliers[supplier_id])

def load_inventory(filename="inventory.json"):
    """Load suppliers and products from JSON into an Inventory. Returns an empty Inventory if no file."""
    inventory = Inventory()
    if not os.path.exists(filename):
        return inventory
    try:
        with open(filename, "r") as file:
            data = json.load(file)

        suppliers = {}
        for item in data["suppliers"]:
            supplier = Supplier.from_dict(item)
            suppliers[supplier.supplier_id] = supplier

        for item in data["products"]:
            try:
                inventory.add_product(product_from_dict(item, suppliers))
            except (KeyError, ValueError, TypeError) as error:
                print(f"Skipped product {item.get('product_id', '?')}: {error}")
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"Could not read {filename} ({error}). Starting with an empty inventory.")
        return Inventory()
    return inventory


def save_inventory(inventory, filename="inventory.json"):
    products = inventory.get_products()

    # Collect each distinct supplier once, even if many products share it
    suppliers = {}
    for p in products:
        suppliers[p.supplier.supplier_id] = p.supplier

    data = {
        "suppliers": [s.to_dict() for s in suppliers.values()],
        "products": [p.to_dict() for p in products],
    }
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)