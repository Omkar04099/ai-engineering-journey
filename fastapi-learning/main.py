from fastapi import FastAPI 
from pydantic import BaseModel, Field

class Product(BaseModel):
    name:str = Field(min_length=1)
    price:float = Field(gt=0)
    quantity:int = Field(ge=0)
    in_stock:bool

class ExpenseCreate(BaseModel):
    title:str
    amount:float
    category:str

class ExpenseResponse(BaseModel):
    id:int
    title:str
    amount:float
    category:str



app = FastAPI()

@app.get("/")
def home():
    return {"message":"Welcome to my first FastAPI application"}

@app.get("/about")
def about():
    return {
        "project":"FastAPI Learning", 
        "developer":"Omkar", 
        "purpose":"Learning backend development"
    }

@app.get("/users/{user_id}")
def get_user(user_id:int):
    return {
        "user_id":user_id,
        "message":"User details fetched successfully"
    }

@app.get("/products/search")
def search_products(keyword:str,category:str="all",limit:int=10):
    return {
        "keyword":keyword,
        "category":category,
        "limit":limit
    }

@app.get("/products/{product_id}")
def get_product(product_id:int):
    return {
        "product_id": product_id,
        "product_name":"Laptop",
        "price":55000
    }


@app.get("/products")
def list_products(category:str, limit:int=10):
    return {
        "category":category,
        "limit":limit,
        "message":"Products fetched successfully"
    }

@app.post("/products/create")
def create_product(product:Product):
    return {
        "name":product.name,
        "price":product.price,
        "quantity":product.quantity,
        "in_stock":product.in_stock
    }

@app.get("/expenses/{expense_id}",response_model=ExpenseResponse)
def expense_response(expense_id:int):
    return {
        "id": expense_id,
        "title": expense.title,
        "amount": expense.amount,
        "category": expense.category,
        "created_by": "Admin 123",
        "is_deleted": True
    }