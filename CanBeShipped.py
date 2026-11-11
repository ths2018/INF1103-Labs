from abc import ABC, abstractmethod

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Calculate the shipping cost for this product."""
        ...