from domain.money import Money
from application.interfaces import PaymentGateway


class FakePaymentGateway(PaymentGateway):
    def __init__(self, should_fail: bool = False):
        self._should_fail = should_fail
        self._charges = []

    def charge(self, order_id: str, money: Money) -> bool:
        self._charges.append((order_id, money))
        return not self._should_fail

    def get_charges(self):
        return self._charges.copy()

