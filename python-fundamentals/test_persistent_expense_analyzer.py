import unittest
from persistent_expense_analyzer import load_expenses, is_valid_expense
import tempfile
import os
import json

class TestPersistentExpenseAnalyzer(unittest.TestCase):
    
    def test_load_expenses_missing_file(self):
        expected_output = []
        obtained_output = load_expenses("file_not_there.json")
        self.assertEqual(obtained_output,expected_output)


    def test_load_expenses_normal_temp_file(self):
        valid_data = [
            {
                "category": "food",
                "amount": 150
            },
            {
                "category": "travel",
                "amount": 80
            }
        ]
        with tempfile.NamedTemporaryFile(mode="w",delete=False) as file:
            json.dump(valid_data,file,indent=4)
            temp_file_path = file.name
        try:
            temp_file_content = load_expenses(temp_file_path)
            self.assertEqual(valid_data,temp_file_content)
        finally:
            os.remove(temp_file_path)

    def test_load_expenses_malformed_temp_file(self):
        with tempfile.NamedTemporaryFile(mode="w",delete=False) as file:
            file.write("invalid json")
            temp_file_path = file.name
        try:
            output = load_expenses(temp_file_path)
            self.assertEqual(output,[])
        finally:
            os.remove(temp_file_path)

    def test_load_expenses_root_dictionary(self):
        valid_dict = {
            "category": "food",
            "amount": 150
        }
        with tempfile.NamedTemporaryFile(mode="w",delete=False) as file:
            json.dump(valid_dict,file,indent=4)
            temp_file_path = file.name
        try:
            output = load_expenses(temp_file_path)
            self.assertEqual(output,[])
        finally:
            os.remove(temp_file_path)

    def test_is_valid_expense_int(self):
        expense = {"category": "food", "amount": 150}
        output = is_valid_expense(expense)
        self.assertTrue(output)

    def test_is_valid_expense_float(self):
        expense = {"category": "food", "amount": 150.5}
        output = is_valid_expense(expense)
        self.assertTrue(output)

    def test_is_valid_expense_bool(self):
        expense = {"category": "food", "amount": True}
        output = is_valid_expense(expense)
        self.assertFalse(output)
    
    def test_is_valid_expense_string(self):
        expense = {"category": "food", "amount": "150"}
        output = is_valid_expense(expense)
        self.assertFalse(output)

    def test_is_valid_expense_category_absent(self):
        expense = {"amount": 150}
        output = is_valid_expense(expense)
        self.assertFalse(output)

    def test_is_valid_expense_amount_absent(self):
        expense = {"category": "food"}
        output = is_valid_expense(expense)
        self.assertFalse(output)

    def test_is_valid_expense_negative_amount(self):
        expense = {"category": "food", "amount": -10}
        output = is_valid_expense(expense)
        self.assertFalse(output)
    
    def test_is_valid_expense_type_and_key_mismatch(self):
        expense = ["food", 150]
        output = is_valid_expense(expense)
        self.assertFalse(output)
    
    def test_is_valid_expense_nan(self):
        expense = {"category": "food", "amount": float("nan")}
        output = is_valid_expense(expense)
        self.assertFalse(output)

    def test_is_valid_expense_positive_infinity(self):
        expense = {"category": "food", "amount": float("inf")}
        output = is_valid_expense(expense)
        self.assertFalse(output)

    def test_is_valid_expense_negative_infinity(self):
        expense = {"category": "food", "amount": float("-inf")}
        output = is_valid_expense(expense)
        self.assertFalse(output)

    def test_load_expenses_valid_file(self):
        valid_data = [
            {
                "category": "food",
                "amount": 150
            },
            {
                "category": "travel",
                "amount": 80
            },
            {
                "category": "shopping",
                "amount": 280
            }
        ]
        with tempfile.NamedTemporaryFile(mode="w",delete=False) as file:
            temp_file_path = file.name
            json.dump(valid_data,file,indent=4)
        try:
            output = load_expenses(temp_file_path)
            self.assertEqual(valid_data,output)
        finally:
            os.remove(temp_file_path)

    def test_load_expenses_one_invalid(self):
        one_invalid = [
            {
                "category": "food",
                "amount": 150
            },
            {
                "category": "travel",
                "amount": 80
            },
            {
                "category": "shopping",
                "amount": -280
            }
        ]
        with tempfile.NamedTemporaryFile(mode="w",delete=False) as file:
            temp_file_path = file.name
            json.dump(one_invalid,file,indent=4)
        try:
            output = load_expenses(temp_file_path)
            self.assertEqual(output,[])
        finally:
            os.remove(temp_file_path)
        
    def test_load_expenses_invalid_item(self):
        invalid_item_type = [
            {
                "category": "food",
                "amount": 150
            },
            {
                "category": "travel",
                "amount": 80
            },
            {
                "category": "shopping",
                "amount": "280"
            }
        ]
        with tempfile.NamedTemporaryFile(mode="w",delete=False) as file:
            temp_file_path = file.name
            json.dump(invalid_item_type,file,indent=4)
        try:
            output = load_expenses(temp_file_path)
            self.assertEqual(output,[])
        finally:
            os.remove(temp_file_path)
            
    def test_load_expenses_non_dict_item(self):
        invalid_item_list = [
            {
                "category": "food",
                "amount": 150
            },
            {
                "category": "travel",
                "amount": 80
            },
            "invalid data",
            {
                "category": "shopping",
                "amount": 280
            }
        ]
        with tempfile.NamedTemporaryFile(mode="w",delete=False) as file:
            temp_file_path = file.name
            json.dump(invalid_item_list,file,indent=4)
        try:
            output = load_expenses(temp_file_path)
            self.assertEqual(output,[])
        finally:
            os.remove(temp_file_path)