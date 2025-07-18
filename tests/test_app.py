# tests/test_app.py
from fastapi.testclient import TestClient
from backend.main import app # Adjust if your file isn't named main.py

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.text

def test_add_expense():
    response = client.post("/add", json={
        "amount": 50.0,
        "category": "Groceries",
        "date": "2025-07-16",
        "description": "Fruits"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Expense added successfully"

def test_get_expenses():
    response = client.get("/expenses")
    assert response.status_code == 200
    assert isinstance(response.json()["expenses"], list)
