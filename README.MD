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

### Phase 2: FastAPI and Backend Development

- [x] Day 11: Introduction to FastAPI and building the first API
- [x] Day 12: HTTP methods, status codes, Pydantic request and response models
- [x] Day 13: Implementing CRUD operations, HTTP exceptions, and stable ID generation
- [x] Day 14: Pydantic validators, validation errors, pytest, and regex fundamentals
- [x] Day 15: Database fundamentals, SQL, primary and foreign keys, and CRUD queries
- [ ] Day 16: PostgreSQL integration with FastAPI
- [ ] PostgreSQL and ORM integration


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

The next stage will introduce databases and persistent storage.

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