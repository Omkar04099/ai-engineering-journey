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

# Day 13: FastAPI CRUD Operations and Python Variable Scope

## 1. Implementing CRUD Operations

Completed the CRUD functionality for the Expense API using FastAPI and Pydantic.

| Operation | HTTP Method | Endpoint | Expected Status |
|---|---|---|---|
| Create expense | POST | `/expenses` | 201 Created |
| Fetch all expenses | GET | `/expenses` | 200 OK |
| Fetch expense by ID | GET | `/expenses/{expense_id}` | 200 OK / 404 |
| Replace expense | PUT | `/expenses/{expense_id}` | 200 OK / 404 |
| Partially update expense | PATCH | `/expenses/{expense_id}` | 200 OK / 404 |
| Delete expense | DELETE | `/expenses/{expense_id}` | 204 No Content / 404 |

## 2. Request and Response Models

Used separate Pydantic models for different API responsibilities:

- `ExpenseCreate`: Validates expense creation and replacement input.
- `ExpenseResponse`: Defines the structure returned by the API, including the server-generated ID.
- `ExpenseUpdate`: Allows partial updates through optional fields.

## 3. PUT vs PATCH

**PUT**
- Replaces the editable fields of an existing resource.
- Requires all fields defined by `ExpenseCreate`.
- Preserves the original resource ID.

**PATCH**
- Updates only the fields provided by the client.
- Uses `model_dump(exclude_unset=True)` to exclude fields that were not supplied.

Example:

```python
expense.update(exp.model_dump(exclude_unset=True))
```

## 4. Python Mutable Objects and Variable Scope

Learned the difference between modifying an existing object and reassigning a variable.

**Modifying a mutable object:**

```python
expenses = []

def add_expense():
    expenses.append({"id": 1})
```

This works without `global` because the existing list is being modified.

**Reassigning a global variable:**

```python
counter = 1

def increment():
    global counter
    counter += 1
```

The `global` keyword tells Python that the function should use and modify the module-level variable.

Key distinction:

- `expenses.append(item)` modifies an existing list.
- `counter += 1` reassigns an integer variable.

## 5. Stable ID Generation

Initially, IDs were generated using:

```python
id = len(expenses) + 1
```

This caused duplicate IDs after deleting an expense.

Example:

- Existing IDs: 1, 2, 3
- Delete ID 2.
- List length becomes 2.
- Next generated ID becomes 3, causing a duplicate.

Fixed this by maintaining a separate counter:

```python
next_expense_id = 1

def create_expense(expense: ExpenseCreate):
    global next_expense_id

    expense_id = next_expense_id
    next_expense_id += 1
```

The counter is independent of the list length, so deleted IDs are not reused.

**Production limitation:** A module-level counter is suitable for this learning exercise, but it resets on application restart and is not safe for multiple workers or concurrent ID generation. Databases will provide persistent ID generation later.

## 6. PATCH: Missing Fields vs Explicit Null

Learned the difference between:

```python
exp.model_dump(exclude_unset=True)
```

and:

```python
exp.model_dump(exclude_none=True)
```

- `exclude_unset=True`: Excludes fields the client did not provide.
- `exclude_none=True`: Excludes fields whose values are `None`.

Example request:

```json
{
    "amount": 500
}
```

With `exclude_unset=True`:

```python
{"amount": 500}
```

Example request:

```json
{
    "amount": 500,
    "title": null
}
```

With `exclude_unset=True`:

```python
{"amount": 500, "title": None}
```

Important: `exclude_unset=True` preserves the distinction between an omitted field and an explicitly supplied `null`.

The current `ExpenseUpdate` model still permits explicit null values. This validation issue is pending and will be addressed after learning Pydantic validators.

## Day 14: Pydantic Validators, Pytest, and Regex Fundamentals

### 1. Pydantic Field Validators

Learned how to add custom validation and preprocessing to Pydantic models using `@field_validator`.

**Before validators**

- Use `mode="before"` to process raw input before Pydantic performs its normal type validation.
- Useful for cleaning or transforming incoming values.
- Example: removing a currency symbol and surrounding whitespace before converting an amount to a float.

**After validators**

- The default validator mode is `after`.
- Runs after Pydantic has validated and converted the field's type.
- Useful for normalizing or checking already validated values.

**Example concepts practised:**

- Removing leading and trailing whitespace from titles and categories using `.strip()`.
- Converting categories to lowercase using `.lower()`.
- Removing the `₹` symbol from string amounts before numeric conversion.
- Using `Field(gt=0)` to enforce a positive amount.
- Raising `ValueError` when custom validation fails.

### 2. Pydantic Validation Errors

- `ValidationError` is raised by Pydantic when model validation fails.
- `ValueError` is a built-in Python exception that can be raised inside a custom validator.
- Pydantic catches validator errors and reports them as a `ValidationError`.
- `model_validate()` validates a Python dictionary against a Pydantic model.
- `.errors()` returns structured validation error details.
- Error details include fields such as `loc`, `msg`, `type`, and `input`.

### 3. Testing with Pytest

Started using `pytest` for FastAPI-related tests.

Practised:

- Writing test functions whose names begin with `test_`.
- Using regular Python `assert` statements.
- Using `pytest.raises(ValidationError)` to verify expected validation failures.
- Inspecting validation details using `exc_info.value.errors()`.
- Checking that multiple invalid fields are reported.

Example:

```python
with pytest.raises(ValidationError) as exc_info:
    ExpenseCreate.model_validate(expense_data)

errors = exc_info.value.errors()
assert len(errors) == 3
```

Pytest can also run tests written using Python's `unittest` framework.

### 4. Python Regular Expressions (Regex)

Learned the fundamentals of the `re` module for pattern-based string validation.

**Raw strings**

- The `r` prefix creates a raw string literal.
- It prevents Python from interpreting most backslash escape sequences.
- `r"\d+"` and `"\\d+"` pass equivalent patterns to the regex engine.

**Regex functions practised**

- `re.fullmatch()` checks whether the entire input matches a pattern.
- `re.search()` searches for a matching portion of a string.
- `re.findall()` finds all matching occurrences.
- `re.sub()` replaces matching portions of a string.

**Character classes**

- `\d`: digit.
- `[0-9]`: digit from 0 to 9.
- `[a-z]`: lowercase English letter.
- `[A-Z]`: uppercase English letter.
- `[a-zA-Z]`: uppercase or lowercase English letter.

