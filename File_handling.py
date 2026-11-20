import json
import csv
import os
from Supplier import Supplier
from Inventory import Inventory
from Product import Product
from ProductFactory import ProductFactory


def product_from_dict(item: dict[str, str | int | float],
                      suppliers: dict[str, Supplier]) -> Product:
    """Build a Product from a saved dictionary, using the factory."""
    product_type = item.get("type")
    if product_type is None:
        # Older files saved before "type" existed: infer it from the fields
        if "weight" in item:
            product_type = "physical"
        elif "download_size" in item:
            product_type = "digital"

    supplier_id = item.get("supplier_id")
    if supplier_id not in suppliers:
        raise ValueError(f"Unknown supplier ID: {supplier_id}")

    extra = item.get("weight", item.get("download_size", 0.0))   # whichever one the item has
    return ProductFactory.create(product_type, item["product_id"], item["name"],
                                 item["price"], item["stock"], suppliers[supplier_id], extra)

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

def _parse_number(text: str, number_type: type, label: str):
    """Convert text to a number, or raise a ValueError with a simple message."""
    try:
        return number_type(text)
    except ValueError:
        raise ValueError(f"{label} '{text}' is not a valid number") from None

def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Load products from a CSV file into the inventory. A bad row is skipped, not fatal."""
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)                          # skip the header row
            loaded = 0
            for row in reader:
                if not row:                             # ignore blank lines
                    continue
                try:
                    if len(row) != 5:
                        raise ValueError(f"expected 5 columns but found {len(row)}")
                    product_type, product_id, name, price, stock = (v.strip() for v in row)
                    product = ProductFactory.create(
                        product_type, product_id, name,
                        _parse_number(price, float, "price"),
                        _parse_number(stock, int, "stock quantity"),
                        supplier)
                    if inventory.add_product(product):
                        loaded += 1
                    else:
                        print(f"Skipped line {reader.line_num}: ID {product_id} already exists.")
                except ValueError as error:
                    print(f"Skipped line {reader.line_num}: {error}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")