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

- [x] Day 11: Introduction to FastAPI and building the first API
- [x] Day 12: HTTP methods, status codes, Pydantic request and response models
- [x] Day 13: Implementing CRUD operations, HTTP exceptions, and stable ID generation
- [x] Day 14: Pydantic validators, validation errors, pytest, and regex fundamentals
- [x] Day 15: Database fundamentals, SQL, primary and foreign keys, and CRUD queries
- [x] Day 16: PostgreSQL setup, table creation, constraints, Psycopg connections, and parameterized queries
- [x] Day 17: PostgreSQL transactions, error handling, Psycopg CRUD operations, context managers, and database module organization
- [x] Day 18: Completing the reusable PostgreSQL CRUD module, generated ID retrieval, pytest database testing, and test cleanup
- [ ] FastAPI and PostgreSQL integration
- [ ] ORM integration


## FastAPI Learning Project

Built an Expense Management REST API using FastAPI and Pydantic.

### Implemented Features

- Create expenses using POST.
- Retrieve all expenses using GET.
- Retrieve an individual expense by ID.
- Replace an existing expense using PUT.
- Partially update expenses using PATCH.
- Delete expenses using DELETE.
- Validate request data using Pydantic models.
- Return appropriate HTTP status codes.
- Handle missing resources using `HTTPException`.
- Generate unique IDs using a separate counter.
- Apply custom field validation using Pydantic `field_validator`.
- Normalize incoming title and category values.
- Preprocess currency-formatted amount strings before numeric validation.
- Test Pydantic validation behaviour using pytest.

### Concepts Practised

- REST API fundamentals
- HTTP methods and status codes
- Path parameters and query parameters
- Pydantic `BaseModel` and `Field`
- Request models and response models
- `model_dump()` and `exclude_unset=True`
- FastAPI automatic API documentation
- Python mutable objects and variable scope
- In-memory data storage
- Pydantic `field_validator` with before and after modes
- Pydantic `ValidationError` and structured error details
- Pytest fundamentals and exception assertions
- Python regular expressions using the `re` module
- Regex character classes, quantifiers, grouping, and alternation
- Indian numbering-system comma grouping validation
- Relational database fundamentals
- SQL tables, rows, and columns
- Primary keys and foreign keys
- Composite primary keys
- Foreign key constraints and referential integrity
- ON DELETE CASCADE, RESTRICT, and SET NULL
- SQL INSERT, SELECT, UPDATE, and DELETE
- WHERE conditions with AND and OR
- ORDER BY, ASC, and DESC
- LIMIT and OFFSET
- COUNT() aggregate function
- PostgreSQL database and table setup
- SQL DDL and DML
- PostgreSQL data types: INTEGER, VARCHAR, NUMERIC, and SERIAL
- PRIMARY KEY, NOT NULL, CHECK, and DEFAULT constraints
- PostgreSQL sequences and nextval()
- Inspecting table metadata using information_schema
- Psycopg 3 installation and database connectivity
- Database connections and cursors
- Executing SQL queries using cursor.execute()
- Retrieving records using fetchone() and fetchall()
- PostgreSQL NUMERIC and Python Decimal
- Environment variable management using .env and python-dotenv
- Reading environment variables using os.getenv()
- Parameterized SQL queries using %s placeholders
- SQL injection risks and prevention
- Database transactions and connection.commit()
- PostgreSQL transaction lifecycle and transaction boundaries
- Python try, except, else, and finally with database operations
- Psycopg database exception handling using psycopg.Error
- connection.rollback() and handling failed transactions
- PostgreSQL transaction atomicity
- Understanding why SERIAL sequence values can have gaps after failed inserts or deletions
- Retrieving individual records using SELECT and WHERE
- Handling missing records using fetchone() and None
- Updating records using parameterized UPDATE queries
- Deleting records using parameterized DELETE queries
- Detecting affected records using cursor.rowcount
- Understanding why UPDATE and DELETE can succeed while affecting zero rows
- Psycopg cursor context managers
- Psycopg connection context managers
- Automatic transaction commit and rollback using connection context managers
- Automatic cursor and connection lifecycle management
- Creating reusable database connection functions
- Python modules and packages for database organization
- Relative imports within Python packages
- Exposing package functions through __init__.py
- Separating database connection logic from database operations
- Single Responsibility Principle (SRP) and separation of concerns
- Debugging parameterized SQL queries and matching placeholder order with parameter values
### Additional Concepts Practised — Day 18

