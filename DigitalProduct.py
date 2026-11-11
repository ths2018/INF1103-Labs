from Product import Product
from Supplier import Supplier

class DigitalProduct(Product):
    """Represents a digital product with download size"""
 
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size = float(download_size)
 
    @property
    def download_size(self) -> float:
        return self.__download_size

    def display_information(self):
        print(super().get_display_text() + f" | Download Size: {self.__download_size:.2f} MB" + f" | {self.get_fulfilment_info()}")

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
    def from_dict(data: dict[str, str | int | float], supplier: Supplier) -> "DigitalProduct":
        return DigitalProduct(data["product_id"], data["name"], data["price"],
                              data["stock"], supplier, data["download_size"])