**Quantifiers and grouping**

- `+`: one or more occurrences.
- `*`: zero or more occurrences.
- `?`: zero or one occurrence.
- `{3}`: exactly three occurrences.
- `{2,3}`: between two and three occurrences.
- `|`: alternation (OR).
- `(...)`: groups regex elements together.
- `\.`: matches a literal dot.

### 5. Indian Number Grouping Regex Exercise

Practised building a regex to validate Indian-style comma grouping.

Examples accepted:

- `1500`
- `150000`
- `1,500`
- `15,000`
- `1,50,000`
- `10,00,000`
- `15,00,000`
- `12,34,56,789`

Examples rejected:

- `1,5,00`
- `1,,500`
- `12.50`

The grouped-number pattern:

```python
grouped = r"[0-9]{1,2}(,[0-9]{2})*,[0-9]{3}"
```

The ungrouped-number pattern:

```python
ungrouped = r"\d+"
```

Combined pattern:

```python
indian_number_pattern = rf"(?:{ungrouped}|{grouped})"
```

Validation function:

```python
import re

def is_valid_number(value):
    return bool(re.fullmatch(indian_number_pattern, value))
```

**Important:** This exercise validates the number's digit and comma grouping. Currency symbols, whitespace normalization, and decimal amounts have not yet been integrated.

### 6. Lessons to Remember

- `mode="before"` and `mode="after"` execute at different stages of Pydantic validation.
- `Field` constraints should be used for standard validation rules where appropriate.
- A `ValueError` raised inside a Pydantic validator becomes part of Pydantic's validation error.
- `re.fullmatch()` is useful when the entire input must follow a specific format.
- Raw strings make regex patterns easier to write and read.
- A regex should be built and tested incrementally rather than written as one complicated expression.

## Day 15: Database Fundamentals and SQL

### 1. Why Databases Are Needed

- Python in-memory lists store data temporarily while the application is running.
- Data stored only in memory is lost when the application restarts.
- Databases provide persistent storage.
- A relational database stores structured data in tables.

### 2. Relational Database Fundamentals

- A **table** represents a collection of related records.
- A **row** represents one complete record.
- A **column** represents an individual attribute or field.
- PostgreSQL is a relational database management system (RDBMS).
- SQL (Structured Query Language) is used to interact with relational databases.

### 3. Primary Keys

A primary key uniquely identifies each record in a table.

Important rules:

- Primary key values must be unique.
- Primary key values cannot be NULL.
- A table can have only one primary key constraint.
- A primary key can consist of one column or multiple columns.

Example:

```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY,
    title VARCHAR(100),
    amount NUMERIC(10, 2)
);
```

A separate `id` column is commonly used as a primary key because expense titles and amounts can repeat.

### 4. Foreign Keys

A foreign key establishes a relationship between two tables.

Example:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE expenses (
    id INTEGER PRIMARY KEY,
    title VARCHAR(100),
    user_id INTEGER REFERENCES users(id)
);
```

Key concepts:

- `users.id` is the referenced primary key.
- `expenses.user_id` is a foreign key.
- Multiple expenses can reference the same user.
- A foreign key prevents references to non-existent records.
- Foreign-key columns can contain repeated values.
- Foreign-key columns should use compatible data types with their referenced columns.

### 5. Composite Primary Keys

A composite primary key uses two or more columns together to uniquely identify a record.

Example:

```sql
CREATE TABLE employee_projects (
    employee_id INTEGER,
    project_id INTEGER,
    role VARCHAR(50),
    PRIMARY KEY (employee_id, project_id)
);
```

Important points:

- `employee_id` alone may not be unique.
- `project_id` alone may not be unique.
- Their combination can uniquely identify an employee-project assignment.
- If multiple roles per employee-project combination are allowed, the role can be included in the composite key.
- Another design option is to use a separate ID and enforce uniqueness with a UNIQUE constraint.

### 6. Foreign Key Deletion Strategies

Learned how foreign-key relationships affect deletion.

| Strategy | Behaviour |
|---|---|
| RESTRICT | Prevents deletion while dependent records exist. |
| CASCADE | Automatically deletes dependent records. |
| SET NULL | Sets the referencing foreign key to NULL. |

Example:

```sql
CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    user_id INTEGER REFERENCES users(id)
        ON DELETE CASCADE
);
```

`SET NULL` requires the foreign-key column to allow NULL values.

PostgreSQL's default foreign-key deletion behaviour is NO ACTION.

### 7. SQL CRUD Operations

CRUD stands for Create, Read, Update and Delete.

**INSERT — Create records**

```sql
INSERT INTO expenses (title, amount, category)
VALUES ('Dinner', 350, 'Food');
```

Multiple records can be inserted in one statement:

```sql
INSERT INTO expenses (title, amount, category)
VALUES
    ('Dinner', 350, 'Food'),
    ('Petrol', 600, 'Travel'),
    ('Shopping', 1200, 'Personal');
```

**SELECT — Retrieve records**

```sql
SELECT * FROM expenses;

SELECT title, amount
FROM expenses;

