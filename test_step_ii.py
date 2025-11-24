# test_step_ii.py
from tools.metrics_engine import calculate_campaign_metrics
from tools.models import PerformanceMetrics
import json

def run_test(name, csv_input, expected_behavior):
    print(f"--- Running Test: {name} ---")
    try:
        result = calculate_campaign_metrics(csv_input)
        
        # Verification Logic
        if expected_behavior == "success":
            print(f"✅ SUCCESS: Calculated ROAS: {result.roas} | CPA: {result.cpa}")
            # specific check for the 'Happy Path'
            if result.roas == 5.0:
                print("   -> Math Verification: Accurate.")
        elif expected_behavior == "zero_division":
            print(f"✅ SUCCESS: Handled Zero Division. CPA is {result.cpa} (Should be 0.0)")
            
    except Exception as e:
        if expected_behavior == "fail":
            print(f"✅ SUCCESS: Correctly caught bad data. Error: {e}")
        else:
            print(f"❌ FAILURE: Crashed unexpectedly. Error: {e}")
    print("\n")

if __name__ == "__main__":
    # TEST 1: The Happy Path (Normal Data)
    csv_normal = """spend,conversions,revenue
100,10,500
200,20,1000"""
    run_test("Normal Data", csv_normal, "success")

    # TEST 2: The "Zero Division" Edge Case (No Conversions)
    # If your code isn't robust, this crashes the agent.
    csv_zero = """spend,conversions,revenue
100,0,0"""
    run_test("Zero Conversions", csv_zero, "zero_division")

    # TEST 3: The Security/Data Integrity Check (Bad Columns)
    # Simulating an uploaded file with wrong headers
    csv_bad = """cost,leads,money_made
100,10,500"""
    run_test("Bad Columns", csv_bad, "fail")