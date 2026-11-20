from Product import Product
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from Supplier import Supplier


class ProductFactory:
    """Decides which Product subclass to build. It creates products but does not store them."""

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock: int, supplier: Supplier, extra: float = 0.0) -> Product:
        """extra = weight in kg for a physical product, download size in MB for a digital one."""
        product_type = product_type.strip().lower()
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock, supplier, extra)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock, supplier, extra)
        else:
            raise ValueError(f"Unknown product type: '{product_type}'. "
                             "Expected 'physical' or 'digital'.")