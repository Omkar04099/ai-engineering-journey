def calculate_total(expenses):
  total_expense = 0
  for expense in expenses:
    total_expense += expense["amount"]
  return total_expense


def average_expense(expenses):
    if not expenses:
        return None
    total = 0
    for expense in expenses:
        total += expense["amount"]
    average = total / len(expenses)
    return average


def highest_expense(expenses):
    if not expenses:
        return None
    highest = expenses[0]
    for expense in expenses:
        if expense["amount"] > highest["amount"]:
            highest = expense
    return highest

def calculate_category_total(expenses, category):
  if not expenses:
    return 0
  total = 0
  for expense in expenses:
    if expense["category"] == category:
      total += expense["amount"]
  return total
        
def total_by_category(expenses):
  total_by_cat = {}
  for expense in expenses:
    if expense["category"] in total_by_cat:
      total_by_cat[expense["category"]] += expense["amount"] 
    else:
      total_by_cat[expense["category"]] = expense["amount"]
  return total_by_cat


def summarize_orders(orders):
  summary = {}
  for order in orders:
    if order["product"] in summary:
      summary[order["product"]] += order["quantity"]
    else:
      summary[order["product"]] = order["quantity"]
  return summary

def summarize_expenses_by_category(expenses):
  summary = {}
  for expense in expenses:
    if expense["category"] in summary:
      summary[expense["category"]]["total"] += expense["amount"]
      summary[expense["category"]]["count"] += 1
    else:
      summary[expense["category"]] = {"total":expense["amount"], "count":1}
  return summary

def summarize_category(expenses, category):
  result = {"category":category, "count":0, "total":0, "average":0}
  for expense in expenses:
    if expense["category"] == category:
      result["count"] += 1
      result["total"] += expense["amount"]
      result["average"] = result["total"] / result["count"]
  return result

def count_fruits(fruits):
  fruit_count = {}
  for fruit in fruits:
    if fruit in fruit_count:
      fruit_count[fruit] += 1
    else:
      fruit_count[fruit] = 1
  return fruit_count

def calculate_total_from_strings(expenses):
  total = 0
  for expense in expenses:
    try:
      amount = int(expense["amount"])
    except KeyError:
      print(f"Amount key not available in:{expense}")
    except ValueError:
      print(f"Invalid amount for category:{expense.get('category','Unknown')}")
    else:
      total += amount
  return total
