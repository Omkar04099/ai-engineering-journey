from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel, Field, field_validator
from database import (get_product_by_id, get_all_products, create_product, update_product_price, delete_product_by_id)
from decimal import Decimal

class Product(BaseModel):
    name:str = Field(min_length=1)
    price:float = Field(gt=0)
    quantity:int = Field(ge=0)
    in_stock:bool

class ExpenseCreate(BaseModel):
    title:str
    amount:float = Field(gt=0)
    category:str

    @field_validator("amount",mode="before")
    @classmethod
    def validate_amount(cls,value):
        if isinstance(value,str):
            value = value.replace("₹","").strip()
        return value
        
    @field_validator("title")
    @classmethod
    def validate_title(cls,value):
        value = value.strip()
        if not value:
            raise ValueError("title cannot be empty")
        return value

        

    @field_validator("category")
    @classmethod
    def validate_category(cls,value):
        value = value.strip()

        if not value:
            raise ValueError("category cannot be empty")
        
        value = value.lower()
        return value

class ExpenseResponse(BaseModel):
    id:int
    title:str
    amount:float
    category:str

class ExpenseUpdate(BaseModel):
    title: str | None = None
    amount: float | None = Field(default=None,gt=0)
    category: str | None = None

class ProductResponse(BaseModel):
    id:int
    name:str
    price:Decimal
    quantity:int

class ProductCreate(BaseModel):
    name:str = Field(min_length=1)
    price:Decimal = Field(gt=0)
    quantity:int = Field(gt=0)

    @field_validator("name")
    @classmethod
    def validate_title(cls,value):
        value = value.strip()
        if not value:
            raise ValueError("name cannot be empty")
        return value

class ProductPriceUpdate(BaseModel):
    price:Decimal = Field(gt=0)


expenses = []
next_expense_id = 1


app = FastAPI()

@app.post("/expenses",status_code=status.HTTP_201_CREATED,response_model=ExpenseResponse)
def create_expense(expense:ExpenseCreate):
    global next_expense_id
    id = next_expense_id
    curr_expense = expense.model_dump()
    curr_expense["id"] = id
    expenses.append(curr_expense)
    next_expense_id +=1
    return {
        "id": id,
        "title": expense.title,
        "amount":expense.amount,
        "category":expense.category
    }

@app.get("/expenses",response_model=list[ExpenseResponse])
def get_expenses():
    return expenses

@app.get("/expenses/{expense_id}",response_model=ExpenseResponse)
def expense_expense_by_id(expense_id:int):
    for expense in expenses:
        if expense["id"] == expense_id:
            return expense
    raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail="Expense not found"
    )

@app.put("/expenses/{expense_id}",response_model=ExpenseResponse)
def edit_expense(expense_id:int,exp:ExpenseCreate):
    for expense in expenses:
        if expense["id"] == expense_id:
            original_id = expense["id"]
            expense.update(exp.model_dump())
            expense["id"] = original_id
            return expense
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"expense not found for {expense_id}"
    )
    
@app.patch("/expenses/{expense_id}",response_model=ExpenseResponse)
def update_expense(exp:ExpenseUpdate,expense_id:int):
    for expense in expenses:
        if expense["id"] == expense_id:
            expense.update(exp.model_dump(exclude_unset=True))
            return expense
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"expense not found for {expense_id}"
    )

@app.delete("/expenses/{expense_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id:int):
    for expense in expenses:
        if expense["id"] == expense_id:
            expenses.remove(expense)
            return
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail=f"expense not found for {expense_id}"
    )

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




@app.get("/products/{product_id}",response_model=ProductResponse)
def get_product(product_id:int):
    product = get_product_by_id(product_id)
    if product is not None:
        return product
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = f"Product not found with id: {product_id}"
    )

@app.get("/products", response_model=list[ProductResponse])
def get_products():
    products = get_all_products()
    return products

@app.post("/products/create", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_prod(product:ProductCreate):
    product_id = create_product(product.name,product.price,product.quantity)
    product_details = get_product_by_id(product_id)
    return product_details
    

@app.patch("/products/{product_id}",response_model=ProductResponse)
def update_product_p(product_id:int,product:ProductPriceUpdate):
    is_product_updated = update_product_price(product_id,product.price)
    if is_product_updated:
        product_details = get_product_by_id(product_id)
        return product_details
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = f"Product not found for id: {product_id}"
    )

@app.delete("/products/{product_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id:int):
    is_deleted = delete_product_by_id(product_id)
    if not is_deleted:    
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Product not found with id: {product_id}"
        )