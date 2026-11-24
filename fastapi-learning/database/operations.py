from .connection import get_connection
from psycopg.rows import dict_row

def get_all_expenses():
    query = """SELECT id, title, amount, category FROM expenses ORDER BY id ASC"""
    with get_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query)
            expense_list = cursor.fetchall()
    return expense_list

def get_expense_by_id(expense_id):
    query = """SELECT id, title, amount, category FROM expenses WHERE id = %s"""
    with get_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query,(expense_id,))
            expense = cursor.fetchone()
    return expense

def create_expense(expense_title,expense_amount,expense_category):
    query = """INSERT INTO expenses (title, amount, category) VALUES (%s, %s, %s) RETURNING id"""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query,(expense_title, expense_amount, expense_category))
            expense_id = cursor.fetchone()[0]
            return expense_id

def update_expense(expense_id,expense_title,expense_amount,expense_category):
    query = """UPDATE expenses SET title = %s, amount = %s, category = %s WHERE id = %s"""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query,(expense_title,expense_amount,expense_category,expense_id))
            affected_rows = cursor.rowcount
            if affected_rows > 0:
                return True
            return False

def patch_expense(expense_id, updates):
    if not updates:
        return False

    allowed_fields = {"title", "amount", "category"}
    for key in updates:
        if key not in allowed_fields:
            return False

    assignments = []
    values = []

    for key in updates:
        assignments.append(f"{key} = %s")
        values.append(updates[key])

    set_clause = ", ".join(assignments)
    query_values = tuple(values) + (expense_id,)

    query = f"UPDATE expenses SET {set_clause} WHERE id = %s"

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, query_values)
            return cursor.rowcount > 0



def delete_expense(expense_id):
    query = """DELETE FROM expenses WHERE id = %s"""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query,(expense_id,))
            return cursor.rowcount > 0