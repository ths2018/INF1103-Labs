from DiscountStrategy import DiscountStrategy


class StudentDiscount(DiscountStrategy):
    """A flat 5% student discount."""

    RATE: float = 0.05

    def apply(self, total: float) -> float:
        return total * (1 - self.RATE)