def filter_by_category(expenses,category):
  if not expenses:
    return []
  filtered_expenses = []
  for expense in expenses:
    if expense["category"] == category:
      filtered_expenses.append(expense.copy())
  return filtered_expenses


def filter_expenses(expenses, minimum):
  output = []
  for expense in expenses:
    if expense["amount"] >= minimum:
      output.append(expense)
  return output

def group_expenses_by_category(expenses):
  grouped_expenses = {}
  for expense in expenses:
    if expense["category"] in grouped_expenses:
      grouped_expenses[expense["category"]].append(expense.copy())
    else:
      grouped_expenses[expense["category"]] = [expense.copy()]
  return grouped_expenses