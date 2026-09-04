import os
from dotenv import load_dotenv
from google import genai


# ==========================================
# LOAD .ENV FILE
# ==========================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)


# ==========================================
# GEMINI API KEY
# ==========================================

api_key = os.getenv("GEMINI_API_KEY")

print("ENV FILE:", ENV_PATH)
print("Gemini key loaded:", bool(api_key))


if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. Check your .env file."
    )


# ==========================================
# GEMINI CLIENT
# ==========================================

client = genai.Client(api_key=api_key)

def safe_generate(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        error_message = str(e)

        if "RESOURCE_EXHAUSTED" in error_message:
            return (
                "⚠️ AI temporarily unavailable\n\n"
                "Gemini API daily limit has been reached. "
                "Please try again later."
            )

        return (
            "❌ PayPilot AI could not process this request right now.\n\n"
            "Please try again later."
        )


# ==========================================
# AI EXPENSE ANALYSIS
# ==========================================

def analyze_expenses(expenses):

    expense_text = "\n".join(
        [
            f"- {e.title}: ₹{e.amount} ({e.category})"
            for e in expenses
        ]
    )

    prompt = f"""
You are PayPilot AI, a smart personal finance assistant.

Analyze these expenses:

{expense_text}

Give the user:

1. Spending summary
2. Highest spending category
3. Areas where they may be overspending
4. Saving suggestions
5. Simple budget recommendation

Keep it concise and easy to understand.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text

def create_budget_plan(expenses, monthly_budget):
    expense_text = "\n".join(
        [
            f"- {e.title}: ₹{e.amount} ({e.category})"
            for e in expenses
        ]
    )

    prompt = f"""
You are PayPilot AI, an intelligent personal finance controller.

The user's monthly budget is ₹{monthly_budget}.

Here are the user's current expenses:

{expense_text}

Create a practical monthly budget plan.

Give:
1. Current spending summary
2. Recommended amount for each major category
3. Recommended savings amount
4. Categories where the user should reduce spending
5. A simple action plan

Make sure the recommended category amounts add up approximately to the monthly budget.

Keep the answer concise, clear and easy to understand.
Use Indian Rupees (₹).
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text

    # ==========================================
# 💬 ASK PAYPILOT AI
# ==========================================

def ask_paypilot(question, expenses):

    expense_text = "\n".join(
        [
            f"- {e.title}: ₹{e.amount} ({e.category})"
            for e in expenses
        ]
    )

    prompt = f"""
You are PayPilot AI, an intelligent personal finance controller.

The user's current expenses are:

{expense_text}

The user asks:

"{question}"

Answer the user's question using their expense data.

Rules:
- Give practical and personalized financial advice.
- Use the expense data when relevant.
- Mention actual amounts when useful.
- Do not invent expenses or financial information.
- Keep the answer concise and easy to understand.
- If the question is unrelated to personal finance, politely say you are focused on financial assistance.

Answer directly without unnecessary introduction.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text

# ==========================================
# ⚠️ SMART OVERSPENDING ALERT
# ==========================================

def detect_overspending(expenses):

    if not expenses:
        return "No expenses available to analyze."

    expense_text = "\n".join(
        [
            f"- {e.title}: ₹{e.amount} ({e.category})"
            for e in expenses
        ]
    )

    prompt = f"""
You are PayPilot AI, an intelligent financial controller.

Analyze the user's expenses below:

{expense_text}

Detect potential overspending.

Rules:
- Identify the highest spending category.
- Look for categories that appear unusually high.
- Give 1 or 2 practical suggestions.
- Mention actual amounts.
- Do not invent expenses.
- If spending does not look concerning, say that clearly.
- Keep the response concise.

Return the result in this format:

⚠️ Spending Alert

[Your main finding]

💡 Recommendation

[Your recommendation]
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return safe_generate(prompt)

def generate_financial_report(expenses):

    if not expenses:
        return "No expenses available to generate a financial report."

    expense_text = "\n".join(
        [
            f"- {e.title}: ₹{e.amount} ({e.category})"
            for e in expenses
        ]
    )

    prompt = f"""
You are PayPilot AI, an intelligent financial controller.

Analyze the user's current expense data:

{expense_text}

Create a concise financial report.

Include:

1. 💰 Total Spending
2. 🏆 Highest Spending Category
3. 📊 Category Breakdown
4. ⚠️ Potential Overspending Areas
5. 💵 Possible Savings Opportunities
6. 🎯 Top 3 Financial Recommendations

Rules:
- Use only the expense data provided.
- Mention actual amounts.
- Do not invent income, dates, or expenses.
- Give practical recommendations.
- Keep the report clear and easy to understand.
- Use Indian Rupees (₹).

Format the response with clear headings.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text

def detect_anomalies(expenses):

    if not expenses:
        return "No expenses available to analyze."

    expense_text = "\n".join(
        [
            f"- {e.title}: ₹{e.amount} ({e.category})"
            for e in expenses
        ]
    )

    prompt = f"""
You are PayPilot AI, an intelligent financial controller.

Analyze these expenses:

{expense_text}

Detect unusual or suspicious spending patterns.

Look for:
1. Expenses that are unusually large.
2. Categories with unusually high spending.
3. Repeated spending that may indicate a problem.
4. Any spending that is significantly different from the rest.

Rules:
- Use only the provided expense data.
- Mention actual expense names and amounts.
- Do not invent information.
- If there are no clear anomalies, say so.
- Give practical advice.
- Keep the response concise.

Return in this format:

🚨 Anomaly Detection

[Main unusual spending found]

💡 Recommendation

[Practical recommendation]
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text

def categorize_expense(title):

    prompt = f"""
You are PayPilot AI, an intelligent expense categorization assistant.

Categorize this expense:

"{title}"

Choose exactly ONE category from:

Food
Travel
Shopping
Education
Health
Bills
Entertainment
Subscriptions
Transport
Other

Return ONLY the category name.
Do not add explanations.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text.strip()

def calculate_financial_health(expenses):

    if not expenses:
        return "No expenses available to calculate your financial health score."

    expense_text = "\n".join(
        [
            f"- {e.title}: ₹{e.amount} ({e.category})"
            for e in expenses
        ]
    )

    prompt = f"""
You are PayPilot AI, an intelligent personal finance controller.

Analyze the user's expenses:

{expense_text}

Calculate a Financial Health Score from 0 to 100.

Consider:
- Overall spending
- Highest spending categories
- Potential overspending
- Ability to save
- Spending balance across categories

Use this scoring:
80-100 = Excellent
60-79 = Good
40-59 = Needs Improvement
0-39 = High Risk

Return the result in exactly this format:

💳 FINANCIAL HEALTH SCORE

Score: XX/100
Status: [Excellent/Good/Needs Improvement/High Risk]

📊 Analysis
[Brief explanation of why the score was given]

⚠️ Main Concern
[Most important spending concern]

💡 Recommendation
[One or two practical recommendations]

🎯 Savings Potential
[Estimated amount the user could potentially save based only on the provided expenses]

Do not invent expenses.
Keep the response concise and easy to understand.
Use Indian Rupees (₹).
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text