SELECT *
FROM expenses
WHERE category = 'Food';
```

**WHERE conditions**

Practised comparison operators:

- `=` : Equal to
- `!=` : Not equal to
- `>` : Greater than
- `<` : Less than
- `>=` : Greater than or equal to
- `<=` : Less than or equal to

Also practised combining conditions using `AND` and `OR`.

Example:

```sql
SELECT *
FROM expenses
WHERE category = 'Food'
AND amount > 300;
```

**UPDATE — Modify records**

```sql
UPDATE expenses
SET amount = 400
WHERE id = 1;
```

Updating amounts using existing values:

```sql
UPDATE expenses
SET amount = amount * 1.10
WHERE category = 'Travel';
```

Important: Always use an appropriate WHERE condition when updating specific records. Without WHERE, every row is updated.

**DELETE — Remove records**

```sql
DELETE FROM expenses
WHERE id = 3;
```

Delete records based on conditions:

```sql
DELETE FROM expenses
WHERE amount <= 100;
```

Important: DELETE without WHERE removes all rows but keeps the table structure.

### 8. Sorting and Pagination

**ORDER BY**

Sort records using ASC or DESC.

```sql
SELECT *
FROM expenses
ORDER BY amount DESC;
```

- `ASC`: Ascending order (default).
- `DESC`: Descending order.

**LIMIT**

Restricts the number of returned records.

```sql
SELECT *
FROM expenses
ORDER BY amount DESC
LIMIT 3;
```

**OFFSET**

Skips a specified number of records.

```sql
SELECT *
FROM expenses
ORDER BY amount DESC
LIMIT 1 OFFSET 1;
```

This retrieves the second-highest expense when amounts are distinct.

Key distinction:

- LIMIT controls how many records are returned.
- OFFSET controls how many records are skipped.

### 9. Aggregate Function: COUNT

`COUNT(*)` returns the number of rows.

```sql
SELECT COUNT(*)
FROM expenses;
```

Using an alias:

```sql
SELECT COUNT(*) AS total_expenses
FROM expenses;
```

COUNT can also be combined with WHERE:

```sql
SELECT COUNT(*)
FROM expenses
WHERE category = 'Food';
```

# Day 16: PostgreSQL Fundamentals and Python Integration Using Psycopg

## 1. Local PostgreSQL Setup

Created a fresh local PostgreSQL database for the learning project.

- Database name: `expense_tracker_db`
- PostgreSQL user: `postgres`
- Host: `localhost`
- Default PostgreSQL port: `5432`

Kept this database separate from the NexusAI project and its NeonDB configuration.

## 2. Creating Tables Using DDL

Learned the difference between:

- **DDL (Data Definition Language):** Defines or changes database structure.
- **DML (Data Manipulation Language):** Inserts, updates, and deletes table records.

Common DDL commands:

- `CREATE`: Creates database objects such as tables.
- `ALTER`: Changes existing database structures.
- `DROP`: Removes database objects.

Created a `products` table:

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price > 0),
    quantity INTEGER NOT NULL CHECK (quantity >= 0) DEFAULT 0
);
```

## 3. SQL Data Types and Constraints

### Data types practised

| Data type | Purpose |
|---|---|
| INTEGER | Whole numbers |
| VARCHAR(100) | Text with a maximum of 100 characters |
| NUMERIC(10, 2) | Exact decimal values with 2 fractional digits |
| SERIAL | Auto-incrementing integer column backed by a sequence |

### Constraints practised

**PRIMARY KEY**

- Uniquely identifies each record.
- Does not allow duplicate values.
- Does not allow NULL values.
- A table has one primary key constraint, which can contain multiple columns.

**NOT NULL**

- Requires a value to be provided.
- Allows valid values such as zero.
- Does not independently enforce positive or non-negative values.

**CHECK**

Enforces a condition on column values.

Examples:

```sql
CHECK (price > 0)
CHECK (quantity >= 0)
```

**DEFAULT**

Provides a value when a column is omitted from an INSERT statement.

Example:

```sql
quantity INTEGER NOT NULL DEFAULT 0
```

Important distinction:

- Omitting `quantity` applies its default value.
- Explicitly inserting `NULL` violates `NOT NULL`.
- `DEFAULT` can also be specified explicitly in an INSERT statement.

Example:

```sql
INSERT INTO products (name, price, quantity)
VALUES
    ('Mechanical Keyboard', 2499.00, 5),
    ('Wireless Mouse', 799.50, DEFAULT);
```

## 4. Inspecting Table Metadata

Used PostgreSQL's `information_schema.columns` to inspect table definitions.

```sql
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'products';
```

Observed:

- `SERIAL` is represented as an integer column with a sequence-based default (`nextval(...)`).
- Primary keys are automatically non-nullable.
- `NOT NULL` columns report `is_nullable = NO`.
- The quantity column reports its default as `0`.

Learned that PostgreSQL uses sequences to generate successive values for SERIAL columns.

## 5. Python Environment Configuration Using .env

Created a `.env` file to separate database configuration from application code.

Example:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=expense_tracker_db
DB_USER=postgres
DB_PASSWORD=your_actual_password
```

Installed the `python-dotenv` package:

```bash
python -m pip install python-dotenv
```

### Loading environment variables

```python
from dotenv import load_dotenv
import os

load_dotenv()

password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
```

Important concepts:

- `.env` is a plain-text configuration file.
- Python does not automatically load `.env` files.
- `load_dotenv()` reads the file and loads its variables into the process environment.
- `os.getenv()` retrieves an environment variable.
- `os.getenv()` returns `None` when the requested variable is missing and no fallback is supplied.
- Environment variables are returned as strings by `os.getenv()`.

Added `.env` to `.gitignore` to prevent database credentials from being committed to GitHub.

A `.env.example` file can be committed with placeholder values.

## 6. Connecting Python to PostgreSQL Using Psycopg

Installed Psycopg 3:

```bash
python -m pip install "psycopg[binary]"
```

### Establishing a connection

```python
import psycopg

connection = psycopg.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=password
)
```

Important concepts:

- `psycopg.connect()` establishes a connection with PostgreSQL.
- It returns a connection object when successful.
- It raises an exception if the connection fails.
- `dbname` is the parameter expected by Psycopg for the database name.

### Connection object vs Cursor object

**Connection object**

- Establishes and manages communication with PostgreSQL.
- Provides access to cursor creation and transaction management.

**Cursor object**

- Executes SQL statements through the connection.
- Retrieves query results.

Create a cursor:

```python
cursor = connection.cursor()
```

## 7. Executing SQL and Retrieving Records

### cursor.execute()

Executes an SQL statement.

```python
cursor.execute("SELECT * FROM products")
```

### cursor.fetchone()

Retrieves one available row.

```python
product = cursor.fetchone()
```

Returns `None` when no rows remain.

### cursor.fetchall()

Retrieves all remaining rows.

```python
products = cursor.fetchall()
```

Important: The cursor maintains its position in the result set. Calling `fetchone()` consumes a row, so a subsequent `fetchall()` returns only the remaining rows.

### Psycopg's default row structure

Psycopg returns rows as tuples by default.

Example:

```python
(
    1,
    'Mechanical Keyboard',
    Decimal('2499.00'),
    5
)
```

For a list of tuples:

```python
products[0][1]  # First product name
products[1][2]  # Second product price
```

The first index identifies the row, and the second identifies the column position.

Dictionary-style rows are also possible, but tuples are sufficient for the current learning exercise.

## 8. PostgreSQL NUMERIC and Python Decimal

Our PostgreSQL price column uses:

```sql
NUMERIC(10, 2)
```

Psycopg maps PostgreSQL NUMERIC values to Python's `Decimal` type by default.

Why this matters:

- `NUMERIC` supports exact decimal storage.
- Python `float` uses binary floating-point representation and can introduce precision differences.
- Python `Decimal` is useful for financial calculations requiring controlled decimal precision.

Example:

```python
0.1 + 0.2
# 0.30000000000000004
```

## 9. Parameterized SQL Queries

Learned why SQL queries should not be constructed by directly interpolating untrusted user input.

### Unsafe approach

```python
query = f"""
INSERT INTO products (name, price, quantity)
VALUES ('{product_name}', {product_price}, {product_quantity})
"""
```

Direct string interpolation can introduce SQL injection vulnerabilities.

### Safe approach: Parameterized queries

Psycopg uses `%s` placeholders for parameter binding.

```python
query = """
INSERT INTO products (name, price, quantity)
VALUES (%s, %s, %s)
"""

