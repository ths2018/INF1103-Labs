from Product import Product
from CanBeShipped import CanBeShipped
from Supplier import Supplier

class PhysicalProduct(Product, CanBeShipped):
    """Represents a physical product with weight"""
 
    def __init__(self, product_id: str, name: str, price: float, stock: int,  supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight:float = float(weight)
 
    @property
    def weight(self) -> float:
        return self.__weight
 
    def display_information(self) -> None:
        print(super().get_display_text() + f" | Weight: {self.__weight:.2f} kg" + f" | {self.get_fulfilment_info()}" + f" | Shipping cost: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        """Flat $5.00 handling fee plus $1.00 per kg."""
        return 5.00 + 1.00 * self.__weight
 
    def to_dict(self) -> dict[str, str | int | float]:
        data = super().to_dict()
        data.update({
            "type": "physical",
            "weight": self.__weight,
        })
        return data
 
    @staticmethod
    def from_dict(data: dict[str, str | int | float], supplier: Supplier) -> "PhysicalProduct":
        return PhysicalProduct(data["product_id"], data["name"], data["price"],
                               data["stock"], supplier, data["weight"])