from DiscountStrategy import DiscountStrategy


class BulkDiscount(DiscountStrategy):
    """Takes `amount` off any total of `threshold` or more, e.g. BulkDiscount(200, 20)."""

    def __init__(self, threshold: float, amount: float) -> None:
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and amount cannot be negative.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    @property
    def threshold(self) -> float:
        return self.__threshold

    @property
    def amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return max(0.0, total - self.__amount)   # never go below zero
        return total