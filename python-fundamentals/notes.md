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

### 10. Important Lessons

- Primary keys uniquely identify records.
- Foreign keys establish relationships between tables.
- Foreign-key values can repeat.
- Composite primary keys enforce uniqueness across a combination of columns.
- SQL CRUD operations are fundamental to database interaction.
- WHERE conditions control which records are affected.
- ORDER BY determines sorting direction.
- LIMIT and OFFSET support pagination.
- PostgreSQL string comparisons using ordinary equality are case-sensitive.
- DELETE and TRUNCATE both remove rows, but serve different purposes.

### Progress

- [x] Day 15: Database fundamentals, primary and foreign keys, composite keys, referential actions, and SQL CRUD operations.

### Next Step

Continue with PostgreSQL integration with FastAPI, replacing the existing in-memory expense storage with persistent database storage.