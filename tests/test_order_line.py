import unittest
from domain.order_line import OrderLine
from domain.money import Money


class TestOrderLine(unittest.TestCase):
    def test_order_line_creation(self):
        line = OrderLine("product-1", 2, Money(100))
        self.assertEqual(line.product_id, "product-1")
        self.assertEqual(line.quantity, 2)
        self.assertEqual(line.price, Money(100))

    def test_zero_quantity_error(self):
        with self.assertRaises(ValueError):
            OrderLine("product-1", 0, Money(100))

    def test_negative_quantity_error(self):
        with self.assertRaises(ValueError):
            OrderLine("product-1", -1, Money(100))

    def test_zero_price_error(self):
        with self.assertRaises(ValueError):
            OrderLine("product-1", 1, Money(0))

    def test_get_total(self):
        line = OrderLine("product-1", 3, Money(100))
        total = line.get_total()
        self.assertEqual(total, Money(300))


if __name__ == "__main__":
    unittest.main()

