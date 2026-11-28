## Learning Progress

### Phase 1: Python Fundamentals

- [x] Days 1–3: Python data structures, functions, loops, and data processing
- [x] Day 4: Automated testing with `unittest`
- [x] Day 5: Input validation and defensive programming
- [x] Day 6: Modules, packages, and project structure
- [x] Day 7: Exception handling
- [x] Day 8: File handling and JSON persistence
- [x] Day 9: Temporary files and testing practices
- [x] Day 10: Numeric validation and integration testing


## Phase 2: FastAPI and Backend Development

- [x] Days 11–14: FastAPI fundamentals, REST APIs, Pydantic validation, and pytest
- [x] Days 15–17: SQL, PostgreSQL setup, Psycopg connectivity, transactions, and reusable database operations
- [x] Day 18: Completed PostgreSQL CRUD functions, generated ID retrieval, and initial database tests
- [x] Day 19: Completed database CRUD tests and practised pytest fixtures, teardown, and test isolation
- [x] Day 20: Rebuilt PostgreSQL-backed Products API CRUD routes from memory and reviewed request/response models, validation, and HTTP status codes
- [x] Day 21: Integrated PostgreSQL with the FastAPI Expense API, replaced in-memory storage, and manually verified CRUD endpoints
- [x] Day 22: Added API-level tests for database-backed Expense endpoints using pytest and FastAPI TestClient
- [x] Day 23: Improved API test cleanup using try/finally, tracked partially created test records, and handled individual deletion errors
- [x] Day 24: Used monkeypatch to simulate a deletion failure and verified that cleanup continues for remaining records
- [x] Day 25: Learned ORM fundamentals, ORM models, object persistence, transactions, and the difference between ORM operations and direct SQL
- [ ] ORM integration

## Current Database Progress

- Created the local PostgreSQL database `expense_tracker_db` and the `products` table.
- Established Python-to-PostgreSQL connectivity using Psycopg 3.
- Configured database credentials through `.env` and `python-dotenv`.
- Implemented reusable CREATE, READ, UPDATE, and DELETE operations in `database/operations.py`.
- Used PostgreSQL `RETURNING id` to retrieve generated product IDs.
- Used parameterized SQL queries, transaction handling, and Psycopg context managers.
- Organized database code into a package with `connection.py`, `operations.py`, and package-level exports.
- Created a separate `tests/` package for database tests.
- Added tests for successful and unsuccessful product retrieval, creation, updating, and deletion.
- Used temporary database records to avoid modifying existing development data.
- Added a pytest fixture that creates a temporary product, provides its ID to a test, and removes the product during teardown.
- Verified the database test suite: **8 passed**.
- Recreated the Products API database operations and Pydantic models from memory.
- Practised GET-all, GET-by-ID, POST, PATCH, and DELETE routes using the reusable Psycopg operations.
- Reviewed request validation, `response_model`, `201 Created`, `204 No Content`, `404 Not Found`, and automatic `422` validation errors.
- Reviewed route-to-database argument order and handling missing records with `cursor.rowcount`.
- Integrated the reusable PostgreSQL operations with the FastAPI Expense API.
- Replaced the Expense API's in-memory list and ID counter with PostgreSQL persistence.
- Implemented database-backed GET-all, GET-by-ID, POST, PUT, PATCH, and DELETE expense endpoints.
- Used `model_dump(exclude_unset=True)` to update only fields supplied in PATCH requests.
- Added PATCH validation for null values, blank titles/categories, positive amounts, and rupee-prefixed amount strings.
- Used an allowlist for dynamic PATCH column names and parameterized SQL for values.
- Handled empty PATCH requests with `400 Bad Request` and missing expense IDs with `404 Not Found`.
- Verified the CRUD flow manually, including successful operations and expected error responses.
- Renamed the mistakenly named PostgreSQL table to `expenses`.
- Created a separate PostgreSQL test database for API-level tests.
- Used pytest fixtures to create test expenses and clean them up after tests.
- Used `monkeypatch` to redirect database operations to the test database during tests.
- Tested FastAPI endpoints with `TestClient`, including successful CRUD operations, validation failures, missing resources, and invalid path parameters.
- Verified the API test suite after adding the cleanup failure test: **12 passed**.
- Improved API test fixture cleanup by tracking each successfully created expense ID immediately.
- Used `try/finally` so cleanup is attempted even when test assertions fail.
- Added per-expense `try/except` handling so one deletion error does not stop cleanup attempts for remaining IDs.
- Updated the POST API test to attempt cleanup of its created expense even if a data assertion fails.
- Reviewed how an ORM maps Python classes to database tables, objects to rows, and attributes to columns.
- Compared direct SQL operations with ORM-based database access.
- Reviewed how ORM sessions manage pending changes and how `commit()` persists a transaction.
- Clarified that uncommitted changes are not guaranteed to persist and may be rolled back.
- Practised a PostgreSQL `SELECT` query to retrieve an expense by ID.
- Confirmed the API test suite after the cleanup failure test: **12 passed**.

## Remaining Work

- Improve API test isolation and cleanup reporting where needed.
- Explore ORM integration after completing direct SQL integration.

## Day 19: Key Concepts Practised

- Pytest fixtures and fixture parameters
- Fixture setup and teardown using `yield`
- Fixture scopes: function, class, module, and session
- Database test isolation and temporary test records
- Why tests should not depend on execution order
- Running and verifying the database test suite with pytest

**Next Session:** Begin ORM integration. Choose the ORM for the Expense API, install and configure it, and create the first ORM model.