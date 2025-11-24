from tools.policy_manager import PolicyManager

def run_test():
    pm = PolicyManager()
    
    print("--- 🕰️ Testing Policy Time Machine ---")
    
    # Test 1: Look up a past date (Jan 20th - Should be 'Rate Pivot')
    date_query = "2024-01-20"
    active_policy = pm.get_policy_for_date(date_query)
    if active_policy:
        print(f"Date: {date_query}")
        print(f"Active Policy: {active_policy.name}")
        print(f"Mandatory Phrases: {active_policy.compliance_phrases}")
        print("✅ Time Travel Successful\n")
    else:
        print("❌ Failed to find policy.")

    print("--- 📊 Testing Volatility Analysis ---")
    
    # Scenario A: Q1 (Jan-Feb) - Many Changes + High Chaos (Good)
    print("\nScenario A: Chaotic Q1 (Market Chaos = 8/10)")
    result_a = pm.analyze_strategic_volatility(
        "2024-01-01", "2024-02-28", market_chaos_score=8
    )
    print(f"Diagnosis: {result_a['strategic_diagnosis']}")
    print(f"Changes: {result_a['policy_changes']}")

    # Scenario B: Q1 (Jan-Feb) - Many Changes + Low Chaos (Bad)
    print("\nScenario B: If Market was Stable (Market Chaos = 2/10)")
    result_b = pm.analyze_strategic_volatility(
        "2024-01-01", "2024-02-28", market_chaos_score=2
    )
    print(f"Diagnosis: {result_b['strategic_diagnosis']}")
    print(f"Changes: {result_b['policy_changes']}")

if __name__ == "__main__":
    run_test()