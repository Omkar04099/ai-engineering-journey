from expense_analyzer import (
    calculate_total,
    highest_expense,
    calculate_total_safe,
)
from persistent_expense_analyzer import (add_expense,save_expenses,load_expenses)

def main():
    expenses = [
        {"category": "food", "amount": 150},
        {"category": "travel", "amount": 80},
        {"category": "food", "amount": 120},
        {"category": "shopping", "amount": 500},
        {"category": "travel", "amount": 50},
        {"category": "food", "amount": 200},
    ]

    expenses_unsafe = [
        {"category": "food", "amount": 150},
        {"category": "travel", "amount": -80},
        {"category": "food", "amount": 120},
        {"category": "shopping", "amount": "500"},
        {"category": "travel"},
        ["category"],
        {"category": "utilities", "amount": 300},
    ]

    orders = [
        {"product": "laptop", "quantity": 1},
        {"product": "mouse", "quantity": 2},
        {"product": "laptop", "quantity": 3},
        {"product": "keyboard", "quantity": 1},
        {"product": "mouse", "quantity": 4}
    ]

    fruits = ["apple", "banana", "apple", "orange", "banana", "apple"]

    
    # total = calculate_total(expenses)
    # highest_exp = highest_expense(expenses)
    # safe_total = calculate_total_safe(expenses_unsafe)
    existing_expenses = load_expenses()
    new_expenses = add_expense(existing_expenses, {"category": "utilities", "amount": 120})
    save_expenses(new_expenses)
    latest_expenses = load_expenses()
    print(latest_expenses)
    print("Total number of expenses: ",len(latest_expenses))
    # print("Total expenses:", total)
    # print("Highest expense:", highest_exp)
    # print("Safe total:", safe_total)



if __name__ == "__main__":
    main()
