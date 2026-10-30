# Python Fundamentals — Days 1–7

A concise reference for concepts practiced in the Expense Analyzer project.

## Day 1: Core Python

### Lists, dictionaries, and loops

- A **list** stores multiple items; a **dictionary** stores key-value pairs.

- A list of dictionaries represents records:

```python

expenses = [

    {"category": "food", "amount": 150},

    {"category": "travel", "amount": 80},

]

for expense in expenses:

    print(expense["amount"])

```

- For dictionaries, `in` checks keys by default.

- `len(items)` counts items, `sum(numbers)` adds values, and `items.append(value)` adds an item to a list.

### Functions and return values

- Functions organize reusable logic and should use arguments rather than hidden global data.

- `return None`, `return []`, and `return 0` have different meanings.

- Empty-input behavior depends on the function: filtering often returns `[]`, totals return `0`, and averages need an explicit design choice.

```python

def calculate_total(expenses):

    total = 0

    for expense in expenses:

        total += expense["amount"]

    return total

```

## Day 2: Filtering, Aggregation, and Copies

### Filtering and summaries

- Build a new result list when filtering; avoid accidentally modifying the input.

- An accumulator keeps a running result, such as a total or count.

- A dictionary can track category totals, counts, and statistics.

- Check that the count is greater than zero before calculating an average. A total of zero can still be valid data.

### Assignment vs. shallow copy vs. deep copy

- **Assignment** (`backup = original`): both variables refer to the same object.

- **Shallow copy** (`original.copy()`): creates a new outer container, but nested mutable objects may still be shared.

- **Deep copy** (`copy.deepcopy(original)`): recursively copies nested objects.

```python

import copy

original = {"name": "Laptop", "specs": {"ram": 16}}

shallow = original.copy()

deep = copy.deepcopy(original)

shallow["specs"]["ram"] = 32  # Also changes original["specs"]["ram"]

deep["specs"]["ram"] = 64     # Does not change original

```

**Rule of thumb:** Use shallow copy when outer-level independence is enough; use deep copy when nested mutable objects must also be independent. Deep copy can use more time and memory.

### Time complexity

- One pass over `n` records is generally **O(n)**.

- A single-pass summary can calculate totals and counts together without repeatedly traversing the input.

## Day 3: Dictionary-Based Data Processing

### Three common patterns

1\\. **Counting:** Use each item as a key; initialize its count on first appearance, then increment it.

2\\. **Grouping:** Use a key such as category, with a list of matching records as the value.

3\\. **Aggregation:** Maintain running totals, counts, or quantities for each key.

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

- An empty list makes a `for` loop run zero times, so initialized results such as `{}` can be returned naturally.

- Keep record structure consistent when filtering or grouping.

- A zero-valued record still contributes to the record count.

- Assignment, mutation, and replacing a nested object are different operations.

## Day 4: Automated Testing

### Why tests matter

Automated tests check whether functions behave as expected and help catch regressions after code changes. Passing tests increases confidence, but only for behaviors actually tested.

### Basic `assert`

```python

assert calculate_total(expenses) == 350, "Total is incorrect"

```

The message is shown if the assertion fails. Regular `assert` statements can be disabled when Python runs in optimized mode.

### `unittest`

- `unittest.TestCase` groups related tests.

- Test method names should begin with `test\\\_`.

- `self.assertEqual(actual, expected)` checks equality.

- `self.assertIsNone(result)` checks that a result is `None`.

- The test runner discovers and runs tests, then reports failures.

```python

import unittest

from expense_analyzer import calculate_total

class TestExpenseAnalyzer(unittest.TestCase):

    def test_calculate_total(self):

        expenses = [

            {"category": "food", "amount": 100},

            {"category": "travel", "amount": 250},

        ]

        self.assertEqual(calculate_total(expenses), 350)

if \\\_\\\_name\\\_\\\_ == "\\\_\\\_main\\\_\\\_":

    unittest.main()

```

Run tests from the `week-01-python` directory:

```bash

python -m unittest test_expense_analyzer.py

```

