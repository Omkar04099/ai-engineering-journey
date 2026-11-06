# Python Fundamentals — Days 1–9

A reference for concepts practised in the Expense Analyzer project. Keep examples aligned with the current implementation; when behaviour changes, update the tests and notes together.

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
- Empty-input behaviour depends on the function: filtering often returns `[]`, totals return `0`, and averages need an explicit design choice.

```python
def calculate_total(expenses):
    total = 0
    for expense in expenses:
        total += expense["amount"]
    return total
```

## Day 2: Filtering, Aggregation, and Copies

- Build a new result list when filtering; avoid accidentally modifying the input.
- An accumulator keeps a running result, such as a total or count.
- A dictionary can track category totals, counts, and statistics.
- Check that the count is greater than zero before calculating an average. A total of zero can still be valid data.
- **Assignment** (`backup = original`): both variables refer to the same object.
- **Shallow copy** (`original.copy()`): creates a new outer container, but nested mutable objects may still be shared.
- **Deep copy** (`copy.deepcopy(original)`): recursively copies nested objects.
- One pass over `n` records is generally `O(n)`. A single-pass summary can calculate totals and counts together.

```python
import copy

original = {"name": "Laptop", "specs": {"ram": 16}}
shallow = original.copy()
deep = copy.deepcopy(original)

shallow["specs"]["ram"] = 32  # Also changes original["specs"]["ram"]
deep["specs"]["ram"] = 64     # Does not change original
```

## Day 3: Dictionary-Based Data Processing

Three common patterns:

1. **Counting:** use each item as a key and increment its count.
2. **Grouping:** use a key such as category, with a list of matching records as the value.
3. **Aggregation:** maintain running totals, counts, or quantities for each key.

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

An empty list makes a `for` loop run zero times, so initialized results such as `{}` can be returned naturally. A zero-valued record still contributes to the record count.

## Day 4: Automated Testing

Automated tests check expected behaviour and help catch regressions. Passing tests increases confidence only for behaviours actually tested.

```python
assert calculate_total(expenses) == 350, "Total is incorrect"
```

Regular `assert` statements can be disabled when Python runs in optimized mode.

With `unittest`:
- `unittest.TestCase` groups related tests.
- Test method names should begin with `test_`.
- `self.assertEqual(actual, expected)` checks equality.
- `self.assertTrue(value)` and `self.assertFalse(value)` check truthiness.
- `self.assertIsNone(result)` checks that a result is `None`.

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
```

Run tests from the Python project directory:

```bash
python -m unittest test_expense_analyzer.py -v
```

Include cases that exercise different paths through the function and rerun tests after code changes.

## Day 5: Input Validation and Defensive Programming

- `isinstance(value, dict)` checks whether a value is a dictionary.
- `"amount" not in expense` checks whether a dictionary key is missing.
- Distinguish a missing key from a key whose value is `0`. Zero can be valid data.
- Technical validation checks type and structure; business validation checks application-specific rules.
- `return` terminates the function; `continue` skips the current loop iteration; `break` terminates the loop.

The `calculate_total_safe()` exercise rules:
- Top-level input must be a list; otherwise return `"Invalid expenses"`.
- Skip records that are not dictionaries, lack `"amount"`, have an exact amount type other than `int`, or have negative amounts.
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

Avoid `if not expense.get("amount")` when zero is valid; use `"amount" not in expense` to check key existence. Production systems may need to log rejected records rather than silently skipping them.

## Day 6: Python Modules, Packages, and Project Structure

- A **module** is a Python file containing code.
- A **package** organizes related modules under a common directory.
- `expense_analyzer/` is a package; `__init__.py` can expose selected functions.

```text
python-fundamentals/
├── expense_analyzer/
│   ├── __init__.py
│   ├── calculations.py
│   ├── filters.py
│   └── validations.py
├── main.py
├── test_expense_analyzer.py
└── notes.md
```

Import directly from a module:

```python
from expense_analyzer.calculations import calculate_total
```

A package can re-export selected functions in `__init__.py`:

```python
from .calculations import calculate_total
```

- `calculations.py`: totals, averages, highest expenses, and summaries.
- `filters.py`: filtering and grouping.
- `validations.py`: defensive validation and safe total calculation.

Keep reusable functions in modules and application execution in `main.py`:

```python
if __name__ == "__main__":
    main()
