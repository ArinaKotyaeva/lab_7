from typing import List
from domain.order_status import OrderStatus
from domain.order_line import OrderLine
from domain.money import Money


class Order:
    def __init__(self, order_id: str, lines: List[OrderLine] = None):
        self._id = order_id
        self._lines: List[OrderLine] = lines if lines else []
        self._status = OrderStatus.PENDING

    @property
    def id(self) -> str:
        return self._id

    @property
    def status(self) -> OrderStatus:
        return self._status

    @property
    def lines(self) -> List[OrderLine]:
        return self._lines.copy()

    def add_line(self, line: OrderLine):
        if self._status == OrderStatus.PAID:
            raise ValueError("Cannot modify paid order")
        self._lines.append(line)

    def remove_line(self, product_id: str):
        if self._status == OrderStatus.PAID:
            raise ValueError("Cannot modify paid order")
        self._lines = [line for line in self._lines if line.product_id != product_id]

    def get_total(self) -> Money:
        if not self._lines:
            return Money(0)
        total = self._lines[0].get_total()
        for line in self._lines[1:]:
            total = total + line.get_total()
        return total

    def pay(self):
        if self._status == OrderStatus.PAID:
            raise ValueError("Order is already paid")
        if not self._lines:
            raise ValueError("Cannot pay empty order")
        self._status = OrderStatus.PAID

    def reset_status(self):
        self._status = OrderStatus.PENDING

    def is_empty(self) -> bool:
        return len(self._lines) == 0

