from Product import Product
from CanBeShipped import CanBeShipped

class PhysicalProduct(Product, CanBeShipped):
    """Represents a physical product with weight"""
 
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = float(weight)
 
    @property
    def weight(self):
        return self.__weight
 
    def display_information(self):
        print(super().get_display_text() + f" | Weight: {self.__weight:.2f} kg" + f" | {self.get_fulfilment_info()}" + f" | Shipping cost: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        """Flat $5.00 handling fee plus $1.00 per kg."""
        return 5.00 + 1.00 * self.__weight
 
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