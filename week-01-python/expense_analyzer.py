



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
  sum = 0
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


# Day 3

def count_fruits(fruits):
  fruit_count = {}
  for fruit in fruits:
    if fruit in fruit_count:
      fruit_count[fruit] += 1
    else:
      fruit_count[fruit] = 1
  return fruit_count

def group_expenses_by_category(expenses):
  grouped_expenses = {}
  for expense in expenses:
    if expense["category"] in grouped_expenses:
      grouped_expenses[expense["category"]].append(expense.copy())
    else:
      grouped_expenses[expense["category"]] = [expense.copy()]
  return grouped_expenses

def summarize_expenses_by_category(expenses):
  summary = {}
  for expense in expenses:
    if expense["category"] in summary:
      summary[expense["category"]]["total"] += expense["amount"]
      summary[expense["category"]]["count"] += 1
    else:
      summary[expense["category"]] = {"total":expense["amount"], "count":1}
  return summary

def summarize_orders(orders):
  summary = {}
  for order in orders:
    if order["product"] in summary:
      summary[order["product"]] += order["quantity"]
    else:
      summary[order["product"]] = order["quantity"]
  return summary
 



if __name__ == "__main__":
  expenses = [
      {"category": "food", "amount": 150},
      {"category": "travel", "amount": 80},
      {"category": "food", "amount": 120},
      {"category": "shopping", "amount": 500},
      {"category": "travel", "amount": 50},
      {"category": "food", "amount": 200},
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

  # 1
  total = calculate_total(expenses)
  category_wise_total = total_by_category(expenses)
  minimum_expenses = filter_expenses(expenses,100)
  average_amount = average_expense(expenses)
  highest_exp = highest_expense(expenses)

  # 2
  filtered_exp = filter_by_category(expenses,"food")
  category_total = calculate_category_total(expenses, "food")
  summary = summarize_category(expenses, "food")

  # 3
  fruit_wise_count = count_fruits(fruits)
  grouped_expenses = group_expenses_by_category(expenses)
  summarized_expenses = summarize_expenses_by_category(expenses)
  summarized_orders = summarize_orders(orders)


  print(total)
  print(category_wise_total)
  print(minimum_expenses)
  print(average_amount)
  print(highest_exp)
  print("summary :",summary)
  print("category total :",category_total)
  print("filtered expenses :",filtered_exp)

  print(fruit_wise_count)
  print(grouped_expenses)
  print(summarized_expenses)
  print(summarized_orders)