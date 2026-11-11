from Product import Product

class OrderLine:
    """One product and the quantity ordered. Created and managed by an Order."""

    def __init__(self, product: Product, quantity: int):
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a whole number greater than 0.")
        self.__product: Product = product    # reference only: the OrderLine does not own it
        self.__quantity: int = quantity

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.price * self.__quantity

    def display_information(self) -> None:
        print(f"{self.__product.name:<15} | Qty: {self.__quantity:>3} | "
              f"Unit: ${self.__product.price:>9.2f} | "
              f"Subtotal: ${self.calculate_subtotal():>9.2f}")