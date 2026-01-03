import unittest
from domain.money import Money


class TestMoney(unittest.TestCase):
    def test_money_creation(self):
        money = Money(100)
        self.assertEqual(money.amount, 100)
        self.assertEqual(money.currency, "RUB")

    def test_money_immutability(self):
        money = Money(100)
        with self.assertRaises(Exception):
            money.amount = 200

    def test_negative_amount_error(self):
        with self.assertRaises(ValueError):
            Money(-10)

    def test_money_addition(self):
        m1 = Money(100)
        m2 = Money(50)
        result = m1 + m2
        self.assertEqual(result, Money(150))

    def test_different_currencies_error(self):
        m1 = Money(100, "RUB")
        m2 = Money(50, "USD")
        with self.assertRaises(ValueError):
            m1 + m2

    def test_money_equality(self):
        m1 = Money(100)
        m2 = Money(100)
        m3 = Money(50)
        self.assertEqual(m1, m2)
        self.assertNotEqual(m1, m3)


if __name__ == "__main__":
    unittest.main()

