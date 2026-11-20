from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        """Return the total after this discount has been applied."""
        ...