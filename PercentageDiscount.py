from DiscountStrategy import DiscountStrategy


class PercentageDiscount(DiscountStrategy):
    """Takes a percentage off the total, e.g. PercentageDiscount(10) takes 10% off."""

    def __init__(self, percentage: float) -> None:
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage: float = percentage

    @property
    def percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)