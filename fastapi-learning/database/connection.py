from dotenv import load_dotenv
import os
import psycopg

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

def get_connection():
    return psycopg.connect(
        host = db_host,
        port = db_port,
        dbname = db_name,
        user = db_user,
        password = password
    )
