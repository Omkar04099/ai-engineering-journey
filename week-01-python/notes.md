# Python Fundamentals — Days 1, 2 & 3

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

For dictionaries, `in` checks keys by default, not values.

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

- For a filtering function, returning `[]` when there are no matches is appropriate.
- For a total calculation, returning `0` is appropriate.
- For an average calculation, define what should happen when there are no records.

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

The `.copy()` method creates a shallow copy of each dictionary. It is sufficient for the current flat expense records, but nested mutable objects may still be shared.

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

This makes functions reusable, predictable, and easier to test.

### 3. Shallow Copy vs. Deep Copy

#### Assignment

Assignment does not create a copy of an existing list or dictionary.

```python
original = {"category": "food", "amount": 100}

backup = original
backup["amount"] = 500

print(original["amount"])  # 500
```

Both variables refer to the same dictionary.

#### Shallow copy

A shallow copy creates a new outer container, but nested objects may still be shared.

```python
original = {
    "category": "food",
    "items": ["rice", "dal"]
}

copied = original.copy()

copied["category"] = "travel"
copied["items"].append("vegetables")

print(original)
```

The original category remains `"food"`, but its `items` list also contains `"vegetables"` because the nested list is shared.

Use shallow copy when:
- You need a new outer list or dictionary.
- Top-level modifications should not affect the original container.
- Sharing nested objects is acceptable.
- The data is flat and contains no nested mutable objects that need independent modification.

#### Deep copy

A deep copy recursively copies nested objects.

```python
import copy

original = {
    "category": "food",
    "items": ["rice", "dal"]
}

copied = copy.deepcopy(original)

copied["category"] = "travel"
copied["items"].append("vegetables")

print(original)
# {"category": "food", "items": ["rice", "dal"]}

print(copied)
# {"category": "travel", "items": ["rice", "dal", "vegetables"]}
```

Use `copy.deepcopy()` when nested mutable objects must also be independent.

Deep copying generally requires more time and memory than shallow copying. It is not necessary for every situation.

#### Important distinction: Mutating vs. replacing a nested object

Consider:

```python
original = {
    "name": "Laptop",
    "specs": {
        "ram": 16,
        "storage": 512
    }
}

shallow = original.copy()
```

Mutating a shared nested dictionary:

```python
shallow["specs"]["ram"] = 32
```

This also changes `original["specs"]["ram"]` because both dictionaries reference the same nested dictionary.

Replacing the nested dictionary:

```python
shallow["specs"] = {"ram": 64}
```

This does not change `original["specs"]`. The assignment replaces the value associated with the `"specs"` key in `shallow`, not in `original`.

**Decision rule:** Use shallow copy when outer-level independence is enough. Use deep copy when nested mutable objects also need to be independent.

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

Do not check whether the total is greater than zero: valid observations can have a total of zero.

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

## Day 3: Dictionaries for Data Processing

### 1. Counting Occurrences

Use a dictionary to track how often each item appears.

```python
def count_fruits(fruits):
    fruit_count = {}

    for fruit in fruits:
        if fruit in fruit_count:
            fruit_count[fruit] += 1
        else:
            fruit_count[fruit] = 1

    return fruit_count
```

Example:

```python
fruits = ["apple", "banana", "apple", "orange", "banana", "apple"]

print(count_fruits(fruits))
# {"apple": 3, "banana": 2, "orange": 1}
```

Key takeaways:

- Use each item as a dictionary key.
- Initialize its count to `1` when it first appears.
- Increment the count for subsequent occurrences.
- An empty input returns `{}` because the loop never executes.

### 2. Grouping Records

Use a dictionary whose values are lists to group records by a shared property.

```python
def group_expenses_by_category(expenses):
    grouped_expenses = {}

    for expense in expenses:
        category = expense["category"]

        if category in grouped_expenses:
            grouped_expenses[category].append(expense.copy())
        else:
            grouped_expenses[category] = [expense.copy()]

    return grouped_expenses
```

Example input:

```python
expenses = [
    {"category": "food", "amount": 100},
    {"category": "travel", "amount": 50},
    {"category": "food", "amount": 200}
]
```

Expected structure:

```python
{
    "food": [
        {"category": "food", "amount": 100},
        {"category": "food", "amount": 200}
    ],
    "travel": [
        {"category": "travel", "amount": 50}
    ]
}
```

Key takeaways:

- First occurrence: initialize a list containing the record.
- Subsequent occurrences: append the record to the existing list.
- Use `.copy()` consistently when independent top-level dictionaries are required.
- Since the current records are flat, shallow copying is sufficient for top-level independence.
- If nested mutable objects need independent modification, consider `copy.deepcopy()`.

### 3. Aggregation

Use a dictionary to maintain running totals, counts, or other statistics.

```python
def summarize_expenses_by_category(expenses):
    summary = {}

    for expense in expenses:
        category = expense["category"]

        if category in summary:
            summary[category]["total"] += expense["amount"]
            summary[category]["count"] += 1
        else:
            summary[category] = {
                "total": expense["amount"],
                "count": 1
            }

    return summary
```

