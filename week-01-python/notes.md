# Python Fundamentals --- Days 1--4

A concise reference for the concepts practiced in the Expense Analyzer
project.

## Day 1: Core Python

### Lists, dictionaries, and loops

-   A **list** stores multiple items; a **dictionary** stores key-value
    pairs.
-   A list of dictionaries is useful for representing records:

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

-   Functions organize reusable logic and should work with their
    arguments rather than hidden global data.
-   `return None`, `return []`, and `return 0` have different meanings.
-   Choose empty-input behavior based on the function: filtering often
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
-   A dictionary can track category totals, counts, and other
    statistics.
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
confidence, but only for the behaviors actually tested.

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

Example:

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

Run the test file:

``` bash
python -m unittest test_expense_analyzer.py
```

### Test normal behavior and edge cases

For the Expense Analyzer, tests cover: - Multiple expenses and a single
expense. - Empty lists and zero amounts. - Empty average results
(`None`, by the project's current design). - The highest expense and an
empty input. - Ties for the highest amount.

**Key lesson:** A test can pass for one input and still miss a bug.
Include cases that exercise different paths through the function. When
code changes, rerun the tests to check for regressions.

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

## Progress

-   [x] Day 1: Lists, dictionaries, loops, and functions
-   [x] Day 2: Filtering, aggregation, and copying
-   [x] Day 3: Counting, grouping, and data processing
-   [x] Day 4: Automated testing with `assert` and `unittest`
-   [ ] Day 5: Error handling and defensive programming

## Next Session: Day 5

1.  Understand exceptions such as `ZeroDivisionError`.
2.  Learn how `try` and `except` handle exceptions.
3.  Practice handling invalid or unexpected inputs.
4.  Add defensive behavior to small Python functions.

**Learning principle:** Attempt each exercise first, then review the
solution and test your understanding.
