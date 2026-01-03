import unittest
from domain.order import Order
from domain.order_line import OrderLine
from domain.money import Money
from domain.order_status import OrderStatus


class TestOrderDomain(unittest.TestCase):
    def test_order_creation(self):
        order = Order("order-1")
        self.assertEqual(order.id, "order-1")
        self.assertEqual(order.status, OrderStatus.PENDING)
        self.assertTrue(order.is_empty())

    def test_add_line(self):
        order = Order("order-2")
        line = OrderLine("product-1", 2, Money(100))
        order.add_line(line)
        self.assertEqual(len(order.lines), 1)
        self.assertFalse(order.is_empty())

    def test_remove_line(self):
        order = Order("order-3")
        order.add_line(OrderLine("product-1", 1, Money(100)))
        order.add_line(OrderLine("product-2", 1, Money(50)))
        order.remove_line("product-1")
        self.assertEqual(len(order.lines), 1)
        self.assertEqual(order.lines[0].product_id, "product-2")

    def test_cannot_modify_after_payment(self):
        order = Order("order-4")
        order.add_line(OrderLine("product-1", 1, Money(100)))
        order.pay()

        with self.assertRaises(ValueError):
            order.add_line(OrderLine("product-2", 1, Money(50)))

        with self.assertRaises(ValueError):
            order.remove_line("product-1")

    def test_cannot_pay_empty_order(self):
        order = Order("order-5")
        with self.assertRaises(ValueError) as context:
            order.pay()
        self.assertIn("empty", str(context.exception).lower())

    def test_cannot_pay_twice(self):
        order = Order("order-6")
        order.add_line(OrderLine("product-1", 1, Money(100)))
        order.pay()
        with self.assertRaises(ValueError) as context:
            order.pay()
        self.assertIn("already paid", str(context.exception).lower())

    def test_total_calculation(self):
        order = Order("order-7")
        order.add_line(OrderLine("product-1", 2, Money(100)))
        order.add_line(OrderLine("product-2", 1, Money(50)))
        total = order.get_total()
        self.assertEqual(total, Money(250))

    def test_empty_order_total(self):
        order = Order("order-8")
        total = order.get_total()
        self.assertEqual(total, Money(0))


if __name__ == "__main__":
    unittest.main()

