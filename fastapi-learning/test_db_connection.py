from dotenv import load_dotenv
import os
import psycopg

load_dotenv()

password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")

connection = psycopg.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=password
)

cursor = connection.cursor()

cursor.execute("SELECT * FROM products")

products = cursor.fetchall()

product_name = "Wireless Headphones"
product_price = 1999.50
product_quantity = 5

query = """
INSERT INTO products (name, price, quantity)
VALUES (%s, %s, %s)
"""

cursor.execute(
    query,
    (product_name, product_price, product_quantity)
)

connection.commit()

print("Product inserted successfully!")

cursor.close()
connection.close()