cursor.execute(
    query,
    (product_name, product_price, product_quantity)
)
```

Important points:

- SQL structure and input values are supplied separately.
- The second argument is a tuple of parameter values.
- Placeholder order must match the supplied parameter order.
- `%s` is used for strings, integers, and decimal values.
- Do not put quotes around `%s` placeholders.
- Psycopg safely binds the values rather than treating them as SQL commands.

Parameterized queries are an essential defence against SQL injection when handling user-provided values.

## 10. Database Transactions and Commit

Database operations such as INSERT are performed within transactions.

A transaction represents a unit of database work that can be committed or rolled back.

**Commit:**

```python
connection.commit()
```

Makes the transaction's changes permanent.

**Rollback:**

```python
connection.rollback()
```

Cancels uncommitted changes in the current transaction.

Learned that closing a connection with an uncommitted transaction causes PostgreSQL to roll back that transaction.

The practical INSERT operation used:

```python
cursor.execute(query, values)
connection.commit()
```

## 11. Practical Implementation and Results

Successfully completed the following exercises:

- Created a fresh local PostgreSQL database.
- Created a `products` table with a SERIAL primary key.
- Applied NOT NULL, CHECK, and DEFAULT constraints.
- Inserted products using pgAdmin.
- Retrieved records using SQL SELECT.
- Inspected table metadata.
- Configured database credentials using `.env`.
- Loaded environment variables using `python-dotenv`.
- Established a Python-to-PostgreSQL connection using Psycopg.
- Created a cursor and executed SELECT.
- Retrieved records using `fetchall()`.
- Successfully inserted a product using a parameterized query.
- Committed the INSERT transaction.
- Verified the inserted record in pgAdmin.

Example product inserted through Python:

```python
product_name = "Wireless Headphones"
product_price = 1999.50
product_quantity = 5
```

The insertion completed successfully and the record was visible in PostgreSQL.

# Day 17: PostgreSQL Transactions, Psycopg CRUD, Context Managers, and Project Structure

## 1. Database Transaction Error Handling

Learned how to handle database errors using Python exception handling and Psycopg.

### try, except, else, and finally

- `try`: Contains code that might raise an exception.
- `except`: Handles matching exceptions raised inside the `try` block.
- `else`: Executes only when the `try` block completes without an exception.
- `finally`: Executes whether an exception occurs or not; commonly used for resource cleanup.

### Handling Psycopg errors

Practised catching database exceptions using `psycopg.Error`.

```python
try:
    cursor.execute(query, parameters)
    connection.commit()

except psycopg.Error as error:
    print("Database error:", error)
    connection.rollback()

finally:
    cursor.close()
    connection.close()
```

Important concepts:

- `psycopg.Error` catches database-related exceptions raised by Psycopg.
- If `cursor.execute()` fails, execution moves to the matching `except` block.
- If `connection.commit()` is inside the `try` block, commit errors matching the exception handler can also be caught.
- An exception raised inside `else` is not caught by the preceding `except`.
- `finally` is useful for ensuring resource cleanup.
- Rollback is an attempt to cancel uncommitted changes after a transaction failure.

## 2. Understanding Transaction Boundaries

Learned how multiple SQL operations behave inside a transaction.

### Example: Multiple INSERT operations in one transaction

```python
try:
    cursor.execute(query_a, parameters_a)
    cursor.execute(query_b, parameters_b)

    connection.commit()

except psycopg.Error as error:
    print("Database error:", error)
    connection.rollback()
```

If the first INSERT succeeds but the second INSERT fails:

- The first INSERT has executed but is not committed.
- The second INSERT fails.
- Execution moves to the exception handler.
- `rollback()` cancels both uncommitted INSERT operations.

### Separate transactions

If Product A is inserted and committed in one transaction, and Product B is inserted in another transaction:

- Product A remains saved after its successful commit.
- If Product B fails, rolling back its transaction does not undo Product A.

### Key takeaway

A transaction groups database operations into a unit of work.

The atomicity principle means that a transaction's changes are committed together or rolled back together.

## 3. PostgreSQL Sequence Behaviour

Observed that PostgreSQL SERIAL-generated IDs can have gaps.

Example:

- A failed INSERT attempted to use ID 5.
- The transaction was rolled back.
- The next generated ID did not necessarily reuse 5.

Important:

- PostgreSQL sequences are not rolled back with the transaction.
- Deleting a record also does not reset the sequence.
- Consecutive IDs are not guaranteed.
- ID gaps are normal and should not be treated as errors.

## 4. SELECT Operations Using Psycopg

Learned to retrieve an individual product using a parameterized SELECT query.

```python
def get_product_by_id(cursor, product_id):
    query = """
    SELECT * FROM products
    WHERE id = %s
    """

    cursor.execute(query, (product_id,))
    product = cursor.fetchone()

    return product
```

### Handling missing records

- `fetchone()` returns a tuple when a matching record exists.
- `fetchone()` returns `None` when no matching record exists.
- A missing record does not raise a database exception.

Practised returning `None` from the database function and allowing the calling code to decide how to display a missing-record message.

## 5. UPDATE Operations Using Psycopg

Practised updating a product's price using a parameterized query.

```python
query = """
UPDATE products
SET price = %s
WHERE id = %s
"""

