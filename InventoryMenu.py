from Product import DigitalProduct, PhysicalProduct, Product
from File_handling import save_inventory


class InventoryMenu:

    def __init__(self, inventory, filename):
        self._inventory = inventory
        self._filename = filename

    @staticmethod
    def read_number(prompt, number_type):
        """Return the input converted to number_type, or None if it isn't valid."""
        try:
            return number_type(input(prompt))
        except ValueError:
            return None

    def _read_product(self):
        """Ask for product details. Returns a Product, or None if input was invalid."""
        productselection = input("Is this a physical product or digital? (physical/digital): ").strip().lower()
        if productselection == "physical":
            product_id = input("Product ID: ").strip()
            name = input("Name: ").strip()
            price = self.read_number("Price: ", float)
            stock = self.read_number("Stock: ", int)
            weight = self.read_number("Weight (kg): ", float) if productselection == "physical" else 0

            if (not product_id or not name or price is None or price < 0
                    or stock is None or weight is None or weight < 0):
                print("Invalid input. Product not added.")
                return None

            try:
                if productselection == "physical":
                    return PhysicalProduct(product_id, name, price, stock, weight)
                return Product(product_id, name, price, stock)
            except ValueError as error:
                print(error)
                return None
        elif productselection == "digital":
            product_id = input("Product ID: ").strip()
            name = input("Name: ").strip()
            price = self.read_number("Price: ", float)
            stock = self.read_number("Stock: ", int)
            download_size = self.read_number("Download Size (MB): ", float)

            if (not product_id or not name or price is None or price < 0
                    or stock is None or download_size is None or download_size < 0):
                print("Invalid input. Product not added.")
                return None

            try:
                return DigitalProduct(product_id, name, price, stock, download_size)
            except ValueError as error:
                print(error)
                return None
        else:
            print("Invalid product type. Please enter 'physical' or 'digital'.")
            return None

    def add_product_option(self):
        product = self._read_product()
        if product is None:
            return
        if self._inventory.add_product(product):
            print("Product added.")
        else:
            print("A product with that ID already exists.")

    def update_stock_option(self):
        product = self._inventory.find_by_id(input("Product ID to update: ").strip())
        if product is None:
            print("Product not found.")
            return
        quantity = self.read_number("New stock quantity: ", int)
        if quantity is None:
            print("Invalid quantity.")
            return
        try:
            product.update_stock(quantity)
            print("Stock updated.")
        except ValueError as error:
            print(error)

    def search_option(self):
        results = self._inventory.search_product(input("Search by ID or name: ").strip())
        if not results:
            print("No matching products.")
        for product in results:
            product.display_information()

    def save_option(self):
        save_inventory(self._inventory, self._filename)
        print("Inventory saved.")