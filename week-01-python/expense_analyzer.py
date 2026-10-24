

expenses = [
    {"category": "food", "amount": 150},
    {"category": "travel", "amount": 80},
    {"category": "food", "amount": 120},
    {"category": "shopping", "amount": 500},
    {"category": "travel", "amount": 50},
    {"category": "food", "amount": 200},
    {"category": "utilities", "amount": 300},
]

def calculate_total(expenses):
  total_expense = 0
  for expense in expenses:
    total_expense += expense["amount"]
  return total_expense

def total_by_category(expenses):
  total_by_cat = {}
  for expense in expenses:
    if expense["category"] in total_by_cat:
      total_by_cat[expense["category"]] += expense["amount"] 
    else:
      total_by_cat[expense["category"]] = expense["amount"]
  return total_by_cat

def filter_expenses(expenses, minimum):
  output = []
  for expense in expenses:
    if expense["amount"] >= minimum:
      output.append(expense)
  return output

def average_expense(expenses):
  if not expenses:
    return None
  sum = 0;
  for expense in expenses:
    sum += expense["amount"]
  average = sum/len(expenses)
  return average

def highest_expense(expenses):
  if not expenses:
    return None
  highest = expenses[0]
  for expense in expenses:
    if expense["amount"] > highest["amount"]:
      highest = expense
  return highest

total = calculate_total(expenses)
category_wise_total = total_by_category(expenses)
minimum_expenses = filter_expenses(expenses,100)
average_amount = average_expense(expenses)
highest_exp = highest_expense(expenses)
print(total)
print(category_wise_total)
print(minimum_expenses)
print(average_amount)
print(highest_exp)