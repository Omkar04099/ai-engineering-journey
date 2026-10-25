# Python Fundamentals — Days 1 & 2

## Day 1: Lists, Dictionaries, Loops, and Functions

### 1. Lists and Dictionaries

- A list stores multiple items.
- A dictionary stores key-value pairs.
- A list can contain dictionaries, making it useful for representing records.

Example:

```python
expenses = [
    {"category": "food", "amount": 150},
    {"category": "travel", "amount": 80}
]
```

Access dictionary values using their keys:

```python
expenses[0]["category"]  # "food"
expenses[0]["amount"]    # 150
```

### 2. Loops

Use a `for` loop to iterate over items in a list.

```python
for expense in expenses:
    print(expense["amount"])
```

The variable `expense` refers to the current dictionary during each iteration.

### 3. Dictionary Membership

The `in` operator checks whether a key exists in a dictionary.

```python
totals = {"food": 150, "travel": 80}

if "food" in totals:
    print("Category exists")
```

### 4. Built-in Functions and Methods

- `len(items)` returns the number of items.
- `sum(numbers)` calculates the sum of an iterable.
- `items.append(value)` adds an item to a list.
- `dictionary.copy()` creates a shallow copy of a dictionary.

### 5. Functions and Return Values

Functions help organize reusable logic.

```python
def calculate_total(expenses):
    total = 0

    for expense in expenses:
        total += expense["amount"]

    return total
```

Important distinctions:

- `return` without a value returns `None`.
- `return None` explicitly returns `None`.
- `return []` returns an empty list.
- `return 0` returns the integer zero.

These values are not interchangeable.

### 6. Preserving Data Structure Consistency

When filtering records, preserve their original structure if downstream code expects the same keys.

For example, if a record contains `category` and `amount`, avoid transforming it into a differently structured dictionary unless that is intentional.

### 7. Handling Empty Inputs

An empty list evaluates to `False` in a condition.

```python
if not expenses:
    print("No expenses available")
```

Use an appropriate return value based on the function's purpose.

For a filtering function, returning `[]` when there are no matches is appropriate.

For an average calculation, define what should happen when there are no records.

---

## Day 2: Filtering, Aggregation, and Copying

### 1. Filtering Records

Use a loop and a condition to select matching records.

```python
def filter_by_category(expenses, category):
    filtered_expenses = []

    for expense in expenses:
        if expense["category"] == category:
            filtered_expenses.append(expense.copy())

    return filtered_expenses
```

Key takeaways:

- Create a new list for filtered results.
- Do not modify the original list unintentionally.
- Return an empty list if no records match.
- Use descriptive variable names.

### 2. Functions Should Use Their Arguments

A function should operate on the data passed to it rather than silently depend on global variables.

```python
def calculate_total(expenses):
    total = 0

    for expense in expenses:
        total += expense["amount"]

    return total
```

The function should use its `expenses` parameter.

### 3. Shallow Copy vs. Deep Copy

A shallow copy creates a new outer dictionary but retains references to nested objects.

```python
original = {
    "category": "food",
    "items": ["rice", "dal"]
}

copied = original.copy()
copied["items"].append("vegetables")
```

Both dictionaries now expose the updated nested list because they share that list.

A deep copy recursively copies nested objects.

```python
import copy

original = {
    "category": "food",
    "items": ["rice", "dal"]
}

copied = copy.deepcopy(original)
copied["items"].append("vegetables")
```

The original nested list remains unchanged.

Use `copy.deepcopy()` when independent nested objects are required. Deep copying is not necessary for every situation.

### 4. Accumulators

An accumulator maintains a running result while iterating through data.

```python
def calculate_category_total(expenses, category):
    total = 0

    for expense in expenses:
        if expense["category"] == category:
            total += expense["amount"]

    return total
```

Here, `total` is the accumulator.

Initializing it to `0` allows the function to return zero naturally when no expenses match.

### 5. Counting and Aggregating Records

A summary can be calculated in one pass through the list.

```python
def summarize_category(expenses, category):
    result = {
        "category": category,
        "count": 0,
        "total": 0,
        "average": 0
    }

    for expense in expenses:
        if expense["category"] == category:
            result["count"] += 1
            result["total"] += expense["amount"]

    if result["count"] > 0:
        result["average"] = result["total"] / result["count"]

    return result
```

Benefits:

- Each expense is examined once.
- Count and total are calculated together.
- Average is calculated after the loop.
- The count check prevents division by zero.

### 6. Average and Edge Cases

Average is calculated by dividing the total by the number of observations.

Before dividing, ensure the count is greater than zero.

Do not check whether the total is greater than zero: a valid set of observations can have a total of zero.

For example, amounts `0`, `0`, and `30` produce:

- Total: `30`
- Count: `3`
- Average: `10`

If no records match, this project's summary function returns zero for the count, total, and average.

### 7. Time Complexity: One Pass vs. Multiple Passes

For a list of `n` expenses:

- One traversal takes O(n) time.
- Two traversals also take O(n) time, but perform more work.
- A single-pass summary can calculate count and total together.

Reusing existing functions can improve organization, but consider whether it causes unnecessary repeated processing.

---

## Mistakes and Lessons Learned

1. Use descriptive variable names such as `expense` rather than `i` when iterating over records.
2. `len()` returns a count; it is not limited to checking whether a list is empty.
3. An empty list and `None` have different meanings.
4. Preserve the structure of records when filtering.
5. A shallow copy does not independently copy nested mutable objects.
6. Check the count before calculating an average.
7. Trace calculations carefully and verify arithmetic.
8. Prefer functions that depend on their arguments rather than global variables.

## Progress

- [x] Day 1: Expense Analyzer
- [x] Day 2: Filtering, category totals, and category summaries
- [ ] Day 3: More list and dictionary practice, followed by introductory automated testing