cursor.execute(query, (new_price, product_id))
affected_rows = cursor.rowcount
```

### Understanding cursor.rowcount

`cursor.rowcount` reports the number of rows affected by the last executed query.

| Result | Meaning |
|---|---|
| 1 | One matching row was updated |
| 0 | No matching row was updated |

Important:

- UPDATE does not raise an exception just because the specified ID does not exist.
- A valid UPDATE query can execute successfully while affecting zero rows.
- Use `rowcount` to detect whether a matching record was updated.
- Database constraint violations, such as a negative price when `CHECK (price > 0)` exists, raise database errors.

### Parameter order lesson

For this query:

```python
UPDATE products
SET price = %s
WHERE id = %s
```

The correct parameter order is:

```python
cursor.execute(query, (new_price, product_id))
```

The order of values must match the order of SQL placeholders.

A mismatch can cause the query to execute against unintended values or affect zero rows without raising an exception.

## 6. DELETE Operations Using Psycopg

Practised deleting products using a parameterized query.

```python
query = """
DELETE FROM products
WHERE id = %s
"""

cursor.execute(query, (product_id,))
affected_rows = cursor.rowcount
```

Important concepts:

- `rowcount == 1` means one record was deleted.
- `rowcount == 0` means no matching record was found.
- DELETE does not raise an exception simply because the specified ID does not exist.
- A DELETE query without a WHERE condition removes all records from the table.
- Capture `rowcount` immediately after executing the query.

## 7. Psycopg Context Managers

Learned how Python's `with` statement simplifies resource management.

### Cursor context manager

Previously:

```python
cursor = connection.cursor()

try:
    cursor.execute(query, parameters)
    product = cursor.fetchone()

finally:
    cursor.close()
```

Using a context manager:

```python
with connection.cursor() as cursor:
    cursor.execute(query, parameters)
    product = cursor.fetchone()
```

Important:

- Creates a cursor for the block.
- Automatically closes the cursor when the block exits.
- Does not close the database connection.

### Connection context manager

Psycopg also supports connection context managers.

```python
with psycopg.connect(...) as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
```

The connection context manager:

- Commits the transaction when the block exits successfully.
- Rolls back the transaction if an exception occurs.
- Closes the connection when the block exits.

The cursor context manager independently handles cursor cleanup.

### Returning from inside a context manager

A return statement inside a `with` block still triggers the context manager's exit and cleanup behaviour.

## 8. Reusable Database Connection Function

Initially, connection configuration was repeated in database functions.

Created a reusable function:

```python
def get_connection():
    return psycopg.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=password,
        dbname=db_name
    )
```

Database functions can now obtain a connection using:

```python
with get_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute(query, parameters)
```

Benefits:

- Avoids repeating connection configuration.
- Centralizes database connection creation.
- Makes database functions cleaner.
- Simplifies future configuration changes.

Environment variable values are read when the module executes the `os.getenv()` statements. Changes to `.env` during an already-running Python process do not automatically refresh those variables.

## 9. Separating Database Modules and Packages

Learned to organize database-related code into a dedicated Python package.

### Project structure

```text
fastapi-learning/
│
├── database/
│   ├── __init__.py
│   ├── connection.py
│   └── operations.py
│
├── test_db_connection.py
├── .env
└── .gitignore
```

### connection.py

Responsibilities:

- Import `load_dotenv`, `os`, and `psycopg`.
- Load environment variables.
- Read database configuration.
- Provide the reusable `get_connection()` function.

Implementation:

```python
from dotenv import load_dotenv
import os
import psycopg

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")


def get_connection():
    return psycopg.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=password
    )
```

### operations.py

Responsibilities:

- Import the reusable connection function.
- Contain reusable database CRUD functions.
- Keep SQL operations separate from connection configuration.

Used a relative import:

```python
from .connection import get_connection
```

The dot indicates that the module is being imported from the same package.

### __init__.py

Learned that `__init__.py` traditionally identifies a regular Python package and can expose selected functions through package-level imports.

Example:

```python
from .connection import get_connection
from .operations import get_product_by_id
from .operations import update_product_price
from .operations import delete_product_by_id
```

Now functions can be imported directly from the package:

```python
from database import get_connection, get_product_by_id
```

This avoids specifying the individual module path for every exposed function.

Modern Python also supports namespace packages without `__init__.py`; we are using an explicit regular package structure in this project.

## 10. Database Operations Module

Moved the database retrieval, update, and deletion functions into `database/operations.py`.

### SELECT

```python
def get_product_by_id(product_id):
    query = """
    SELECT * FROM products
    WHERE id = %s
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (product_id,))
            product = cursor.fetchone()
            return product
```

### UPDATE

```python
def update_product_price(product_id, new_price):
    query = """
    UPDATE products
    SET price = %s
    WHERE id = %s
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (new_price, product_id))
            affected_rows = cursor.rowcount

            if affected_rows == 0:
                return f"Product not found for product_id: {product_id}"

            return "Product Updated"
```

### DELETE

```python
def delete_product_by_id(product_id):
    query = """
    DELETE FROM products
    WHERE id = %s
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (product_id,))
            affected_rows = cursor.rowcount

            if affected_rows == 0:
                return f"Product not found with product_id: {product_id}"

            return "Product deleted successfully"
```

The connection context manager handles transaction commit or rollback and connection closure. The cursor context manager handles cursor closure.

The INSERT operation was practised separately using a parameterized query and transaction commit. It has not yet been added to `operations.py`.

## 11. Practical Results

Successfully practised:

- Triggering a database constraint violation using a negative product price.
- Catching the error using `psycopg.Error`.
- Rolling back an unsuccessful transaction.
- Verifying that the failed product was not inserted.
- Understanding transaction boundaries with multiple INSERT operations.
- Retrieving existing and non-existing products.
- Updating existing products.
- Detecting missing products using `cursor.rowcount`.
- Handling CHECK constraint violations during UPDATE.
- Deleting existing products.
- Handling deletion requests for non-existing IDs.
- Using cursor and connection context managers.
- Creating a reusable database connection function.
- Moving database connection logic into `connection.py`.
- Moving SELECT, UPDATE, and DELETE functions into `operations.py`.
- Exposing functions through `database/__init__.py`.
- Importing database functions using package-level imports.

### Debugging lesson

During UPDATE implementation, the parameter order did not match the SQL placeholder order.

Incorrect:

```python
cursor.execute(query, (product_id, new_price))
```

Correct:

```python
cursor.execute(query, (new_price, product_id))
```

This demonstrated why checking SQL placeholder order and inspecting affected-row counts are important when debugging database operations.

# Day 18: Completing PostgreSQL CRUD Operations and Automated Database Testing

## 1. Completing the Database CRUD Module

Completed the reusable database CRUD module by adding the INSERT operation to `database/operations.py`.

The module now contains all four operations:

- `create_product()`
- `get_product_by_id()`
- `update_product_price()`
- `delete_product_by_id()`

The functions use the reusable `get_connection()` function and Psycopg context managers.

## 2. INSERT Operation and PostgreSQL RETURNING

Implemented product creation using a parameterized INSERT query.

```python
def create_product(product_name, product_price, product_quantity):
    query = """
        INSERT INTO products (name, price, quantity)
        VALUES (%s, %s, %s)
        RETURNING id
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (product_name, product_price, product_quantity)
            )
            product_id = cursor.fetchone()[0]

    return product_id
