from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel, Field, field_validator

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
def expense_response(expense_id:int):
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

