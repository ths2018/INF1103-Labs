from Product import Product

class DigitalProduct(Product):
    """Represents a digital product with download size"""
 
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = float(download_size)
 
    @property
    def download_size(self):
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
    def from_dict(data):
        return DigitalProduct(data["product_id"], data["name"], data["price"],
                              data["stock"], data["download_size"])