import unittest
from fin import BalanceManager

class TestBalanceManager(unittest.TestCase):

    def test_get_balance_invalid_input(self):
        manager = BalanceManager()
        with self.assertRaises(Exception):
            manager.get_balance('invalid_file.txt')

    def test_add_invalid_input(self):
        manager = BalanceManager()
        with self.assertRaises(Exception):
            manager.write_post({"дата": "2022-01-01", "категория": "доход", "сумма": "1000"})

    def test_show_balance_correct_sum(self):
        manager = BalanceManager()
        balance = [
            {"дата": "2022-01-01", "категория": "доход", "сумма": 1000, "описание": "Зарплата"},
            {"дата": "2022-01-05", "категория": "расход", "сумма": 500, "описание": "Покупки"}
        ]
        manager.balance = balance
        result = manager.show_balance()
        self.assertEqual(result['Общая сумма'], 500)  # Проверяем, что общая сумма расходов равна 500

if __name__ == '__main__':
    unittest.main()