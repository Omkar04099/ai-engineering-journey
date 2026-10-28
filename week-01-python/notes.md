# Python Fundamentals --- Days 1--5

A concise reference for concepts practiced in the Expense Analyzer
project.

## Day 1: Core Python

### Lists, dictionaries, and loops

-   A **list** stores multiple items; a **dictionary** stores key-value
    pairs.
-   A list of dictionaries represents records:

``` python
expenses = [
    {"category": "food", "amount": 150},
    {"category": "travel", "amount": 80},
]
for expense in expenses:
    print(expense["amount"])
```

-   For dictionaries, `in` checks keys by default.
-   `len(items)` counts items, `sum(numbers)` adds values, and
    `items.append(value)` adds an item to a list.

### Functions and return values

-   Functions organize reusable logic and should use arguments rather
    than hidden global data.
-   `return None`, `return []`, and `return 0` have different meanings.
-   Empty-input behavior depends on the function: filtering often
    returns `[]`, totals return `0`, and averages need an explicit
    design choice.

``` python
def calculate_total(expenses):
    total = 0
    for expense in expenses:
        total += expense["amount"]
    return total
```

## Day 2: Filtering, Aggregation, and Copies

### Filtering and summaries

-   Build a new result list when filtering; avoid accidentally modifying
    the input.
-   An accumulator keeps a running result, such as a total or count.
-   A dictionary can track category totals, counts, and statistics.
-   Check that the count is greater than zero before calculating an
    average. A total of zero can still be valid data.

### Assignment vs. shallow copy vs. deep copy

-   **Assignment** (`backup = original`): both variables refer to the
    same object.
-   **Shallow copy** (`original.copy()`): creates a new outer container,
    but nested mutable objects may still be shared.
-   **Deep copy** (`copy.deepcopy(original)`): recursively copies nested
    objects.

``` python
import copy
original = {"name": "Laptop", "specs": {"ram": 16}}
shallow = original.copy()
deep = copy.deepcopy(original)
shallow["specs"]["ram"] = 32  # also changes original["specs"]["ram"]
deep["specs"]["ram"] = 64     # does not change original
```

**Rule of thumb:** Use shallow copy when outer-level independence is
enough; use deep copy when nested mutable objects must also be
independent. Deep copy can use more time and memory.

### Time complexity

-   One pass over `n` records is generally **O(n)**.
-   A single-pass summary can calculate totals and counts together
    without repeatedly traversing the input.

## Day 3: Dictionary-Based Data Processing

### Three common patterns

1.  **Counting:** use each item as a key; initialize its count on first
    appearance, then increment it.
2.  **Grouping:** use a key such as category, with a list of matching
    records as the value.
3.  **Aggregation:** maintain running totals, counts, or quantities for
    each key.

``` python
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

-   An empty list makes a `for` loop run zero times, so initialized
    results such as `{}` can be returned naturally.
-   Keep record structure consistent when filtering or grouping.
-   A zero-valued record still contributes to the record count.
-   Assignment, mutation, and replacing a nested object are different
    operations.

## Day 4: Automated Testing

### Why tests matter

Automated tests check whether functions behave as expected and help
catch regressions after code changes. Passing tests increases
confidence, but only for behaviors actually tested.

### Basic `assert`

``` python
assert calculate_total(expenses) == 350, "Total is incorrect"
```

The message is shown if the assertion fails. Regular `assert` statements
can be disabled when Python runs in optimized mode.

### `unittest`

-   `unittest.TestCase` groups related tests.
-   Test method names should begin with `test_`.
-   `self.assertEqual(actual, expected)` checks equality.
-   `self.assertIsNone(result)` checks that a result is `None`.
-   The test runner discovers and runs tests, then reports failures.

``` python
import unittest
from expense_analyzer import calculate_total

class TestExpenseAnalyzer(unittest.TestCase):
    def test_calculate_total(self):
        expenses = [
            {"category": "food", "amount": 100},
            {"category": "travel", "amount": 250},
        ]
        self.assertEqual(calculate_total(expenses), 350)

if __name__ == "__main__":
    unittest.main()
```

Run tests with:

``` bash
python -m unittest test_expense_analyzer.py
```

Tests cover multiple and single expenses, empty lists, zero amounts,
empty average results (`None`, by the project's current design), highest
expenses, empty inputs, and ties for the highest amount.

**Key lesson:** A test can pass for one input and still miss a bug.
Include cases that exercise different paths through the function. Rerun
tests after code changes to check for regressions.

## Day 5: Error Handling and Defensive Programming

### Input validation

-   Validate assumptions about incoming data before processing it.
-   `isinstance(value, dict)` checks whether a value is a dictionary.
-   `"amount" not in expense` checks whether a dictionary key is
    missing.
-   Distinguish a missing key from a key whose value is `0`. Zero can be
    valid data.
-   Technical validation checks type and structure; business validation
    checks application-specific rules.

### `return`, `continue`, and `break`

-   `return` terminates the entire function and returns a value.
-   `continue` skips the current loop iteration and moves to the next
    item.
-   `break` terminates the loop.

For `calculate_total_safe()`, invalid individual records are skipped
with `continue`, allowing later valid records to be processed.

### Defensive total calculation

The current `calculate_total_safe()` rules are:

-   The top-level input must be a list; otherwise, return
    `"Invalid expenses"`.
-   Skip records that are not dictionaries.
-   Skip records without an `"amount"` key.
-   Skip amounts whose exact type is not `int`; this also rejects
    Boolean values such as `True`.
-   Skip negative amounts.
-   Include zero and positive integer amounts.
-   Return the total of accepted records.

``` python
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
```

### Truthiness vs. key existence

Avoid `if not expense.get("amount")` when zero is valid. That condition
treats `0` as falsy and may mistake it for a missing or invalid amount.
Use `"amount" not in expense` when checking whether the key exists.

### Testing defensive behavior

The test suite includes valid records, empty input, non-dictionary
records, missing amounts, negative amounts, string amounts, Boolean
amounts, zero amounts, and invalid top-level input.

**Important limitation:** Invalid records are silently skipped in this
exercise. Production systems may need to log or report rejected records
so data-quality problems are visible. The current function returns an
integer total or an error string for invalid top-level input; a more
mature design could use exceptions or a structured result.

## Mistakes and Lessons to Remember

-   Use descriptive variable names.
-   Initialize accumulators correctly.
-   Use function arguments instead of unrelated global variables.
-   Preserve record structure when returning filtered data.
-   Decide and test empty-input behavior explicitly.
-   Check the count before dividing to calculate an average.
-   Understand whether a copy shares nested mutable objects.
-   Test edge cases, not just the happy path.
-   Use a single pass when it keeps aggregation clear and efficient.
-   Use `continue` to skip a bad record when processing should continue.
-   Distinguish technical validation from business rules.
-   Do not confuse a valid zero value with a missing value.

## Progress

-   [x] Day 1: Lists, dictionaries, loops, and functions
-   [x] Day 2: Filtering, aggregation, and copying
-   [x] Day 3: Counting, grouping, and data processing
-   [x] Day 4: Automated testing with `assert` and `unittest`
-   [x] Day 5: Error handling and defensive programming

## Next Session: Day 6

1.  Learn Python modules and imports.
2.  Understand how to organize code across files.
3.  Separate application logic from test code cleanly.
4.  Review the Expense Analyzer project structure before moving toward
    APIs.

**Learning principle:** Attempt each exercise first, then review the
solution and test your understanding.