```

Python executes a module's top-level statements when it is first imported into a process. Imported modules are normally cached in `sys.modules`; a function body executes when called. After refactoring, run tests, confirm imports resolve, run `main.py`, and verify behaviour is preserved.

## Day 7: Exception Handling

Common exceptions:
- `TypeError`: an operation receives an incompatible type.
- `ValueError`: a value is invalid for the operation.
- `KeyError`: a dictionary key does not exist.
- `ZeroDivisionError`: division by zero is attempted.
- `FileNotFoundError`: a requested file does not exist.
- `json.JSONDecodeError`: JSON text cannot be parsed.

`try` contains risky code; `except` handles a matching exception; `else` runs when `try` completes without an exception; `finally` is commonly used for cleanup. Prefer catching specific exceptions.

Practised `calculate_total_from_strings()` to convert string amounts, handle invalid numeric strings and missing keys, skip invalid records, preserve original data, and test these behaviours.

## Day 8: File Handling and JSON Persistence

- Use `open(path, mode)` to open a file.
- `with open(...) as file:` ensures the file is closed when the block exits.
- Common modes: `"r"` reads, `"w"` writes/truncates, `"a"` appends.
- `json.dump(data, file)` writes JSON to a file; `json.load(file)` reads JSON from a file.
- `json.dumps(data)` serializes to a JSON string; `json.loads(text)` parses a JSON string.

The project includes `save_expenses()` and `load_expenses(file_name="expenses.json")` in `persistent_expense_analyzer.py`.

The loader currently handles:
- Missing files (`FileNotFoundError`) by returning `[]`.
- Malformed JSON (`json.JSONDecodeError`) by returning `[]`.
- A JSON root value that is not a list by returning `[]`.
- A JSON list by returning that list; individual entries still need validation before they can be trusted.

Returning `[]` for malformed JSON is convenient for this exercise, but production applications may need to distinguish missing data from corrupted data.

## Day 9: Temporary Files, Test Lifecycle, Exception Assertions, and Data Validation

### Temporary files

- `tempfile.NamedTemporaryFile(mode="w", delete=False)` creates a named temporary file.
- `file.name` gives its path.
- With `delete=False`, closing the file does not delete it; cleanup must be performed explicitly.
- Close the file before reopening it by path when necessary, especially on Windows.

```python
import json
import os
import tempfile

with tempfile.NamedTemporaryFile(mode="w", delete=False) as file:
    json.dump([{"category": "food", "amount": 150}], file)
    temp_path = file.name

try:
    # Test using temp_path
    pass
finally:
    os.remove(temp_path)
```

The `finally` block ensures cleanup is attempted even if the assertion or code under test raises an exception.

### Test lifecycle and isolation

- `setUp()` runs before each test method.
- `tearDown()` runs after each test method when setup succeeds.
- Creating a separate temporary file for each test helps prevent one test's contents affecting another.

### Exception assertions

```python
with self.assertRaises(KeyError):
    get_expense_amount({"category": "food"})