- Completing reusable database CRUD operations using Psycopg
- Implementing INSERT operations inside a reusable database module
- PostgreSQL `RETURNING` clause
- Retrieving automatically generated primary keys using `RETURNING id`
- Fetching generated IDs using `cursor.fetchone()[0]`
- Understanding why `RETURNING id` is safer than calculating IDs using `MAX(id) + 1`
- Understanding transaction commit before returning successful operation results
- Pytest test discovery and execution using `python -m pytest`
- Pytest test file naming conventions: `test_*.py`
- Organizing database tests in a separate `tests/` package
- Arrange–Act–Assert (AAA) testing pattern
- Positive testing and negative testing
- Testing existing and non-existing database records
- Verifying database operation results using assertions
- Testing UPDATE operations with temporary database records
- Database test isolation and repeatability
- Using `try` and `finally` for test cleanup
- Protecting cleanup operations when test data creation fails
- Comparing PostgreSQL `NUMERIC` values using Python `Decimal`
- Understanding Python import paths when running pytest
- Using `python -m pytest` to execute tests from the project root

### Current Limitations

The Expense API currently uses an in-memory Python list.

This means:
- Data is lost when the application restarts.
- The global ID counter resets when the application restarts.
- In-memory storage is not suitable for concurrent production workloads.
- Indian currency grouping validation has been practised independently
  but is not yet integrated into the Expense API's Pydantic validation.
- Decimal currency input and currency-symbol handling still need
  complete integration and testing.

PostgreSQL learning and database setup have started separately from the FastAPI application.

PostgreSQL learning and database setup have started separately from the FastAPI application.

**Current database progress:**

- Created a local PostgreSQL database named `expense_tracker_db`.
- Created a `products` table with appropriate data types and constraints.
- Practised inserting and retrieving records using pgAdmin.
- Established Python-to-PostgreSQL connectivity using Psycopg 3.
- Configured database credentials using `.env` and `python-dotenv`.
- Executed parameterized SQL queries from Python.
- Practised transaction commits, failed transactions, and rollback.
- Implemented all four CRUD operations in `database/operations.py`:
  - `create_product()`
  - `get_product_by_id()`
  - `update_product_price()`
  - `delete_product_by_id()`
- Used PostgreSQL `RETURNING id` to retrieve automatically generated product IDs.
- Used `fetchone()` and `cursor.rowcount` to handle retrieved and affected records.
- Practised exception handling using `try`, `except`, and `finally`.
- Used cursor and connection context managers for resource and transaction management.
- Created a reusable database connection function.
- Organized database code into a Python package containing `connection.py` and `operations.py`.
- Used relative imports and package-level exports through `__init__.py`.
- Created a separate `tests/` package for database tests.
- Added pytest tests for retrieving existing and non-existing products.
- Added an UPDATE test using temporary product data and cleanup through `finally`.
- Verified three database tests successfully.

**Remaining work:**

- Add automated tests for successful and failed product creation.
- Add automated tests for successful deletion and deletion of non-existing records.
- Improve database test isolation and reliability.
- Integrate PostgreSQL with the FastAPI Expense API.
- Replace in-memory storage with persistent database storage.
- Explore ORM integration after understanding direct SQL operations.



## Learning Philosophy

This journey focuses on understanding concepts before implementation.

Each learning session follows this approach:

1. Understand the concept.
2. Learn why it is needed.
3. Explore a simple example.
4. Apply it to a practical project.
5. Attempt exercises independently.
6. Review code and test understanding.

**Goal:** Build strong AI engineering fundamentals and transition from React development to AI engineering.