from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel, Field, field_validator
from database import (get_all_expenses, get_expense_by_id, create_expense,update_expense,patch_expense,delete_expense as delete_expense_db)

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

    @field_validator("title","amount","category",mode="before")
    @classmethod
    def reject_null(cls,value):
        if value is None:
            raise ValueError("Field cannot be null")
        return value
    
    @field_validator("amount", mode="before")
    @classmethod
    def validate_amount(cls, value):
        if isinstance(value, str):
            value = value.replace("₹", "").strip()
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
        return value.lower()

app = FastAPI()

@app.post("/expenses",status_code=status.HTTP_201_CREATED,response_model=ExpenseResponse)
def create_exp(expense:ExpenseCreate):
    expense_id = create_expense(expense.title,expense.amount,expense.category)
    expense_details = get_expense_by_id(expense_id)
    return expense_details

@app.get("/expenses",response_model=list[ExpenseResponse])
def get_expenses():
    expense_list = get_all_expenses()
    return expense_list

@app.get("/expenses/{expense_id}",response_model=ExpenseResponse)
def get_expense(expense_id:int):
    expense = get_expense_by_id(expense_id)
    if expense is not None:
        return expense
    raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail="Expense not found"
    )

@app.put("/expenses/{expense_id}",response_model=ExpenseResponse)
def edit_expense(expense_id:int,exp:ExpenseCreate):
    is_updated = update_expense(expense_id,exp.title,exp.amount,exp.category)
    if is_updated:
        updated_expense = get_expense_by_id(expense_id)
        return updated_expense
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"expense not found for {expense_id}"
    )
    
@app.patch("/expenses/{expense_id}",response_model=ExpenseResponse)
def update_exp(exp:ExpenseUpdate,expense_id:int):
    patched_exp = exp.model_dump(exclude_unset=True)
    if not patched_exp:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Please provide at least 1 field to update"
        )
    is_patched = patch_expense(expense_id,patched_exp)
    if is_patched:
        updated_expense = get_expense_by_id(expense_id)
        return updated_expense
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"expense not found for {expense_id}"
    )

@app.delete("/expenses/{expense_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id:int):
    is_deleted = delete_expense_db(expense_id)
    if not is_deleted:
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

  