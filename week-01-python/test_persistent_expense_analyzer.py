import unittest
from persistent_expense_analyzer import load_expenses

class TestPersistentExpenseAnalyzer(unittest.TestCase):
    def test_load_expenses_normal(self):
        expected_output = [
            {
                "category": "food",
                "amount": 150
            },
            {
                "category": "travel",
                "amount": 80
            }
        ]
        obtained_output = load_expenses("temp_expenses.json")
        self.assertEqual(obtained_output,expected_output)
    
    def test_load_expenses_missing_file(self):
        expected_output = []
        obtained_output = load_expenses("file_not_there.json")
        self.assertEqual(obtained_output,expected_output)

    def test_load_expenses_malformed_data(self):
        expected_output = []
        obtained_output = load_expenses("malformed_data.json")
        self.assertEqual(obtained_output,expected_output)