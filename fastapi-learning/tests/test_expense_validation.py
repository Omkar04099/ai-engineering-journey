from main import ExpenseCreate
from pydantic import ValidationError
import pytest

def test_expense_creation_valid_data():
    expense_data = {
        "title": "  Dinner  ",
        "amount": "₹350",
        "category": " FOOD "
        }
    expense = ExpenseCreate.model_validate(expense_data)
    assert expense.title == "Dinner"
    assert expense.amount == 350.0
    assert expense.category == "food"


def test_expense_creation_invalid_data():
    expense_data = {
        "title": "   ",
        "amount": -100,
        "category": "   "
    }
    with pytest.raises(ValidationError):
        ExpenseCreate.model_validate(expense_data)


def test_inspect_validation_errors():
    expense_data = {
        "title": "   ",
        "amount": -500,
        "category": "   "
    }

    with pytest.raises(ValidationError) as exc_info:
        ExpenseCreate.model_validate(expense_data)

    errs = exc_info.value.errors()
    assert len(errs) == 3
    error_fields = [err["loc"][0] for err in errs]
    assert "title" in error_fields
    assert "amount" in error_fields
    assert "category" in error_fields