Tests cover multiple and single expenses, empty lists, zero amounts, empty average results (`None`, by the project's current design), highest expenses, empty inputs, and ties for the highest amount.

**Key lesson:** A test can pass for one input and still miss a bug. Include cases that exercise different paths through the function. Rerun tests after code changes to check for regressions.

## Day 5: Input Validation and Defensive Programming

### Input validation

- Validate assumptions about incoming data before processing it.

- `isinstance(value, dict)` checks whether a value is a dictionary.

- `"amount" not in expense` checks whether a dictionary key is missing.

- Distinguish a missing key from a key whose value is `0`. Zero can be valid data.

- Technical validation checks type and structure; business validation checks application-specific rules.

### `return`, `continue`, and `break`

- `return` terminates the entire function and returns a value.

- `continue` skips the current loop iteration and moves to the next item.

- `break` terminates the loop.

For `calculate_total_safe()`, invalid individual records are skipped with `continue`, allowing later valid records to be processed.

### Defensive total calculation

The current `calculate_total_safe()` rules are:

- The top-level input must be a list; otherwise, return `"Invalid expenses"`.

- Skip records that are not dictionaries.

- Skip records without an `"amount"` key.

- Skip amounts whose exact type is not `int`; this also rejects Boolean values such as `True`.

- Skip negative amounts.

- Include zero and positive integer amounts.

- Return the total of accepted records.

```python

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

### Truthiness vs. key existence

Avoid `if not expense.get("amount")` when zero is valid. That condition treats `0` as falsy and may mistake it for a missing or invalid amount.

Use `"amount" not in expense` when checking whether the key exists.

### Testing defensive behavior

The test suite includes valid records, empty input, non-dictionary records, missing amounts, negative amounts, string amounts, Boolean amounts, zero amounts, and invalid top-level input.

**Important limitation:** Invalid records are silently skipped in this exercise. Production systems may need to log or report rejected records so data-quality problems are visible. The current function returns an integer total or an error string for invalid top-level input; a more mature design could use exceptions or a structured result.

## Day 6: Python Modules, Packages, and Project Structure

### Modules

- A **module** is a Python file that contains code, such as functions, variables, or classes.

- Modules let us separate related functionality into different files.

- Instead of keeping every function in one large file, we can organize functions by responsibility.

For the Expense Analyzer, we separated calculations, filtering, and validation into different modules.

### Packages

- A **package** organizes related modules under a common directory.

- Our `expense_analyzer/` directory is a package.

- An `\\\_\\\_init\\\_\\\_.py` file makes the package structure explicit and can expose selected functions through the package namespace.

Our project structure is:

```text

week-01-python/

├── expense_analyzer/

│   ├── \\\_\\\_init\\\_\\\_.py

│   ├── calculations.py

│   ├── filters.py

│   └── validations.py

├── main.py

├── test_expense_analyzer.py

└── notes.md

```

### Importing functions

A function can be imported directly from its module:

```python

from expense_analyzer.calculations import calculate_total

```

We can then call it without prefixing the module name:

```python

total = calculate_total(expenses)

```

The package's `\\\_\\\_init\\\_\\\_.py` can re-export selected functions:

```python

from .calculations import calculate_total

```

The leading `.` means that Python should import from a module relative to the current package.

After a function is exposed through `\\\_\\\_init\\\_\\\_.py`, it can also be imported from the package namespace:

```python

from expense_analyzer import calculate_total

```

**Key distinction:** Defining a function in a module and making it available through the package namespace are related but different things. The imports in `\\\_\\\_init\\\_\\\_.py` determine which names the package exposes.

### Organizing code by responsibility

We split the Expense Analyzer functions into three modules:

- `calculations.py`: totals, averages, highest expenses, and summary calculations.

- `filters.py`: filtering expenses and grouping records.

- `validations.py`: defensive validation and safe total calculation.

This makes the project easier to navigate, maintain, test, and extend.

### Separating reusable logic from program execution

`main.py` is the entry point for running the sample application. It imports reusable functions from the package and calls them from a `main()` function.

```python

def main():

    # Prepare sample data and call the required functions.

    pass

if \\\_\\\_name\\\_\\\_ == "\\\_\\\_main\\\_\\\_":

    main()

```

The `pass` above is a placeholder to demonstrate the structure, not a replacement for the actual implementation in our project.

- When a Python file is run directly, Python sets its `\\\_\\\_name\\\_\\\_` to `"\\\_\\\_main\\\_\\\_"`.

- When the file is imported as a module, its `\\\_\\\_name\\\_\\\_` is normally its module name.

- The `if \\\_\\\_name\\\_\\\_ == "\\\_\\\_main\\\_\\\_":` guard lets us run the entry-point logic directly without running it automatically when the file is imported.

**Key lesson:** Keep reusable functions in modules and application execution in an entry-point file.

### What happens when a module is imported?

- Python executes a module's top-level statements when the module is first imported into a running process.

- Python normally caches imported modules in `sys.modules`, so subsequent imports in the same process reuse the loaded module rather than executing it from scratch each time.

- A function's body executes when that function is called, not simply because the function was defined or imported.

This distinction helps explain why module-level code and function calls behave differently.

### Testing after refactoring

Moving functions into modules can accidentally break imports or change behavior. After reorganizing the project:

1\\. Run the existing test suite.

2\\. Confirm that imports resolve correctly.

3\\. Run `main.py` and check its output.

4\\. Verify that the original behavior is preserved.

The Expense Analyzer's existing suite still passes **19 tests** after the refactor.

Run the tests from the project directory:

```bash

python -m unittest test_expense_analyzer.py

```

Run the sample application:

```bash

python main.py

```

### Mistakes and lessons to remember

- A module is a Python file; a package organizes modules.

- Use explicit imports to make dependencies clear.

- Use relative imports, such as `from .calculations import calculate_total`, within a package when appropriate.

- `\\\_\\\_init\\\_\\\_.py` can expose selected functions at the package level.

- Keep application execution separate from reusable business logic.

- Use `if \\\_\\\_name\\\_\\\_ == "\\\_\\\_main\\\_\\\_":` to guard entry-point execution.

- Test after changing a project's structure, not just after changing function logic.

- Avoid keeping multiple obsolete files that duplicate the current implementation.

**## Day 7: Exception Handling**

**### Exception Basics**

Exceptions occur when Python encounters an error during execution.

Common exceptions:

- `TypeError`: An operation receives an incompatible type.

- `ValueError`: A value has the correct general type but is invalid for the operation.

- `KeyError`: A dictionary key does not exist.

- `ZeroDivisionError`: Division by zero is attempted.

**### try, except, else, and finally**

- `try`: Contains code that might raise an exception.

- `except`: Handles a matching exception.

- `else`: Executes when the `try` block completes without an exception.

- `finally`: Normally executes when control leaves the `try` statement, whether an exception occurs or not. It is commonly used for cleanup.

Prefer catching specific exceptions instead of using a blanket `except`.

**### Exception Handling in the Expense Analyzer**

Practised writing `calculate_total_from_strings()` to:

- Convert string amounts to integers.

- Handle invalid numeric strings using `ValueError`.

- Handle missing dictionary keys using `KeyError`.

- Skip invalid records while continuing to process subsequent records.

- Add only successfully converted amounts to the total.

- Preserve the original expense data.

**### Automated Testing**

Practised using `unittest` to verify:

- The correct total is returned when an amount is invalid.

- Missing amount keys do not prevent valid records from being processed.

- The input remains unchanged.

**### Key Lessons**

- Handle different failure conditions with appropriate exception types.

- Keep `try` blocks focused on operations that might raise the expected exception.

- Error-reporting code should not introduce additional exceptions.

- A shallow copy duplicates the outer container but may share nested mutable objects.

- A deep copy recursively copies nested objects.

- Tests should cover both normal behavior and edge cases.

## Mistakes and Lessons to Remember

- Use descriptive variable names.

- Initialize accumulators correctly.

- Use function arguments instead of unrelated global variables.

- Preserve record structure when returning filtered data.

- Decide and test empty-input behavior explicitly.

- Check the count before dividing to calculate an average.

- Understand whether a copy shares nested mutable objects.

- Test edge cases, not just the happy path.

- Use a single pass when it keeps aggregation clear and efficient.

- Use `continue` to skip a bad record when processing should continue.

- Distinguish technical validation from business rules.

- Do not confuse a valid zero value with a missing value.

- Organize related functions into modules based on responsibility.

- Keep reusable logic separate from the program's entry point.

- Rerun tests after refactoring to detect regressions.

## Progress

- [x] Day 1: Lists, dictionaries, loops, and functions

- [x] Day 2: Filtering, aggregation, and copying

- [x] Day 3: Counting, grouping, and data processing

- [x] Day 4: Automated testing with `assert` and `unittest`

- [x] Day 5: Input validation and defensive programming

- [x] Day 6: Modules, packages, imports, and project structure

- [x] Day 7: Exceptions and error handling

## Next Session: Day 8

1. Learn how to read and write files.

2. Practise file operations with small examples.

3. Introduce JSON and structured data exchange.

4. Apply the concepts in a small practical exercise.

1\\. Understand why exceptions are useful.

2\\. Learn `try` and `except`.

3\\. Understand `else` and `finally`.

4\\. Practise handling errors in small Python examples.

5\\. Apply the concepts to the Expense Analyzer where appropriate.

**Learning principle:** Attempt each exercise first, then review the solution and test your understanding.