```

### Understanding RETURNING

- PostgreSQL automatically generates the primary key because the `id` column uses `SERIAL`.
- `RETURNING id` asks PostgreSQL to return the generated ID after insertion.
- `cursor.fetchone()` retrieves the returned value as a tuple.
- `[0]` accesses the first element of that tuple.
- The function returns the generated product ID after the connection context manager exits successfully.

Example:

```python
product_id = create_product("Test Keyboard", 1500, 2)
print(product_id)
```

The function returned the newly generated ID, which was `9` during the exercise.

### Why RETURNING is safer than MAX(id) + 1

Avoid calculating the next ID manually using:

```sql
SELECT MAX(id) + 1 FROM products;
```

Reasons:

- Deleted records can leave gaps in IDs.
- Rolled-back INSERT transactions do not rewind PostgreSQL sequences.
- Concurrent operations can calculate the same next ID.

`RETURNING id` retrieves the actual ID generated by PostgreSQL for that INSERT.

## 3. Transaction Behaviour During INSERT

Verified successful and unsuccessful INSERT operations.

### Successful INSERT

- The parameterized INSERT query executes successfully.
- PostgreSQL returns the generated ID.
- The cursor context manager closes the cursor.
- The connection context manager commits the transaction and closes the connection.
- The function returns the generated ID.

### Failed INSERT

Tested inserting a product with a negative price.

PostgreSQL raised:

`psycopg.errors.CheckViolation`

The error occurred because the products table has:

```sql
CHECK (price > 0)
```

The connection context manager rolled back the failed transaction and closed the connection.

The exception propagated to the calling code, so the success return statement was not executed.

## 4. Organizing Database Tests

Created a separate `tests/` package to keep automated tests separate from database implementation code.

Project structure:

```text
fastapi-learning/
│
├── database/
│   ├── __init__.py
│   ├── connection.py
│   └── operations.py
│
├── tests/
│   ├── __init__.py
│   └── test_database.py
│
├── test_db_connection.py
├── .env
└── .gitignore
```

### Why separate tests from application code?

- `database/` contains reusable database implementation.
- `tests/` contains code that verifies database behaviour.
- This separation improves project organization and maintainability.

### Pytest test discovery

Pytest automatically discovers test files following patterns such as:

- `test_*.py`
- `*_test.py`

Test functions should begin with `test_`.

Executed tests using:

```bash
python -m pytest -v tests/test_database.py
```

Initially, running `pytest` directly produced:

`ModuleNotFoundError: No module named 'database'`

Running pytest through Python as a module resolved the import-path issue:

```bash
python -m pytest -v tests/test_database.py
```

This demonstrated the importance of the current working directory and Python's module search path when importing project packages.

## 5. Arrange–Act–Assert (AAA) Testing Pattern

Learned a common structure for writing automated tests.

1. **Arrange:** Prepare the data and conditions required for the test.
2. **Act:** Execute the function being tested.
3. **Assert:** Verify that the actual result matches the expected result.

Example:

```python
def test_get_product_by_id():
    product_id = 6

    product = get_product_by_id(product_id)

    assert product is not None
    assert product[1] == "Gaming Mouse"
```

The test checks both that a record exists and that the returned product has the expected name.

## 6. Positive and Negative Database Tests

Created tests for existing and non-existing products.

### Existing product

```python
def test_get_product_by_id():
    product_id = 6
    product = get_product_by_id(product_id)

    assert product is not None
    assert product[1] == "Gaming Mouse"
```

### Non-existing product

```python
def test_get_product_by_id_not_found():
    product_id = 9999
    product = get_product_by_id(product_id)

    assert product is None
```

Important observations:

- `fetchone()` returns a tuple when a matching record exists.
- `fetchone()` returns `None` when no matching record exists.
- A SELECT query returning no matching records is a valid database outcome, not a database exception.
- Psycopg returns tuples by default, so column values can be accessed using indexes.

For the products table:

| Index | Column |
|---|---|
| 0 | id |
| 1 | name |
| 2 | price |
| 3 | quantity |

## 7. Database Test Isolation and Cleanup

Learned why database tests should avoid modifying existing development records.

A test that repeatedly updates an existing product can permanently change its data.

A better approach is to create temporary records specifically for testing.

The test lifecycle:

1. Create a temporary product.
2. Capture its generated ID.
3. Perform the operation being tested.
4. Verify the result.
5. Delete the temporary product.

### Using finally for cleanup

```python
try:
    # Test operations
    pass

finally:
    # Cleanup operations
    pass
```

The `finally` block executes whether the preceding code succeeds or raises an exception.

This makes it useful for cleaning up temporary database records.

A cleanup operation should also check whether the temporary record was successfully created before attempting deletion:

```python
finally:
    if product_id is not None:
        delete_product_by_id(product_id)
```

Important: `finally` ensures that cleanup is attempted, but the cleanup operation itself can still fail.

## 8. Testing UPDATE Operations

Created an automated UPDATE test using a temporary product.

```python
from decimal import Decimal

def test_update_product_price():
    product_id = None

    try:
        product_id = create_product("Blade", 500.00, 8)

        message = update_product_price(product_id, 2500.00)
        assert message == "Product Updated"

        product = get_product_by_id(product_id)
        assert product[2] == Decimal("2500.00")

    finally:
        if product_id is not None:
            delete_product_by_id(product_id)
```

### What this test verifies

- A temporary product can be created.
- The generated product ID can be captured.
- The UPDATE operation returns the expected success message.
- The product's price is actually updated in PostgreSQL.
- The temporary product is deleted during cleanup.

### PostgreSQL NUMERIC and Python Decimal

The PostgreSQL price column uses `NUMERIC(10, 2)`.

Psycopg returns these values as Python `Decimal` objects by default.

Therefore, the test uses:

```python
from decimal import Decimal

