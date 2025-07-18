from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import os
import json
from collections import defaultdict

app = FastAPI()

# ✅ Use local path since expenses.json is in the same folder as main.py
DATA_FILE = os.path.join(os.path.dirname(__file__), "expenses.json")

# Pydantic model for validation
class Expense(BaseModel):
    amount: float
    category: str
    date: str  # ISO format string like "2025-07-01 12:45:00"
    description: str = ""

# Load all expenses
def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Save a new expense
def save_expense(new_expense):
    expenses = load_expenses()
    expenses.append(new_expense)
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)

# Routes

@app.get("/")
def home():
    return {"message": "📊 Welcome to your personal expense tracker API!"}

@app.get("/expenses")
def get_all_expenses():
    return load_expenses()

@app.get("/expenses/category/{category}")
def get_expenses_by_category(category: str):
    expenses = load_expenses()
    filtered = [e for e in expenses if e["category"].lower() == category.lower()]
    if not filtered:
        raise HTTPException(status_code=404, detail="No expenses found for this category.")
    return filtered

@app.get("/expenses/total")
def get_total_expense():
    expenses = load_expenses()
    total = sum(e["amount"] for e in expenses)
    return {"total": total}

@app.get("/expenses/daily")
def get_daily_expense():
    expenses = load_expenses()
    daily_totals = defaultdict(float)
    for e in expenses:
        date_only = e["date"].split()[0]
        daily_totals[date_only] += e["amount"]
    return dict(daily_totals)

@app.get("/expenses/summary")
def get_summary():
    expenses = load_expenses()
    summary = defaultdict(float)
    for e in expenses:
        summary[e["category"]] += e["amount"]
    return dict(summary)

@app.post("/add")
def add_expense(expense: Expense):
    expense_dict = expense.dict()
    save_expense(expense_dict)
    return {"message": "✅ Expense added successfully!"}
