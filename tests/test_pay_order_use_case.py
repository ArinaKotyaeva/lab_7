import unittest
from domain.order import Order
from domain.order_line import OrderLine
from domain.money import Money
from domain.order_status import OrderStatus
from application.pay_order_use_case import PayOrderUseCase
from infrastructure.order_repository import InMemoryOrderRepository
from infrastructure.payment_gateway import FakePaymentGateway


class TestPayOrderUseCase(unittest.TestCase):
    def setUp(self):
        self.repository = InMemoryOrderRepository()
        self.payment_gateway = FakePaymentGateway()
        self.use_case = PayOrderUseCase(self.repository, self.payment_gateway)

    def test_successful_payment(self):
        order = Order("order-1")
        order.add_line(OrderLine("product-1", 2, Money(100)))
        order.add_line(OrderLine("product-2", 1, Money(50)))
        self.repository.save(order)

        result = self.use_case.execute("order-1")

        self.assertTrue(result.success)
        self.assertEqual(order.status, OrderStatus.PAID)
        self.assertEqual(len(self.payment_gateway.get_charges()), 1)
        charge = self.payment_gateway.get_charges()[0]
        self.assertEqual(charge[0], "order-1")
        self.assertEqual(charge[1], Money(250))

    def test_payment_empty_order_error(self):
        order = Order("order-2")
        self.repository.save(order)

        result = self.use_case.execute("order-2")

        self.assertFalse(result.success)
        self.assertIn("empty", result.message.lower())
        self.assertEqual(order.status, OrderStatus.PENDING)

    def test_double_payment_error(self):
        order = Order("order-3")
        order.add_line(OrderLine("product-1", 1, Money(100)))
        self.repository.save(order)

        result1 = self.use_case.execute("order-3")
        self.assertTrue(result1.success)

        result2 = self.use_case.execute("order-3")

        self.assertFalse(result2.success)
        self.assertIn("already paid", result2.message.lower())

    def test_cannot_modify_after_payment(self):
        order = Order("order-4")
        order.add_line(OrderLine("product-1", 1, Money(100)))
        self.repository.save(order)

        result = self.use_case.execute("order-4")
        self.assertTrue(result.success)

        with self.assertRaises(ValueError) as context:
            order.add_line(OrderLine("product-2", 1, Money(50)))

        self.assertIn("modify", str(context.exception).lower())

        with self.assertRaises(ValueError) as context:
            order.remove_line("product-1")

        self.assertIn("modify", str(context.exception).lower())

    def test_total_calculation(self):
        order = Order("order-5")
        order.add_line(OrderLine("product-1", 2, Money(100)))
        order.add_line(OrderLine("product-2", 3, Money(50)))
        order.add_line(OrderLine("product-3", 1, Money(25)))

        total = order.get_total()
        expected = Money(375)

        self.assertEqual(total, expected)

    def test_order_not_found(self):
        result = self.use_case.execute("non-existent")

        self.assertFalse(result.success)
        self.assertIn("not found", result.message.lower())

    def test_payment_gateway_failure(self):
        failing_gateway = FakePaymentGateway(should_fail=True)
        use_case = PayOrderUseCase(self.repository, failing_gateway)

        order = Order("order-6")
        order.add_line(OrderLine("product-1", 1, Money(100)))
        self.repository.save(order)

        result = use_case.execute("order-6")

        self.assertFalse(result.success)
        self.assertIn("failed", result.message.lower())
        self.assertEqual(order.status, OrderStatus.PENDING)


if __name__ == "__main__":
    unittest.main()

