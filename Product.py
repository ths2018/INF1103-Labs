from abc import ABC, abstractmethod

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        """Calculate the shipping cost for this product."""
        pass

class Product(ABC):
 
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
 
    def get_display_text(self):
        return (f"ID: {self.__product_id:<6} | Name: {self.__name:<15} | "
                f"Price: ${self.__price:>9.2f} | Stock: {self.__stock}")

    @abstractmethod
    def display_information(self):
        print(self.get_display_text())

    def get_fulfilment_info(self):
        """Return a string describing how this product is fulfilled."""
        pass
 
    def to_dict(self):
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }
 
    @staticmethod
    @abstractmethod
    def from_dict(data):
        pass  # This method should be implemented in subclasses to create an instance from a dictionary

class PhysicalProduct(Product):
    """Represents a physical product with weight"""
 
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = float(weight)
 
    @property
    def weight(self):
        return self.__weight
 
    def display_information(self):
        print(super().get_display_text() + f" | Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."
 
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "type": "physical",
            "weight": self.__weight,
        })
        return data
 
    @staticmethod
    def from_dict(data):
        return PhysicalProduct(data["product_id"], data["name"], data["price"],
                               data["stock"], data["weight"])

class DigitalProduct(Product):
    """Represents a digital product with download size"""
 
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = float(download_size)
 
    @property
    def download_size(self):
        return self.__download_size

    def display_information(self):
        print(super().get_display_text() + f" | Download Size: {self.__download_size:.2f} MB")

    def get_fulfilment_info(self):
        return "This product is delivered digitally."
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "type": "digital",
            "download_size": self.__download_size,
        })
        return data
 
    @staticmethod
    def from_dict(data):
        return DigitalProduct(data["product_id"], data["name"], data["price"],
                              data["stock"], data["download_size"])