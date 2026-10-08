import json
import os

FILENAME = "inventory.json"

DEFAULT_INVENTORY = {
    "P001": {"name": "Laptop", "price": 1200.00, "stock": 15},
    "P002": {"name": "Mouse", "price": 25.50, "stock": 40},
    "P003": {"name": "Keyboard", "price": 45.00, "stock": 25},
}

# ---------- Menu ----------
def print_header():
    print("=" * 44)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 44)
 
 
def print_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("-" * 28)

def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 47)
    for pid, item in inventory.items():
        print(f"ID: {pid} | Name: {item['name']} | "
              f"Price: ${item['price']:.2f} | Stock: {item['stock']}")
    print("-" * 47)
 
 
def add_product(inventory):
    print("\nAdd New Product")
    pid = input("Product ID: ").strip().upper()
    if pid in inventory:
        print("Product ID already exists.")
        return
    name = input("Product Name: ").strip()
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))
    inventory[pid] = {"name": name, "price": price, "stock": stock}
    print("\nProduct added successfully!")
 
 
def update_stock(inventory):
    print("\nUpdate Stock")
    pid = input("Enter Product ID: ").strip().upper()
    if pid not in inventory:
        print("\nProduct not found.")
        return
    item = inventory[pid]
    print("\nProduct Found:")
    print(f"Name: {item['name']}")
    print(f"Current Stock: {item['stock']}")
    item["stock"] = int(input("\nNew Stock Quantity: "))
    print("\nStock updated successfully!")
 
 
def search_product(inventory):
    print("\nSearch Product")
    pid = input("Enter Product ID: ").strip().upper()
    if pid not in inventory:
        print("\nProduct not found.")
        return
    item = inventory[pid]
    print("\nProduct Found")
    print("-" * 47)
    print(f"ID: {pid}")
    print(f"Name: {item['name']}")
    print(f"Price: ${item['price']:.2f}")
    print(f"Stock: {item['stock']}")
    print("-" * 47)

def load_inventory(filename=FILENAME):
    """Load inventory from JSON. Creates default data if the file is missing."""
    if os.path.exists(filename):
        print(f"{filename} found.")
        try:
            with open(filename, "r") as f:
                inventory = json.load(f)
            print("Inventory loaded successfully.")
            return inventory
        except (json.JSONDecodeError, OSError):
            print("Error reading file. Starting with default inventory.")
    else:
        print(f"{filename} not found. Creating default inventory.")
    save_inventory(DEFAULT_INVENTORY, filename)
    return dict(DEFAULT_INVENTORY)
 
 
def save_inventory(inventory, filename=FILENAME):
    """Write inventory dictionary to JSON. Returns True on success."""
    try:
        with open(filename, "w") as f:
            json.dump(inventory, f, indent=4)
        return True
    except OSError:
        print("Error: could not save inventory.")
        return False