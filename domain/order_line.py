from dataclasses import dataclass
from domain.money import Money


@dataclass
class OrderLine:
    product_id: str
    quantity: int
    price: Money

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.price.amount <= 0:
            raise ValueError("Price must be positive")

    def get_total(self) -> Money:
        return Money(self.price.amount * self.quantity, self.price.currency)

