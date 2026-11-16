import re 

grouped = r"[0-9]{1,2}(,[0-9]{2})*,[0-9]{3}"
ungrouped = r"\d+"

indian_number_pattern = rf"(?:{ungrouped}|{grouped})"

def number_validity_printer(arr):
  for number in arr:
    print(bool(re.fullmatch(indian_number_pattern,number)))


valid = [
    "1500",
    "150000",
    "1,500",
    "15,000",
    "1,50,000",
    "10,00,000"
]

invalid = [
    "1,5,00",
    "1,,500",
    "12.50"
]

number_validity_printer(valid)
number_validity_printer(invalid)
