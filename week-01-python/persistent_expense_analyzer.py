import json

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
        return expenses