assert product[2] == Decimal("2500.00")
```

This avoids comparing a database Decimal value against a Python float.

## 9. Results and Current Testing Progress

Successfully implemented and executed three database tests:

| Test | Expected behaviour | Result |
|---|---|---|
| `test_get_product_by_id` | Retrieve an existing product | Passed |
| `test_get_product_by_id_not_found` | Return `None` for a missing product | Passed |
| `test_update_product_price` | Update and verify price, then clean up | Passed |

### Concepts reinforced

- Pytest discovery and execution.
- Python package imports.
- AAA testing pattern.
- Positive and negative testing.
- Temporary database records.
- Test isolation and cleanup.
- `try` and `finally`.
- PostgreSQL `RETURNING id`.
- Python `Decimal` comparisons.


# Day 19: Pytest Fixtures and Database Test Cleanup

## 1. Completing Database CRUD Tests

Completed automated tests for the reusable PostgreSQL CRUD functions in `database/operations.py`.

The database test suite now covers:

- Retrieving an existing product.
- Handling a product ID that does not exist.
- Updating a product’s price and verifying the stored value.
- Creating a product and checking its generated ID and stored data.
- Rejecting product creation that violates a database constraint.
- Deleting a product and verifying that it no longer exists.
- Handling deletion requests for a non-existing product.

The tests use temporary product records where appropriate so they do not depend on or permanently modify existing development data.

## 2. Pytest Fixtures

A pytest fixture prepares resources or data that a test needs. A test requests a fixture by using the fixture’s name as a function parameter.

Fixtures are useful for repeated setup and cleanup logic, such as creating a temporary database record before a test and deleting it afterward.

### Fixture lifecycle

A fixture can use `yield` to separate setup from teardown:

1. Code before `yield` runs as setup.
2. The value supplied to `yield` is passed to the test.
3. The test body runs.
4. Code after `yield` runs as teardown.

If the test body fails after the fixture has yielded, pytest still resumes the fixture and runs its teardown. If fixture setup fails before reaching `yield`, the post-`yield` teardown does not run.

### Temporary product fixture

```python
@pytest.fixture
def temporary_product():
    product_id = create_product("Laptop Charger", 450.69, 40)

    yield product_id

    delete_product_by_id(product_id)
    assert get_product_by_id(product_id) is None


def test_temporary_product_exist(temporary_product):
    assert temporary_product is not None

    product = get_product_by_id(temporary_product)

    assert product is not None
    assert product[1] == "Laptop Charger"
```

The fixture creates a product, provides its generated ID to the test, then deletes the product and verifies that it is gone.

## 3. Fixture Scope and Test Isolation

Pytest fixtures have scopes that determine how often setup runs and when teardown occurs.

- `function` — once per test function; this is the default.
- `class` — once per test class.
- `module` — once per test module/file.
- `session` — once per pytest run.

For database tests that create or modify records, function scope is generally a good default because each test receives its own temporary record and cleanup runs after that test.

Broader scopes can reduce repeated setup, but they can also introduce shared-state dependencies between tests. Tests should remain independently runnable and should not rely on another test having run first.

## 4. Test Results

Ran the database tests using:

```bash
python -m pytest -v tests/test_database.py
```

Result:

```text
8 passed
```

# Day 20: Rebuilding a PostgreSQL-backed FastAPI CRUD API

### 1. Practice Goal

Rebuilt the Products API from memory to strengthen recall of the database layer, Pydantic models, route definitions, and HTTP status handling.

This was a code-review exercise in an online practice environment. The API was not executed against PostgreSQL, so this session did not verify live integration behaviour.

### 2. Database Operations

Practised reusable Psycopg functions for:

- Reading one product and returning a dictionary or `None`.
- Reading all products and returning a list of dictionaries.
- Creating a product with `INSERT ... RETURNING id`.
- Updating a product and checking `cursor.rowcount`.
- Deleting a product and checking `cursor.rowcount`.

Important: SQL placeholders and the values passed to `cursor.execute()` must be in the same order.

```python
query = "UPDATE products SET price = %s WHERE id = %s"
cursor.execute(query, (price, product_id))
```

# Day 21: Integrating PostgreSQL with FastAPI

## Goals
- Replace the in-memory expense list with PostgreSQL storage.
- Connect FastAPI endpoints to database operations.
- Verify the Expense API's CRUD operations.

## What I Learned
- How to use PostgreSQL as the persistent data store for a FastAPI application.
- How to separate database operations from route handlers.
- How to use parameterized SQL queries to pass values safely.
- How to use `RETURNING id` to retrieve the ID of a newly created record.
- How to use `cursor.rowcount` to check whether an `UPDATE` or `DELETE` affected a record.
- How to build a dynamic `UPDATE` query for PATCH requests using an allowlist of permitted fields.
- How to use `model_dump(exclude_unset=True)` to retrieve only the fields supplied in a PATCH request.
- How to return appropriate HTTP status codes for successful operations and missing records.

## Implementation
- Connected the FastAPI Expense API to PostgreSQL.
- Replaced in-memory storage with database-backed CRUD operations.
- Implemented database functions to:
  - Retrieve all expenses.
  - Retrieve an expense by ID.
  - Create an expense.
  - Replace an expense using PUT.
  - Partially update an expense using PATCH.
  - Delete an expense.
- Manually tested the API endpoints and verified their responses.

## Key Concepts

### Parameterized SQL
Used `%s` placeholders and passed values separately to `cursor.execute()` rather than inserting user input directly into SQL strings.

### PATCH Updates
Used `model_dump(exclude_unset=True)` to identify fields provided by the client. The database function updates only allowed fields.

### Database Transactions
Used the connection context manager to manage database operations and commit successful changes.

### Error Handling
- `404 Not Found` when an expense ID does not exist.
- `400 Bad Request` when a PATCH request contains no fields to update.
- `422 Unprocessable Entity` when request data fails validation.
- `204 No Content` after a successful DELETE.

## Challenges and Fixes
- Corrected the table name from `exepenses` to `expenses`.
- Removed the in-memory data store and connected the API to PostgreSQL.
- Kept database functions separate from FastAPI route handlers to make the code easier to maintain.


# Day 22 — Automated API Testing with pytest and FastAPI TestClient

## 1. Learning Objectives

- Test FastAPI endpoints automatically using `pytest`.
- Send requests to the API using FastAPI’s `TestClient`.
- Keep test data separate from development data.
- Use fixtures to prepare and clean up test data.
- Use `monkeypatch` to replace the database connection during tests.
- Verify successful responses and expected error responses.

## 2. FastAPI TestClient

`TestClient` lets us call FastAPI endpoints directly from our tests without starting a separate server.

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
```

