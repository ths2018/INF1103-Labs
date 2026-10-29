class Product:
    """Represents and manages a single product (SRP: one product, its data and its state)."""
 
    def __init__(self, product_id, name, price, stock):
        # "Private" by convention (name mangling): outside code should use the methods/properties.
        self.__product_id = product_id
        self.__name = name
        self.__price = float(price)
        self.__stock = 0
        self.update_stock(stock)  # reuse validation instead of assigning directly
 
    # ---- read-only access (no setters, so values can't be changed from outside) ----
    @property
    def product_id(self):
        return self.__product_id
 
    @property
    def name(self):
        return self.__name
 
    @property
    def price(self):
        return self.__price
 
    @property
    def stock(self):
        return self.__stock
 
    # ---- behaviour ----
    def update_stock(self, quantity):
        """Set the stock level. The Product decides what is a valid value."""
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Stock must be a whole number that is 0 or more.")
        self.__stock = quantity
 
    def display_information(self):
        print(f"ID: {self.__product_id:<6} | Name: {self.__name:<15} | "
              f"Price: ${self.__price:>9.2f} | Stock: {self.__stock}")
 
    # ---- helpers so the file-handling code doesn't need to touch private attributes ----
    def to_dict(self):
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }
 
    @staticmethod
    def from_dict(data):
        return Product(data["product_id"], data["name"], data["price"], data["stock"])