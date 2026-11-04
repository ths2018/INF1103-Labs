from Inventory import Inventory
from InventoryMenu import InventoryMenu
from File_handling import load_inventory

FILENAME = "inventory.json"


def print_menu():
    print("\n=== Inventory Management System ===")
    print("1. Display all products")
    print("2. Add a product")
    print("3. Update stock")
    print("4. Search for a product")
    print("5. Save inventory")
    print("6. Exit")


def main():
    inventory = load_inventory(FILENAME)
    menu = InventoryMenu(inventory, FILENAME)

    while True:
        print_menu()
        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            menu.add_product_option()
        elif choice == "3":
            menu.update_stock_option()
        elif choice == "4":
            menu.search_option()
        elif choice == "5":
            menu.save_option()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please enter 1-6.")


if __name__ == "__main__":
    main()