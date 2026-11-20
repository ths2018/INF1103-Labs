from Product import Product
from OrderLine import OrderLine
from DiscountStrategy import DiscountStrategy
from NoDiscount import NoDiscount


class Order:
    """Creates and owns its OrderLine objects (composition)."""

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def order_lines(self) -> list[OrderLine]:
        """Return a copy so outside code can't add or remove lines directly."""
        return list(self.__order_lines)

    @property
    def discount(self) -> DiscountStrategy:
        return self.__discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    def calculate_total(self) -> float:
        subtotal = sum((line.calculate_subtotal() for line in self.__order_lines), 0.0)
        return self.__discount.apply(subtotal)

    def add_order_line(self, product: Product, quantity: int) -> None:
        """The Order creates the OrderLine itself; callers never pass one in."""
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Remove the line for this product. Returns False if there isn't one."""
        for line in self.__order_lines:
            if line.product.product_id.lower() == product_id.lower():
                self.__order_lines.remove(line)
                return True
        return False

    def display_information(self) -> None:
        print(f"Order {self.__order_id}")
        if not self.__order_lines:
            print("  (no order lines)")
        for line in self.__order_lines:
            print("  ", end="")
            line.display_information()
        print(f"  Total: ${self.calculate_total():.2f}")