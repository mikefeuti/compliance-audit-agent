# test_step_iii.py
from agents.analyzer import ContentAnalyzerAgent
from agents.coordinator import ReviewCoordinatorAgent
import time

def test_agents():
    print("--- Testing Probabilistic Layer (Agents) ---")

    # 1. Test Content Analyzer (CAA)
    print("\n1. Testing Content Analyzer (Flash)...")
    try:
        caa = ContentAnalyzerAgent()
        script = "HEY GUYS! This new energy drink is literally fire. Buy it now!"

        start = time.time()
        analysis = caa.analyze(script)
        duration = time.time() - start

        print(f"   -> Latency: {duration:.2f}s")
        print(f"   -> Output: {analysis}")

        if "tone_score" in analysis:
            print("   ✅ CAA Success: Valid Structured Data.")
        else:
            print("   ❌ CAA Failure: Invalid Output.")
    except Exception as e:
        print(f"   ❌ CAA Crash: {e}")

    # 2. Test Review Coordinator (RCA)
    print("\n2. Testing Review Coordinator (Pro)...")
    try:
        rca = ReviewCoordinatorAgent()

        # Mock inputs
        mock_content = {"tone_score": 8, "hook_strength": "High", "key_themes": ["Energy", "Excitement"]}
        mock_perf = {"roas": 4.5, "cpa": 12.50, "total_spend": 1000}

        start = time.time()
        strategy = rca.review(mock_content, mock_perf)
        duration = time.time() - start

        print(f"   -> Latency: {duration:.2f}s")

        if "<thought_process>" in strategy:
            print("   ✅ RCA Success: Thought Process XML found.")
            # Show a snippet of the AI's brain
            start_tag = strategy.find("<thought_process>") + 17
            end_tag = strategy.find("</thought_process>")
            print(f"   -> Reasoning Snippet: '{strategy[start_tag:start_tag+80]}...'")
        else:
            print("   ❌ RCA Failure: Model skipped reasoning protocol.")
            print(f"   -> Output: {strategy[:100]}...")
    except Exception as e:
         print(f"   ❌ RCA Crash: {e}")

if __name__ == "__main__":
    test_agents()