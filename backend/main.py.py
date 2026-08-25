from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles 
import os
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from models import Expense

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PayPilot API")


# ---------------- CORS ----------------

app.mount(
    "/frontend",
    StaticFiles(
        directory=os.path.join(
            os.path.dirname(__file__),
            "../frontend"
        )
    ),
    name="frontend"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- HOME ----------------

@app.get("/")
def home():
    return {
        "message": "Welcome to PayPilot!"
    }


# ---------------- HEALTH ----------------

@app.get("/health")
def health():
    return {
        "status": "OK"
    }


# ---------------- GET EXPENSES ----------------

@app.get("/expenses")
def get_expenses():

    db = SessionLocal()

    try:
        expenses = db.query(Expense).all()

        return [
            {
                "id": expense.id,
                "title": expense.title,
                "amount": expense.amount,
                "category": expense.category
            }
            for expense in expenses
        ]

    finally:
        db.close()


# ---------------- ADD EXPENSE ----------------

@app.post("/expenses")
def add_expense(
    title: str,
    amount: float,
    category: str
):

    db = SessionLocal()

    try:

        new_expense = Expense(
            title=title,
            amount=amount,
            category=category
        )

        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)

        print("ADDED:", {
            "id": new_expense.id,
            "title": new_expense.title,
            "amount": new_expense.amount,
            "category": new_expense.category
        })

        return {
            "id": new_expense.id,
            "title": new_expense.title,
            "amount": new_expense.amount,
            "category": new_expense.category
        }

    finally:
        db.close()


# ---------------- DELETE EXPENSE ----------------

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):

    db = SessionLocal()

    try:

        expense = db.query(Expense).filter(
            Expense.id == expense_id
        ).first()

        if not expense:
            return {
                "error": "Expense not found"
            }

        db.delete(expense)
        db.commit()

        return {
            "message": "Expense deleted successfully"
        }

    finally:
        db.close()


# ---------------- UPDATE EXPENSE ----------------

@app.put("/expenses/{expense_id}")
def update_expense(
    expense_id: int,
    title: str,
    amount: float,
    category: str
):

    db = SessionLocal()

    try:

        expense = db.query(Expense).filter(
            Expense.id == expense_id
        ).first()

        if not expense:
            return {
                "error": "Expense not found"
            }

        expense.title = title
        expense.amount = amount
        expense.category = category

        db.commit()
        db.refresh(expense)

        return {
            "id": expense.id,
            "title": expense.title,
            "amount": expense.amount,
            "category": expense.category
        }

    finally:
        db.close()