A test can make a request and inspect the response:

```python
def test_get_expenses():
    response = client.get("/expenses")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

Useful response properties:

- `response.status_code` — the HTTP status code.
- `response.json()` — the response body parsed as Python data.

## 3. Use a Separate Test Database

Tests should not modify the development database or real application data.

A separate database was created for testing:

```env
DB_TEST_NAME=expense_test
```

The test database connection uses its own configuration. This keeps test data isolated from the development database.

## 4. Replacing the Database Connection with `monkeypatch`

`monkeypatch` is a pytest feature that temporarily replaces an object or function during a test.

In our tests, we replace the database connection used by the operations module with the test database connection:

```python
monkeypatch.setattr(
    operations,
    "get_connection",
    get_test_connection
)
```

This means database operations performed during the test use the test database instead of the development database.

The replacement applies during the test and is automatically undone by pytest afterward.

## 5. Pytest Fixtures

A fixture prepares the resources that a test needs.

Our fixture:

1. Uses the test database connection.
2. Creates test expenses.
3. Provides their IDs to the test.
4. Deletes the test expenses after the test finishes.

A fixture can provide its result to a test through its function argument:

```python
def test_get_expense_by_id(test_expenses):
    ...
```

Here, `test_expenses` is the fixture name. Pytest runs the fixture and passes its returned value into the test.

The fixture uses `yield` to separate setup from cleanup:

- Code before `yield` prepares the test data.
- The yielded value is made available to the test.
- Code after `yield` runs during cleanup.

## 6. Tests Implemented

The test suite covers the following API behavior:

### GET endpoints

- Retrieve all expenses.
- Retrieve an expense by ID.

### POST endpoint

- Create an expense successfully.
- Reject an invalid amount.
- Reject an invalid title.
- Reject an invalid category.

### DELETE endpoint

- Delete an expense successfully.
- Return `404` when trying to delete an expense that does not exist.
- Return `422` when the path parameter is not an integer.

### PATCH endpoint

- Update an expense successfully.
- Return `400` when the request body contains no fields to update.
- Return `404` when the requested expense does not exist.
- Return `422` when the path parameter is not an integer.

## 7. Important HTTP Status Codes

| Status code | Meaning | Example from our API |
|---|---|---|
| `200` | OK | A request succeeds |
| `201` | Created | An expense is created |
| `400` | Bad Request | PATCH request contains no fields to update |
| `404` | Not Found | Expense ID does not exist |
| `422` | Unprocessable Content | Path parameter or request data fails validation |

A `404` means the requested resource was not found. A `422` means the request could not pass validation.

## 8. Test Results

The automated test suite completed successfully:

```text
11 passed
```

The tests verify both successful API behavior and expected error responses.

## 9. Key Takeaways

- `TestClient` allows API endpoints to be tested without running a separate server.
- Tests should use a separate database to avoid changing development data.
- `monkeypatch` temporarily replaces the database connection used by the application.
- Fixtures help organize test setup and cleanup.
- Tests should verify status codes and response data, not just whether a request completes.
- Testing error cases is important because APIs must handle invalid input and missing resources predictably.

## 10. Next Step

Review the test fixture’s cleanup behavior, especially what happens if a test fails before reaching its assertions. Then continue improving the automated test suite.

# Day 23 — Improving API Test Cleanup

## Learning Goals

- Understand when pytest runs fixture teardown.
- Handle setup failures that occur before a fixture reaches `yield`.
- Ensure cleanup is attempted even when test assertions fail.
- Continue cleanup attempts if deleting one test record raises an exception.

## Key Concepts

### 1. Fixture Teardown with `yield`

A pytest fixture can use `yield` to provide a value to a test and separate setup from teardown.

- Code before `yield` performs fixture setup.
- The value passed to `yield` is provided to the test.
- Code after `yield` runs during teardown when the test finishes.
- If setup raises an exception before reaching `yield`, the code after `yield` does not run.

**Key takeaway:** Cleanup placed only after `yield` will not run if setup fails before the fixture reaches `yield`.

### 2. Tracking Partially Created Test Records

The fixture records each expense ID immediately after that expense is created successfully.

This prevents an expense created earlier in setup from being forgotten if a later expense creation fails before `yield`.

**Key takeaway:** Track each resource as soon as its creation succeeds, so cleanup can find resources created during partial setup.

### 3. Using `try/finally`

A `finally` block runs after the protected code finishes, including when an assertion fails.

The POST API test uses `finally` to attempt deletion of the newly created expense after its response data is available.

**Key takeaway:** Use `finally` when cleanup must be attempted regardless of whether the protected code succeeds or fails.

### 4. Handling Cleanup Errors Per Record

The fixture places `try/except` inside the cleanup loop.

If deleting one expense raises an exception, the exception is handled for that ID and the loop can continue attempting to delete the remaining records.

The exception is printed with the affected expense ID and error message.

**Important:** Catching the exception allows the loop to continue, but it does not guarantee that deletion succeeded.

## Implementation Summary

- Added a list to track successfully created fixture expense IDs.
- Added `try/finally` around fixture setup and teardown.
- Added per-expense exception handling inside the fixture cleanup loop.
- Updated the POST test to attempt cleanup even if its data assertions fail.

## Test Run

Ran the API tests using:

```powershell
py -m pytest -v test_main.py
```

**Test result:** The command was run, but the test output was not included in these notes. Add the reported pass/fail count here.

## Key Takeaways

- Fixture teardown after `yield` does not run if setup fails before reaching `yield`.
- Tracking created IDs immediately helps cleanup handle partial setup.
- `finally` ensures cleanup is attempted even when assertions fail.
- Handling cleanup errors per record allows later cleanup attempts to continue.
- An attempted deletion is not the same as a confirmed successful deletion.

## Next Step

Extract the cleanup logic into a helper and test that a simulated deletion failure does not prevent cleanup attempts for the remaining expense IDs.