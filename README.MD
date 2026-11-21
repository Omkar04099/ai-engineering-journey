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
- [ ] Integrate PostgreSQL with the FastAPI Expense API
- [ ] Replace in-memory storage with persistent database storage
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

## Remaining Work

- Integrate the reusable PostgreSQL operations with the FastAPI Expense API.
- Replace the API’s in-memory list and ID counter with persistent database operations.
- Add and verify API-level tests for database-backed endpoints.
- Explore ORM integration after completing direct SQL integration.

## Day 19: Key Concepts Practised

- Pytest fixtures and fixture parameters
- Fixture setup and teardown using `yield`
- Fixture scopes: function, class, module, and session
- Database test isolation and temporary test records
- Why tests should not depend on execution order
- Running and verifying the database test suite with pytest

## Next Session

Begin integrating the existing PostgreSQL database layer with the FastAPI Expense API. Continue using direct SQL and Psycopg before introducing an ORM.
