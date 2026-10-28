from expense_analyzer import calculate_total,average_expense,highest_expense,calculate_total_safe
import unittest

class TestExpenseAnalyzer(unittest.TestCase):
    def test_calculate_total(self):
        expenses = [
            {"category": "food", "amount": 100},
            {"category": "travel", "amount": 50},
            {"category": "shopping", "amount": 200}
        ]
        result = calculate_total(expenses)
        self.assertEqual(result,350)

    def test_calculate_total_empty_list(self):
        expenses = []
        result = calculate_total(expenses)
        self.assertEqual(result,0)


    def test_calculate_total_zero_amount(self):
        expenses = [ 
         {"category": "food", "amount": 100},
         {"category": "travel", "amount": 0},
        ]
        result = calculate_total(expenses)
        self.assertEqual(result,100)


    def test_calculate_total_single_expense(self):
        expenses = [{"category": "food", "amount": 75},]
        result = calculate_total(expenses)
        self.assertEqual(result,75)

    def test_average_expense_empty_list(self):
        expenses = []
        result = average_expense(expenses)
        self.assertIsNone(result)

    def test_average_expense_normal_list(self):
        expenses = [
              {"category": "food", "amount": 100},
              {"category": "travel", "amount": 200},
        ]
        result = average_expense(expenses)
        self.assertEqual(result,150)

    def test_highest_expense(self):
        expenses = [
            {"category": "food", "amount": 100},
            {"category": "travel", "amount": 250},
            {"category": "shopping", "amount": 200},
            ]
        result = highest_expense(expenses)
        self.assertEqual(result,  {"category": "travel", "amount": 250})
    
    def test_highest_expense_empty_list(self):
        expenses = []
        result = highest_expense(expenses)
        self.assertIsNone(result)

    def test_highest_expense_tie(self):
        expenses = [
            {"category": "food", "amount": 100},
            {"category": "travel", "amount": 250},
            {"category": "shopping", "amount": 250},
        ]
        result = highest_expense(expenses)
        self.assertEqual(result,  {"category": "travel", "amount": 250})
    
    def test_calculate_total_safe(self):
        expenses = [
        {"category": "food", "amount": 100},
        {"category": "travel", "amount": 150},
        {"category": "utilities", "amount": 200},
        ]
        total = calculate_total_safe(expenses)
        self.assertEqual(total,450)

    def test_calculate_total_safe_empty_list(self):
        expenses = []
        total = calculate_total_safe(expenses)
        self.assertEqual(total,0)

    def test_calculate_total_safe_non_dict(self):
        expenses =  [
        {"category": "food", "amount": 100},
        ["travel"],
        {"category": "utilities", "amount": 200},
        ]
        total = calculate_total_safe(expenses)
        self.assertEqual(total,300)

    def test_calculate_total_safe_without_amount(self):
        expenses =  [
        {"category": "food", "amount": 100},
        {"category": "travel"},
        {"category": "utilities", "amount": 200},
        ]
        total = calculate_total_safe(expenses)
        self.assertEqual(total,300)

    def test_calculate_total_safe_negative_amount(self):
        expenses =  [
        {"category": "food", "amount": -100},
        {"category": "travel", "amount": 150},
        {"category": "utilities", "amount": 200},
        ]
        total = calculate_total_safe(expenses)
        self.assertEqual(total,350)

    def test_calculate_total_safe_string_amount(self):
        expenses =  [
        {"category": "food", "amount": 100},
        {"category": "travel", "amount": 150},
        {"category": "utilities", "amount": "200"},
        ]
        total = calculate_total_safe(expenses)
        self.assertEqual(total,250)

    def test_calculate_total_safe_boolean_amount(self):
        expenses =  [
        {"category": "food", "amount": 100},
        {"category": "travel", "amount": 150},
        {"category": "utilities", "amount": 200},
        {"category": "shopping", "amount": True},
        ]
        total = calculate_total_safe(expenses)
        self.assertEqual(total,450)

    def test_calculate_total_safe_zero_amount(self):
        expenses =  [
        {"category": "food", "amount": 100},
        {"category": "travel", "amount": 0},
        {"category": "utilities", "amount": 200},
        ]
        total = calculate_total_safe(expenses)
        self.assertEqual(total,300)

    def test_calculate_total_safe_invalid_input(self):
        expenses = 400
        total = calculate_total_safe(expenses)
        self.assertEqual(total,"Invalid expenses")

    def test_calculate_total_safe_float_amount(self):
        expenses = [
            {"category": "food", "amount": 100},
            {"category": "travel", "amount": 50.5},
            {"category": "shopping", "amount": 200},
        ]

        total = calculate_total_safe(expenses)
        self.assertEqual(total, 300)