Example input:

```python
expenses = [
    {"category": "food", "amount": 100},
    {"category": "travel", "amount": 50},
    {"category": "food", "amount": 200},
    {"category": "travel", "amount": 70},
    {"category": "shopping", "amount": 300}
]
```

Expected output:

```python
{
    "food": {"total": 300, "count": 2},
    "travel": {"total": 120, "count": 2},
    "shopping": {"total": 300, "count": 1}
}
```

Important distinction:

- `total` is the sum of the amounts.
- `count` is the number of records, not the number of distinct amounts.
- A record with an amount of `0` still contributes to the count.

### 4. Initialize-or-Update Pattern

Many dictionary-processing functions follow the same pattern:

1. Iterate over the input.
2. Extract a key.
3. Check whether the key exists.
4. Initialize the corresponding value if the key is new.
5. Update the existing value otherwise.

This pattern works for counting, grouping, and aggregation.

### 5. Aggregating Product Quantities

The same approach works with data other than expenses.

```python
def summarize_orders(orders):
    summary = {}

    for order in orders:
        product = order["product"]

        if product in summary:
            summary[product] += order["quantity"]
        else:
            summary[product] = order["quantity"]

    return summary
```

Example:

```python
orders = [
    {"product": "laptop", "quantity": 2},
    {"product": "mouse", "quantity": 3},
    {"product": "laptop", "quantity": 2},
    {"product": "mouse", "quantity": 3},
    {"product": "keyboard", "quantity": 1}
]

print(summarize_orders(orders))
# {"laptop": 4, "mouse": 6, "keyboard": 1}
```

The dictionary key identifies the product, and its value accumulates the total quantity.

### 6. Empty Collections

An empty list causes a `for` loop to execute zero times.

An appropriately initialized accumulator can therefore produce the correct empty result without an explicit condition.

Examples:

```python
count_fruits([])
# {}

group_expenses_by_category([])
# {}

summarize_expenses_by_category([])
# {}
```

The correct result depends on the function's purpose and its initialized data structure.

### 7. Shallow Copy and Deep Copy: Practical Lessons

For a flat dictionary:

```python
original = {"category": "food", "amount": 100}
copied = original.copy()

copied["amount"] = 500

print(original["amount"])  # 100
```

The original remains unchanged because the top-level value was replaced in the copied dictionary.

For a nested dictionary:

```python
original = {
    "name": "Laptop",
    "specs": {"ram": 16, "storage": 512}
}

shallow = original.copy()
shallow["specs"]["ram"] = 32

print(original["specs"]["ram"])  # 32
```

The nested dictionary is shared, so its mutation affects both structures.

To make nested mutable objects independent:

```python
import copy

deep = copy.deepcopy(original)
```

Remember:

- Assignment creates another reference to the same object.
- Shallow copy creates a new outer container.
- Deep copy recursively copies nested objects.
- Mutating a shared nested object differs from replacing the nested object in one dictionary.

### 8. Time Complexity

A single loop with average O(1) dictionary operations typically gives O(n) average time complexity, where `n` is the number of input records.

Examples:

- Counting occurrences: O(n) average time.
- Grouping records: O(n) average time, excluding the cost of copying records.
- Aggregating totals and counts: O(n) average time.

---

## Mistakes and Lessons Learned

1. Use descriptive variable names such as `expense` rather than `i` when iterating over records.
2. `len()` returns a count; it is not limited to checking whether a list is empty.
3. An empty list and `None` have different meanings.
4. Preserve the structure of records when filtering.
5. Prefer functions that depend on their arguments rather than global variables.
6. Initialize accumulators correctly before processing data.
7. Check the count before calculating an average to prevent division by zero.
8. A shallow copy does not independently copy nested mutable objects.
9. Assignment, mutation, and replacement are different operations.
10. Use deep copy only when independent nested objects are required.
11. Verify arithmetic and test edge cases, including empty inputs and zero-valued amounts.
12. A single-pass aggregation can calculate multiple statistics without traversing the input repeatedly.

---

## Progress

- [x] Day 1: Expense Analyzer — lists, dictionaries, loops, and functions
- [x] Day 2: Filtering, category totals, summaries, and introductory copying
- [x] Day 3: Counting, grouping, aggregation, empty inputs, shallow copy, and deep copy
- [ ] Day 4: Automated testing with `assert` and introductory `unittest`

## Next Session: Day 4 — Automated Testing

Planned topics:

1. Why automated tests matter.
2. Writing basic tests with `assert`.
3. Testing existing Expense Analyzer functions.
4. Testing normal cases, empty inputs, and edge cases.
5. Introducing `unittest` after the fundamentals are clear.

**Learning principle:** Attempt the tests independently before reviewing solutions. Focus on understanding expected behavior and catching bugs rather than merely making the tests pass.