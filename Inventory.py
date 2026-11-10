from Product import Product

class Inventory:
    def __init__(self):
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        """Add a product. Returns False if the ID already exists."""
        if self.find_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> bool:
        """Remove the matching Product reference. Returns False if not found.
        The Product object itself is not changed or destroyed."""
        product = self.find_product(product_id)
        if product is None:
            return False
        self.__products.remove(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        """Return the exact product with this ID, or None."""
        for product in self.__products:
            if product.product_id.lower() == product_id.lower():
                return product
        return None

    def search_product(self, keyword: str) -> list[Product]:
        """Return a list of products whose ID or name contains the keyword."""
        keyword = keyword.lower()
        return [p for p in self.__products
                if keyword in p.product_id.lower() or keyword in p.name.lower()]

    def display_all(self) -> list[Product]:
        if not self.__products:
            print("Inventory is empty.")
            return []
        for product in self.__products:
            product.display_information()
        return self.__products

    def get_products(self) -> list[Product]:
        """Return a copy of the list so outside code can't alter the internal list."""
        return list(self.__products)