from .connection import get_connection
from psycopg.rows import dict_row

def get_all_products():
    query = """SELECT * FROM products ORDER BY id DESC"""
    with get_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query)
            products = cursor.fetchall()
            return products

def get_product_by_id(product_id):
    query = """SELECT * FROM products WHERE id = %s"""
    with get_connection() as connection:
        with connection.cursor(row_factory = dict_row) as cursor:
            cursor.execute(query,(product_id,))
            product = cursor.fetchone()
            return product

def update_product_price(product_id,new_price):
    query = """UPDATE products SET price = %s WHERE id = %s"""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query,(new_price,product_id))
            affected_rows = cursor.rowcount
            if affected_rows == 0:
                return False
    return True

def delete_product_by_id(product_id):
    query = """DELETE FROM products WHERE id = %s"""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query,(product_id,))
            affected_rows = cursor.rowcount
            if affected_rows == 0:
                return False
    return True


def create_product(product_name,product_price,product_quantity):
    query = """INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s) RETURNING id"""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query,(product_name,product_price,product_quantity))
            product_id = cursor.fetchone()[0]
    return product_id