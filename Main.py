from Product import Product
from Inventory import Inventory
from File_handling import load_inventory, save_inventory

FILENAME = "inventory.json"


def print_menu():
    print("\n=== Inventory Management System ===")
    print("1. Display all products")
    print("2. Add a product")
    print("3. Update stock")
    print("4. Search for a product")
    print("5. Save inventory")
    print("6. Exit")


def read_number(prompt, number_type):
    try:
        return number_type(input(prompt))
    except ValueError:
        return None


def add_product_option(inventory):
    product_id = input("Product ID: ").strip()
    name = input("Name: ").strip()
    price = read_number("Price: ", float)
    stock = read_number("Stock: ", int)
    if not product_id or not name or price is None or price < 0 or stock is None:
        print("Invalid input. Product not added.")
        return
    try:
        product = Product(product_id, name, price, stock)
    except ValueError as error:
        print(error)
        return
    if inventory.add_product(product):
        print("Product added.")
    else:
        print("A product with that ID already exists.")


def update_stock_option(inventory):
    product = inventory.find_by_id(input("Product ID to update: ").strip())
    if product is None:
        print("Product not found.")
        return
    quantity = read_number("New stock quantity: ", int)
    try:
        product.update_stock(quantity)
        print("Stock updated.")
    except ValueError as error:
        print(error)


def search_option(inventory):
    results = inventory.search_product(input("Search by ID or name: ").strip())
    if not results:
        print("No matching products.")
    for product in results:
        product.display_information()


def main():
    inventory = load_inventory(FILENAME)

    while True:
        print_menu()
        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_option(inventory)
        elif choice == "3":
            update_stock_option(inventory)
        elif choice == "4":
            search_option(inventory)
        elif choice == "5":
            save_inventory(inventory, FILENAME)
            print("Inventory saved.")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please enter 1-6.")


if __name__ == "__main__":
    main()