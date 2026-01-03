from typing import Optional
from application.interfaces import OrderRepository, PaymentGateway
from domain.order import Order
from domain.money import Money


class PayOrderResult:
    def __init__(self, success: bool, message: str = ""):
        self.success = success
        self.message = message


class PayOrderUseCase:
    def __init__(self, order_repository: OrderRepository, payment_gateway: PaymentGateway):
        self._order_repository = order_repository
        self._payment_gateway = payment_gateway

    def execute(self, order_id: str) -> PayOrderResult:
        order = self._order_repository.get_by_id(order_id)
        if not order:
            return PayOrderResult(False, "Order not found")

        try:
            order.pay()
        except ValueError as e:
            return PayOrderResult(False, str(e))

        total = order.get_total()
        payment_success = self._payment_gateway.charge(order_id, total)

        if not payment_success:
            order.reset_status()
            return PayOrderResult(False, "Payment failed")

        self._order_repository.save(order)
        return PayOrderResult(True, "Order paid successfully")

