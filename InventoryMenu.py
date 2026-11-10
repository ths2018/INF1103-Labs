from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from CanBeShipped import CanBeShipped
from File_handling import save_inventory
from Supplier import Supplier

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

    def _find_supplier(self, supplier_id):
        """Return an existing Supplier with this ID from the inventory, or None."""
        for product in self._inventory.get_products():
            if product.supplier.supplier_id == supplier_id:
                return product.supplier
        return None

    def _read_supplier(self):
        """Ask for a supplier ID. Reuse an existing Supplier, or create a new one.
        Returns a Supplier, or None if input was invalid."""
        supplier_id = input("Supplier ID: ").strip()
        if not supplier_id:
            print("Supplier ID cannot be empty.")
            return None

        existing = self._find_supplier(supplier_id)
        if existing is not None:
            print(f"Using existing supplier: {existing.name}")
            return existing

        print("New supplier. Please enter their details.")
        name = input("Supplier name: ").strip()
        email = input("Supplier contact email: ").strip()
        if not name or "@" not in email:
            print("Invalid supplier details.")
            return None
        return Supplier(supplier_id, name, email)

    def _read_product(self):
        """Ask for product details. Returns a Product, or None if input was invalid."""
        product_type = input("Is this a physical product or digital? (physical/digital): ").strip().lower()
        if product_type not in ("physical", "digital"):
            print("Invalid product type. Please enter 'physical' or 'digital'.")
            return None

        product_id = input("Product ID: ").strip()
        name = input("Name: ").strip()
        price = self.read_number("Price: ", float)
        stock = self.read_number("Stock: ", int)
        if product_type == "physical":
            extra = self.read_number("Weight (kg): ", float)
        else:
            extra = self.read_number("Download Size (MB): ", float)

        if (not product_id or not name or price is None or price < 0
                or stock is None or extra is None or extra < 0):
            print("Invalid input. Product not added.")
            return None

        supplier = self._read_supplier()
        if supplier is None:
            print("Product not added.")
            return None

        try:
            if product_type == "physical":
                return PhysicalProduct(product_id, name, price, stock, supplier, extra)
            return DigitalProduct(product_id, name, price, stock, supplier, extra)
        except ValueError as error:
            print(error)
            return None

    def add_product_option(self):
        product = self._read_product()
        if product is None:
            return
        if self._inventory.add_product(product):
            print("Product added.")
            print(product.get_fulfilment_info())
            if isinstance(product, CanBeShipped):
                print(f"Shipping cost: ${product.calculate_shipping_cost():.2f}")
        else:
            print("A product with that ID already exists.")

    def update_stock_option(self):
        product = self._inventory.find_product(input("Product ID to update: ").strip())
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
            product.display_supplier_information()

    def save_option(self):
        save_inventory(self._inventory, self._filename)
        print("Inventory saved.")