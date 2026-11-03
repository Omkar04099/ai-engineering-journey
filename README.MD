# AI Engineering Journey

My journey from React development toward AI engineering through structured learning, hands-on projects, and continuous practice.

I'm focusing on strong programming fundamentals, deep understanding, and practical skills for building real-world AI applications.

## Roadmap

- [x] Python fundamentals: lists, dictionaries, loops, and functions — Day 1
- [x] Filtering, aggregation, and copying — Day 2
- [x] Dictionary-based data processing — Day 3
- [x] Automated testing with `assert` and `unittest` — Day 4
- [x] Input validation and defensive programming — Day 5
- [x] Python modules, packages, imports, and project structure — Day 6
- [x] Python exceptions and error handling — Day 7
- [x] Python file handling, JSON, persistence, and persistence tests — Day 8
- [x] Temporary files, test setup/cleanup, exception assertions, and JSON data validation — Day 9
- [x] Strict expense validation, non-finite number handling, and integration testing — Day 10
- [ ] FastAPI and REST APIs
- [ ] Databases and backend integration
- [ ] LLM fundamentals and API integration
- [ ] Embeddings, vector search, and Retrieval-Augmented Generation (RAG)
- [ ] AI agents and workflow orchestration
- [ ] Production deployment, evaluation, and interview preparation

## Projects

### Expense Analyzer

A Python project for practising core programming concepts by processing expense and order records.

#### Features and concepts practised

- Filtering expenses by category
- Calculating category-wise totals and counts
- Generating category summaries
- Counting occurrences with dictionaries
- Grouping records by category
- Aggregating product quantities
- Handling empty inputs and edge cases
- Understanding references, shallow copies, and deep copies
- Writing automated tests for expected behaviour and edge cases
- Validating input types, required dictionary keys, and expense amounts
- Skipping invalid records with `continue`
- Organizing functions into modules based on responsibility
- Using a package and explicit imports to structure the code
- Separating reusable logic from application execution
- Using `if __name__ == "__main__":` to guard the application entry point
- Testing the project after refactoring
- Handling expected exceptions with `try`, `except`, `else`, and `finally`
- Distinguishing `TypeError`, `ValueError`, and `KeyError`
- Reading and writing files with context managers
- Serializing and deserializing JSON with `json.dump()`, `json.load()`, `json.dumps()`, and `json.loads()`
- Persisting expense records between program executions
- Handling missing files and malformed JSON
- Testing persistence behaviour with `unittest`
- Creating temporary files with `tempfile.NamedTemporaryFile()`
- Cleaning up temporary files with `try...finally`
- Using `setUp()` and `tearDown()` to isolate test setup and cleanup
- Testing expected exceptions with `assertRaises()` and `assertRaisesRegex()`
- Validating JSON root types and individual expense records
- Rejecting Boolean values when validating numeric amounts
- Handling NaN and positive/negative infinity with `math.isfinite()`
- Validating every expense record using `all()` and a generator expression
- Understanding short-circuit evaluation

#### Tech stack

- Python
- `unittest`
- JSON
- `tempfile`

#### Testing

Run commands from the Python project directory.

Core Expense Analyzer tests:

```bash
python -m unittest test_expense_analyzer.py -v
```

Persistence tests:

```bash
python -m unittest test_persistent_expense_analyzer.py -v
```

All discoverable tests in the directory:

```bash
python -m unittest discover -v
```

Run the sample application:

```bash
python main.py
```

Note: `main.py` currently adds a utilities expense each time it runs. Repeated runs therefore increase the number of records in `expenses.json`. Be mindful when running it repeatedly.

**Latest test result:** All 19 persistence and validation tests passed.

#### Current status and next step

Completed through Day 10: Python fundamentals, testing, exceptions, JSON persistence, temporary files, strict expense validation, and integration testing.

**Next session:** Introduction to FastAPI — understand what FastAPI is, why it is used, how it compares with Flask, and build the first basic API endpoint.

## Learning Approach

- Learn one concept at a time.
- Attempt exercises independently before reviewing solutions.
- Test edge cases, not just typical inputs.
- Document mistakes and revisit weak areas.
- Refactor code without breaking existing behaviour.
- Build practical projects before moving to advanced topics.
- Aim for two hours per study day; if a session runs longer, stop and resume later rather than adding unnecessary scope.

## Current Focus

**Completed:** Day 10 — strict expense validation, non-finite number handling, and integration testing. All 19 tests passed.

**Next:** Day 11 — Introduction to FastAPI and building the first basic API endpoint.