# AI Engineering Journey

My journey from React development toward AI engineering through
structured learning, hands-on projects, and continuous practice.

I'm focusing on strong programming fundamentals, deep understanding, and
practical skills for building real-world AI applications.

## Roadmap

-   [x] Python fundamentals: Days 1--2
-   [x] Dictionaries, data processing, and copying: Day 3
-   [x] Automated testing with `assert` and `unittest`: Day 4
-   [x] Error handling and defensive programming: Day 5
-   [ ] Python modules and project structure: Day 6
-   [ ] FastAPI and REST APIs
-   [ ] Databases and backend integration
-   [ ] LLM fundamentals and API integration
-   [ ] Embeddings, vector search, and Retrieval-Augmented Generation
    (RAG)
-   [ ] AI agents and workflow orchestration
-   [ ] Production deployment, evaluation, and interview preparation

## Projects

### Expense Analyzer

A Python project for practicing core programming concepts by processing
expense and order records.

**Features and concepts practiced**

-   Filtering expenses by category
-   Calculating category-wise totals and counts
-   Generating category summaries
-   Counting occurrences with dictionaries
-   Grouping records by category
-   Aggregating product quantities
-   Handling empty inputs and edge cases
-   Understanding references, shallow copies, and deep copies
-   Writing automated tests for expected behavior and edge cases
-   Validating input types, required dictionary keys, and expense
    amounts
-   Skipping invalid records with `continue`
-   Using `unittest` to test defensive behavior

**Tech stack:** Python, `unittest`

**Testing:** The test suite currently has 19 passing tests, including
tests for the original expense functions and defensive validation in
`calculate_total_safe()`.

Run the tests from the project directory:

``` bash
python -m unittest test_expense_analyzer.py
```

## Learning Notes

-   [Week 1 --- Python Fundamentals](week-01-python/notes.md)

The notes capture key concepts, code examples, mistakes, and lessons
from hands-on practice.

## Learning Approach

-   Learn one concept at a time.
-   Attempt exercises independently before reviewing solutions.
-   Test edge cases, not just typical inputs.
-   Document mistakes and revisit weak areas.
-   Build practical projects before moving to advanced topics.

## Current Focus

**Python modules, imports, and project structure.**

The goal is to build a reliable foundation before moving into APIs, LLM
integration, RAG, and production AI applications.
