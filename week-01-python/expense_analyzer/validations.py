def calculate_total_safe(expenses):
  if not isinstance(expenses, list):
    return "Invalid expenses"
  total = 0
  for expense in expenses:
    if not isinstance(expense, dict):
      continue
    elif "amount" not in expense:
      continue
    elif type(expense["amount"]) is not int:
      continue
    elif expense["amount"] < 0:
      continue
    else:
      total += expense["amount"]
  return total