```

- `assertRaises(ExceptionType)` passes only if the expected exception type is raised.
- `assertRaisesRegex(ExceptionType, pattern)` additionally checks that the exception message matches the pattern.
- If a function catches an exception internally and returns a fallback value, test that return value rather than expecting the exception to escape.

### JSON syntax vs. application-level validity

Valid JSON is not necessarily valid Expense Analyzer data:
- Malformed JSON cannot be parsed.
- A JSON dictionary is valid JSON, but the expected root structure is a list.
- A JSON list can still contain invalid expense records.

The current `load_expenses()` checks file existence, JSON parsing, and root type. The next planned change is to validate every list item before returning it.

### `is_valid_expense()` exercise

The validator checks an individual expense dictionary and returns `True` only when its expected structure and amount rules are satisfied.

Rules:
- Expense must be a dictionary.
- It must contain both `"category"` and `"amount"`.
- Amount must be an integer or float, excluding Boolean values.
- Amount must be non-negative.
- Otherwise return `False`.

```python
def is_valid_expense(expense):
    if not isinstance(expense, dict):
        return False
    if "amount" not in expense:
        return False
    if "category" not in expense:
        return False
    if isinstance(expense["amount"], bool):
        return False
    if not (
        isinstance(expense["amount"], int)
        or isinstance(expense["amount"], float)
    ):
        return False
    if expense["amount"] < 0:
        return False
    return True
```

Python's `bool` is a subclass of `int`, so `isinstance(True, int)` returns `True`. Explicitly reject Boolean amounts before the numeric check.

Test cases practised: valid integers, valid floats, Boolean and string amounts, missing category, missing amount, negative amount, and non-dictionary input.

### Test assertion lesson

Assert against the result of the function, not the input:

```python
output = is_valid_expense(["food", 150])
self.assertFalse(output)
```

`["food", 150]` is a non-empty list and is truthy. The function result is `False`, which is what the test must check.


**## Day 10: Numeric Validation and Integration Testing**

**### Non-finite numbers**

- `float("nan")` represents Not a Number.
- `float("inf")` and `float("-inf")` represent positive and negative infinity.
- Comparisons with NaN do not behave like normal numeric comparisons.
- Use `math.isfinite(value)` to reject NaN and infinity.

```python
import math

math.isfinite(150)          # True
math.isfinite(float("nan")) # False
math.isfinite(float("inf")) # False
```

**### Strict expense validation**

- Integrated `is_valid_expense()` into `load_expenses()`.
- Used `all()` with a generator expression to validate every expense.
- The entire dataset is rejected (`[]`) if any record is invalid.
- `all()` stops at the first `False` result (short-circuit evaluation).
- `all([])` returns `True`.

```python
if not all(is_valid_expense(expense) for expense in expenses):
    return []

return expenses
```

**### Testing**

Added tests for:
- NaN, positive infinity, and negative infinity.
- Valid and invalid expense lists.
- Invalid record types and amounts.

**Result: All 19 tests passed.**

## Day 11: Introduction to FastAPI

### Environment setup

- Created a virtual environment using `py -m venv venv`.
- Activated it using `.\venv\Scripts\Activate.ps1`.
- Installed FastAPI and Uvicorn.
- Uvicorn runs the FastAPI application using ASGI.
- `uvicorn main:app --reload` starts the development server.
- `/docs` provides interactive Swagger documentation.

### FastAPI fundamentals

- `app = FastAPI()` creates the application instance.
- `@app.get()` defines GET endpoints.
- `@app.post()` defines POST endpoints.
- FastAPI supports both `def` and `async def` route handlers.
- ASGI supports asynchronous communication and WebSockets.

### Request parameters

- Path parameters identify resources, e.g. `/users/{user_id}`.
- Query parameters provide optional or required filters, e.g. `/products?category=electronics&limit=10`.
- Parameters without defaults are required; parameters with defaults are optional.
- Type annotations allow FastAPI to validate and convert incoming parameters.

### Request bodies and Pydantic

- `BaseModel` defines structured request data.
- FastAPI parses JSON request bodies and validates them using Pydantic.
- `Field(gt=0)` enforces a value greater than zero.
- `Field(ge=0)` allows zero and positive values.
- `Field(min_length=1)` rejects empty strings.
- FastAPI automatically converts returned dictionaries into JSON responses.
- Invalid request data produces a validation error (HTTP 422).


# Day 12 — FastAPI REST API Fundamentals

## Topics Covered

### 1. HTTP Methods and CRUD

Learned the purpose of HTTP methods used in REST APIs:

| HTTP Method | Operation | Purpose |
|---|---|---|
| GET | Read | Retrieve resources |
| POST | Create | Create new resources |
| PUT | Update | Replace an existing resource |
| PATCH | Partial Update | Modify selected fields |
| DELETE | Delete | Remove a resource |

### 2. PUT vs PATCH

- PUT generally replaces the complete resource representation.
- PATCH modifies only the specified fields.
- Both methods can accept request bodies.

### 3. Request Models vs Response Models

Practised creating separate Pydantic models for incoming and outgoing data.

**ExpenseCreate:**
- Defines the fields expected from the client.
- Used to validate incoming request data.
- Does not contain server-generated fields such as `id`.
- Server-managed fields such as `created_by` and `is_deleted` should not be controlled by the client.

**ExpenseResponse:**
- Defines the structure of the API response.
- Includes the server-generated expense ID.
- Controls which fields are exposed to the frontend.

### 4. FastAPI Response Models

Learned how to use `response_model`:

```python
@app.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def expense_response(expense_id: int):
    return {
        "id": expense_id,
        "title": "Electricity Bill",
        "amount": 1200,
        "category": "Utilities",
        "created_by": "Admin 123",
        "is_deleted": True
    }
