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
- [ ] Python exceptions and error handling — Day 7
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

#### Project structure

```text
week-01-python/
├── expense_analyzer/
│   ├── __init__.py
│   ├── calculations.py
│   ├── filters.py
│   └── validations.py
├── main.py
├── test_expense_analyzer.py
└── notes.md
```

#### Tech stack

- Python
- `unittest`

#### Testing

The test suite currently has **19 passing tests**, covering the expense-processing functions and defensive validation in `calculate_total_safe()`.

Run the tests from the project directory:

```bash
python -m unittest test_expense_analyzer.py
```

Run the sample application:

```bash
python main.py
```

#### Learning notes

Detailed explanations, examples, mistakes, and lessons from each study session are documented here:

- [Week 1 — Python Fundamentals](week-01-python/notes.md)

## Learning Approach

- Learn one concept at a time.
- Attempt exercises independently before reviewing solutions.
- Test edge cases, not just typical inputs.
- Document mistakes and revisit weak areas.
- Refactor code without breaking existing behaviour.
- Build practical projects before moving to advanced topics.

## Current Focus

**Day 7: Python exceptions and error handling.**

The next step is to understand `try`, `except`, `else`, and `finally`, then practise handling errors before moving toward APIs, LLM integration, RAG, and production AI applications.