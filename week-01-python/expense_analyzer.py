

expenses = [
    {"category": "food", "amount": 150},
    {"category": "travel", "amount": 80},
    {"category": "food", "amount": 120},
    {"category": "shopping", "amount": 500},
    {"category": "travel", "amount": 50},
    {"category": "food", "amount": 200},
    {"category": "utilities", "amount": 300},
]

# Day 1

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

# Day 2

def filter_by_category(expenses,category):
  if not expenses:
    return []
  filtered_expenses = []
  for expense in expenses:
    if expense["category"] == category:
      filtered_expenses.append(expense.copy())
  return filtered_expenses

def calculate_category_total(expenses, category):
  if not expenses:
    return 0
  total = 0
  for expense in expenses:
    if expense["category"] == category:
      total += expense["amount"]
  return total

def summarize_category(expenses, category):
  result = {"category":category, "count":0, "total":0, "average":0}
  for expense in expenses:
    if expense["category"] == category:
      result["count"] += 1
      result["total"] += expense["amount"]
      result["average"] = result["total"] / result["count"]
  return result

total = calculate_total(expenses)
category_wise_total = total_by_category(expenses)
minimum_expenses = filter_expenses(expenses,100)
average_amount = average_expense(expenses)
highest_exp = highest_expense(expenses)
filtered_exp = filter_by_category(expenses,"food")
category_total = calculate_category_total(expenses, "food")
summary = summarize_category(expenses, "food")
print(total)
print(category_wise_total)
print(minimum_expenses)
print(average_amount)
print(highest_exp)
print("summary :",summary)
print("category total :",category_total)
print("filtered expenses :",filtered_exp)