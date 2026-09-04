# 💳 PayPilot

### AI-Powered Personal Finance Controller

PayPilot is an AI-powered expense management and financial intelligence application that helps users understand their spending, detect potential overspending, create budgets, and receive personalized financial insights.

Instead of simply recording expenses, PayPilot uses AI to turn expense data into actionable financial recommendations.

---

## 🚀 Features

### 📊 Expense Management
- Add, edit and delete expenses
- Track expense title, amount and category
- Search expenses
- View total, average and highest expenses

### 📈 Spending Analytics
- Spending breakdown by category
- Visual spending chart
- Recent expense history
- Automatic spending statistics

### 🤖 PayPilot AI

PayPilot integrates Google's Gemini AI to provide intelligent financial assistance.

#### 🧠 AI Spending Analysis
Analyzes expenses and provides:
- Spending summary
- Highest spending category
- Potential overspending areas
- Saving suggestions
- Budget recommendations

#### 💬 Ask PayPilot AI
Users can ask natural-language questions about their spending and receive personalized answers.

Example:

> Where am I spending the most?

#### ⚠️ Smart Overspending Detection
AI analyzes spending patterns and highlights potential overspending with practical recommendations.

#### 🎯 AI Budget Planner
Generates a personalized monthly budget based on:
- Current expenses
- Monthly budget
- Spending categories
- Savings goals

#### 📊 AI Financial Report
Generates an AI-powered financial report based on the user's expense data.

#### 🏷️ AI Expense Categorization
Automatically categorizes expenses using AI.

Example:

`Uber ride to college` → `Transport`

#### ❤️ Financial Health Score
PayPilot evaluates spending behavior and generates a Financial Health Score from 0–100 with recommendations.

#### 🔎 Anomaly Detection
Identifies unusual spending patterns that may require attention.

---

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite

### AI
- Google Gemini API
- `google-genai`

### Development
- Visual Studio Code
- Git
- GitHub

---

## 🏗️ Architecture

```text
                ┌─────────────────────┐
                │     PayPilot UI     │
                │   HTML / CSS / JS    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │     FastAPI API     │
                │      Backend        │
                └──────────┬──────────┘
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
        ┌────────────────┐   ┌────────────────┐
        │ SQLite Database│   │  Gemini AI API │
        │    Expenses    │   │ AI Intelligence│
        └────────────────┘   └────────────────┘
