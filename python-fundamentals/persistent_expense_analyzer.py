import json
import math

def is_valid_expense(expense):
    if not isinstance(expense,dict):
        return False
    if "amount" not in expense:
        return False
    if "category" not in expense:
        return False
    if type(expense["amount"]) is bool:
        return False
    if not (isinstance(expense["amount"],int) or isinstance(expense["amount"],float)):
        return False
    if not math.isfinite(expense["amount"]):
        return False
    if expense["amount"] < 0:
        return False
    
    return True
   


def add_expense(expenses,new_expense):
    expenses.append(new_expense)
    return expenses

def save_expenses(expenses):
    with open("expenses.json","w") as file:
        json.dump(expenses,file,indent=4)

def load_expenses(file_name="expenses.json"):
    try:
        with open(file_name,"r") as file:
            expenses = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    else:
        if not isinstance(expenses,list):
            return []
        if not all(is_valid_expense(expense) for expense in expenses):
            return []
        return expenses