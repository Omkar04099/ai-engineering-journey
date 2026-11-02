import unittest

def validate_expense(expense):
    if "amount" not in expense:
        raise ValueError("Expense must contain an amount")

    if expense["amount"] < 0:
        raise ValueError("Expense amount cannot be negative")

    return True

class TestExpense(unittest.TestCase):
    def test_missing_amount(self):
        with self.assertRaises(ValueError):
            validate_expense({"category":"food"})
    
    def test_negative_amount(self):
        with self.assertRaises(ValueError):
            validate_expense({"category":"food","amount":-50})

    def test_negative_amount_message(self):
        with self.assertRaisesRegex(ValueError,r"cannot be negative"):
            validate_expense({"category":"food","amount":-50})