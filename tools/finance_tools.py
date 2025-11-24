# tools/finance_tools.py
import random

def get_current_mortgage_rate(loan_type: str = "30_year_fixed"):
    """
    Fetches the current national average mortgage rate.
    Use this tool when the script mentions rates, payments, or market conditions.
    """
    # MOCK: Simulating a live API call (e.g., 6.5% - 7.5%)
    base_rate = 6.5 + (random.random() * 1.0)
    
    print(f"   [TOOL] 🛠️  Agent is looking up {loan_type} rates...")
    
    return {
        "loan_type": loan_type,
        "rate_percentage": round(base_rate, 2),
        "trend": "stable",
        "timestamp": "2025-11-18"
    }