from .connection import get_connection

def get_product_by_id(product_id):
    query = """SELECT * FROM products WHERE id = %s"""
    with get_connection() as connection:
        with connection.cursor() as cursor:
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
                return f"Product not found for product_id: {product_id}"
            return "Product Updated"

def delete_product_by_id(product_id):
    query = """DELETE FROM products WHERE id = %s"""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query,(product_id,))
            affected_rows = cursor.rowcount
            if affected_rows == 0:
                return f"Product not found with product_id: {product_id}"
            return "Product deleted successfully"