```

FastAPI uses the response model to:
- Validate returned data.
- Serialize the response.
- Filter out fields not defined in the response model.
- Generate API documentation.

Important: Response filtering is useful for controlling exposed fields, but it does not replace authorization and security checks.

### 5. HTTP Status Codes

| Status Code | Meaning |
|---|---|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Unprocessable Content |
| 500 | Internal Server Error |

Important distinctions:
- 404: Requested resource does not exist.
- 422: Request data failed validation.
- 204: Successful operation with no response body.

FastAPI automatically returns 422 for standard request validation failures.

## Mistakes and Lessons to Remember

1. A GET endpoint using a path parameter does not need an `ExpenseCreate` request body when retrieving an expense by ID.
2. Path parameter names should match the endpoint function parameters.
3. Use explicit type annotations such as `expense_id: int`.
4. Never access attributes that are not defined in the corresponding Pydantic model.
5. Do not allow clients to control server-generated or server-managed fields.
6. Separate request and response models according to their responsibilities.
7. Extra fields returned by an endpoint are filtered when they are not included in its response model.
8. GET should retrieve resources rather than modify server state.
9. POST is commonly used for resource creation, while PUT and PATCH are used for updates.

## Exercises and Assessment

- HTTP methods exercise: 5/5.
- HTTP status codes exercise: 5/5.
- Implemented and reviewed the structure of `ExpenseCreate` and `ExpenseResponse`.
- Practised identifying incorrect request-body parameters and model attribute access.

## Progress

**Completed:**
- HTTP methods and CRUD fundamentals.
- Request models and response models.
- Response filtering with `response_model`.
- HTTP status codes and their practical applications.

**Not yet completed:**
- Full CRUD endpoint implementation.
- Handling missing resources with `HTTPException`.
- Testing CRUD operations using Swagger UI.

## Next Step

**Day 13 — Implementing CRUD operations using FastAPI.**

We will:
1. Store expenses in an in-memory Python list.
2. Implement POST to create expenses.
3. Implement GET to retrieve all expenses and individual expenses.
4. Implement PUT and PATCH to update expenses.
5. Implement DELETE to remove expenses.
6. Handle missing expense IDs using `HTTPException`.
7. Return appropriate HTTP status codes.
8. Test all endpoints through Swagger UI.

We will use in-memory storage first and introduce database integration later.

**Key takeaway:** Understand the complete request-response lifecycle before introducing databases or advanced backend concepts.