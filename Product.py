from abc import ABC, abstractmethod

from Supplier import Supplier

class Product(ABC):
 
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier) -> None:
        self.__product_id:str = product_id
        self.__name:str = name
        self.__price:float = float(price)
        self.__stock:int = 0
        self.__supplier: Supplier = supplier
        self.update_stock(stock)  # reuse validation instead of assigning directly
 
    # ---- read-only access (no setters, so values can't be changed from outside) ----
    @property
    def product_id(self) -> str:
        return self.__product_id
 
    @property
    def name(self) -> str:
        return self.__name
 
    @property
    def price(self) -> float:
        return self.__price
 
    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    def display_supplier_information(self) -> None:
        """Show the supplier's details through this product."""
        self.__supplier.display_information()
 
    # ---- behaviour ----
    def update_stock(self, quantity: int) -> None:
        """Set the stock level. The Product decides what is a valid value."""
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Stock must be a whole number that is 0 or more.")
        self.__stock = quantity
 
    def get_display_text(self) -> str:
        return (f"ID: {self.__product_id:<6} | Name: {self.__name:<15} | "
                f"Price: ${self.__price:>9.2f} | Stock: {self.__stock}")

    @abstractmethod
    def display_information(self) -> None:
        print(self.get_display_text())

    def get_fulfilment_info(self) -> str:
        """Return a string describing how this product is fulfilled."""
        pass
 
    def to_dict(self) -> dict[str, str | int | float]:
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier_id": self.__supplier.supplier_id,
        }
 
    @staticmethod
    @abstractmethod
    def from_dict(data: dict[str, str | int | float], supplier: Supplier) -> "Product":
        pass  # This method should be implemented in subclasses to create an instance from a dictionary