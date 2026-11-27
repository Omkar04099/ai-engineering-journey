import pytest
from main import app
from fastapi.testclient import TestClient
from fastapi import status
from database import (operations, get_test_connection, create_expense, delete_expense)
import sys

@pytest.fixture
def client():
    return TestClient(app)

def cleanup_expenses(expense_ids):
    for expense_id in expense_ids:
        try:
            delete_expense(expense_id)
        except Exception as error:
            print(f"Expense deletion failed for id:{expense_id}, {error}")

attempted_ids = []
def test_cleanup_expenses(monkeypatch):
    attempted_ids = []
    expenses = [10, 20, 30]

    def fake_delete(expense_id):
        attempted_ids.append(expense_id)

        if expense_id == 20:
            raise Exception("Deletion failure")

    monkeypatch.setattr(
        sys.modules[__name__],
        "delete_expense",
        fake_delete
    )

    cleanup_expenses(expenses)

    assert attempted_ids == [10, 20, 30]

def fake_delete(attempted_id):
    attempted_ids.append(attempted_id)

    if attempted_id == 20:
        raise Exception("Deletion failure")

@pytest.fixture
def example_expense(monkeypatch):
    monkeypatch.setattr(
        operations,
        "get_connection",
        get_test_connection
    )
    created_expenses = []
    try:
        id_1 = create_expense("Test coffee", 120, "Food")
        created_expenses.append(id_1)
        id_2 = create_expense("Test book", 450, "Education")
        created_expenses.append(id_2)
        yield id_1, id_2
    finally:
        for expense_id in created_expenses:
            try:
                delete_expense(expense_id)
            except Exception as error:
                print(f"Deletion failed for expense: {expense_id}, {error}")


def test_get_expenses(client,example_expense):
    id_1,id_2 = example_expense
    
    response = client.get("/expenses")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

    expense_ids = []
    for expense in data:
        expense_ids.append(expense["id"])

    sorted_ids = sorted(expense_ids)
    assert expense_ids == sorted_ids
    assert expense_ids == [id_1,id_2]


def test_get_expense_by_id(client,example_expense):
    id_1, id_2 = example_expense
    response = client.get(f"/expenses/{id_1}")
    assert response.status_code == status.HTTP_200_OK
    response = client.get("/expenses/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_create_expense(client,example_expense):
   data = {
    "title":"Test coffee", 
    "amount":120, 
    "category":"Food" 
   }
   response = client.post("/expenses",json=data)
   assert response.status_code == status.HTTP_201_CREATED
   expense = response.json()
   try:
    assert data["title"] == expense["title"]
    assert data["amount"] == expense["amount"]
    assert data["category"].lower() == expense["category"]
   finally:
    try:
        delete_expense(expense["id"])
    except Exception as error:
        print(f"Deletion failed for test expense:{expense['id']},{error}")

def test_create_expense_invalid_amount(client,example_expense):
    data = {
        "title":"Test coffee", 
        "amount": 0, 
        "category":"food" 
        }
    response = client.post("/expenses",json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_create_expense_invalid_title(client,example_expense):
    data = {
        "title":" ", 
        "amount": 50, 
        "category":"food" 
        }
    response = client.post("/expenses",json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_create_expense_invalid_category(client,example_expense):
    data = {
        "title":"abc", 
        "amount": 50, 
        "category":" " 
        }
    response = client.post("/expenses",json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_delete_expense_by_id(client,example_expense):
    id_1, id_2 = example_expense
    response = client.delete(f"/expenses/{id_1}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = client.delete(f"/expenses/{id_1}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.delete("/expenses/anc")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_patch_update_by_id(client,example_expense):
    id_1,id_2 = example_expense
    data = {"title" : "Beast Coffee"}
    response = client.patch(f"/expenses/{id_1}", json = data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Beast Coffee"
    assert response.json()["id"] == id_1

def test_patch_update_by_id_empty_body(client,example_expense):
    id_1,id_2 = example_expense
    data = {}
    response = client.patch(f"/expenses/{id_1}", json = data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_patch_update_by_id_non_existing_id(client,example_expense):
    data = {"title" : "Beast Coffee"}
    response = client.patch("/expenses/9999", json = data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_patch_update_by_id_invalid_id(client,example_expense):
    data = {"title" : "Beast Coffee"}
    response = client.patch("/expenses/abc", json = data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT