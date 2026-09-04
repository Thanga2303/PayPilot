from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session
from dotenv import load_dotenv

import os

from google import genai 
from .database import engine, SessionLocal, Base
from .models import Expense
from .ai import(analyze_expenses,ask_paypilot,detect_overspending,create_budget_plan,generate_financial_report,
detect_anomalies,categorize_expense,calculate_financial_health
)

# =========================================================
# CREATE DATABASE TABLES
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(title="PayPilot AI API")


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# FRONTEND
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR=os.path.join(BASE_DIR,"frontend")
ENV_PATH=os.path.join(BASE_DIR,".env")
load_dotenv(os.path.join(BASE_DIR,".env"))
api_key=os.getenv("GEMINI_API_KEY")
print("Gemini key loaded:",bool(api_key))
client=genai.Client(api_key=api_key)

app.mount(
    "/frontend",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend"
)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "message": "PayPilot AI API is running 🚀"
    }


# =========================================================
# GET ALL EXPENSES
# =========================================================

@app.get("/expenses")
def get_expenses():

    db: Session = SessionLocal()

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


# =========================================================
# ADD EXPENSE
# =========================================================

@app.post("/expenses")
def add_expense(
    title: str,
    amount: float,
    category: str
):

    db: Session = SessionLocal()

    try:

        new_expense = Expense(
            title=title,
            amount=amount,
            category=category
        )

        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)

        return {
            "message": "Expense added successfully",
            "expense": {
                "id": new_expense.id,
                "title": new_expense.title,
                "amount": new_expense.amount,
                "category": new_expense.category
            }
        }

    finally:

        db.close()


# =========================================================
# DELETE EXPENSE
# =========================================================

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):

    db: Session = SessionLocal()

    try:

        expense = db.query(Expense).filter(
            Expense.id == expense_id
        ).first()

        if not expense:
            raise HTTPException(
                status_code=404,
                detail="Expense not found"
            )

        db.delete(expense)
        db.commit()

        return {
            "message": "Expense deleted successfully"
        }

    finally:

        db.close()


# =========================================================
# EDIT / UPDATE EXPENSE
# =========================================================

@app.put("/expenses/{expense_id}")
def update_expense(
    expense_id: int,
    title: str,
    amount: float,
    category: str
):

    db: Session = SessionLocal()

    try:

        expense = db.query(Expense).filter(
            Expense.id == expense_id
        ).first()

        if not expense:
            raise HTTPException(
                status_code=404,
                detail="Expense not found"
            )

        expense.title = title
        expense.amount = amount
        expense.category = category

        db.commit()
        db.refresh(expense)

        return {
            "message": "Expense updated successfully",
            "expense": {
                "id": expense.id,
                "title": expense.title,
                "amount": expense.amount,
                "category": expense.category
            }
        }

    finally:

        db.close()


# =========================================================
# 🤖 AI EXPENSE ANALYSIS
# =========================================================

@app.get("/ai/status")
def ai_status():
    return {
        "ai": "PayPilot AI",
        "status": "ready 🤖"
    }


@app.get("/ai/analyze")
def ai_analyze():
    db = SessionLocal()

    try:
        expenses = db.query(Expense).all()

        if not expenses:
            return {
                "analysis": "Add some expenses first so PayPilot AI can analyze your spending."
            }

        result = analyze_expenses(expenses)

        return {
            "analysis": result
        }

    finally:
        db.close()

# =========================================================
# 💬 ASK PAYPILOT AI
# =========================================================

@app.post("/ai/ask")
def ai_ask(question: str):

    db = SessionLocal()

    try:
        expenses = db.query(Expense).all()

        if not expenses:
            return {
                "answer": "Add some expenses first so I can help you analyze your spending."
            }

        result = ask_paypilot(question, expenses)

        return {
            "answer": result
        }

    finally:
        db.close()

# =========================================================
# ⚠️ SMART OVERSPENDING ALERT
# =========================================================

@app.get("/ai/overspending")
def ai_overspending():

    db = SessionLocal()

    try:
        expenses = db.query(Expense).all()

        if not expenses:
            return {
                "alert": "Add some expenses first so PayPilot AI can check your spending."
            }

        result = detect_overspending(expenses)

        return {
            "alert": result
        }

    except Exception as e:

        error_message = str(e)

        if "RESOURCE_EXHAUSTED" in error_message:
            return {
                "alert": "⚠️ AI temporarily unavailable.\n\nGemini's daily request limit has been reached. Please try again later."
            }

        return {
            "alert": "❌ PayPilot AI could not process the spending alert right now."
        }

    finally:
        db.close()

@app.post("/ai/budget")
def ai_budget(monthly_budget: float):
    db = SessionLocal()

    try:
        expenses = db.query(Expense).all()

        if not expenses:
            return {
                "plan": "Add some expenses first so PayPilot AI can create your budget plan."
            }

        result = create_budget_plan(expenses, monthly_budget)

        return {
            "plan": result
        }

    finally:
        db.close()

@app.get("/ai/report")
def ai_report():

    db = SessionLocal()

    try:

        expenses = db.query(Expense).all()

        if not expenses:
            return {
                "report": "Add some expenses first so PayPilot AI can generate your financial report."
            }

        result = generate_financial_report(expenses)

        return {
            "report": result
        }

    finally:
        db.close()

@app.get("/ai/anomalies")
def ai_anomalies():

    db = SessionLocal()

    try:
        expenses = db.query(Expense).all()

        if not expenses:
            return {
                "anomalies": "Add some expenses first so PayPilot AI can detect unusual spending."
            }

        result = detect_anomalies(expenses)

        return {
            "anomalies": result
        }

    finally:
        db.close()

@app.get("/ai/categorize")
def ai_categorize(title: str):

    if not title.strip():
        raise HTTPException(
            status_code=400,
            detail="Expense title is required."
        )

    result = categorize_expense(title)

    return {
        "category": result
    }

@app.get("/ai/financial-health")
def ai_financial_health():

    db = SessionLocal()

    try:
        expenses = db.query(Expense).all()

        if not expenses:
            return {
                "health": "Add some expenses first so PayPilot can calculate your financial health."
            }

        result = calculate_financial_health(expenses)

        return {
            "health": result
        }

    finally:
        db.close()