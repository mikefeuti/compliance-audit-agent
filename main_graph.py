import asyncio
import time
from datetime import date
from agents.analyzer import ContentAnalyzerAgent
from agents.coordinator import ReviewCoordinatorAgent
from tools.metrics_engine import calculate_campaign_metrics
from tools.policy_manager import PolicyManager
from tools.models import AgentState, InfluencerProfile, InfluencerTag

# Initialize Agents and Managers (Singletons)
caa = ContentAnalyzerAgent()
rca = ReviewCoordinatorAgent()
policy_manager = PolicyManager()

async def run_agent_system(approved_script: str, influencer_transcript: str, csv_data: str, campaign_date_str: str, influencer_data: dict) -> AgentState:
    """
    The Core Orchestration Logic.
    1. Looks up Brand Policy based on date (Time Travel).
    2. Runs Content Analysis (Tool Use) and Metrics Calculation (Deterministic) in parallel.
    3. Synthesizes all inputs via the Review Coordinator.
    """
    print("\n--- 🚀 Starting Orchestration with Context Lookup ---")
    start_total = time.time()
    
    # 1. Initialization and Policy Lookup (The Governance Layer)
    try:
        campaign_date = date.fromisoformat(campaign_date_str)
        # Validate and unpack the influencer data
        influencer_profile = InfluencerProfile(**influencer_data)
        
        # GEAR 3 INTEGRATION: Find the active policy for the campaign date
        active_policy = policy_manager.get_policy_for_date(campaign_date_str)
        if not active_policy:
            raise ValueError(f"No active Brand Policy found for date {campaign_date_str}")
        
        # Create the central state object (active_policy is a Pydantic object, so we pass it directly)
        state = AgentState(
            approved_script=approved_script,
            influencer_transcript=influencer_transcript,
            csv_data=csv_data,
            campaign_date=campaign_date,
            influencer_profile=influencer_profile,
            brand_policy=active_policy # Pydantic object access will use dot notation
        )

    except Exception as e:
        print(f"   [INIT] ❌ Initialization Failed: {e}")
        # Return a failed state
        return AgentState(
            approved_script="", influencer_transcript="", csv_data="", errors=[f"Initialization Failed: {e}"], 
            campaign_date=date.today(), 
            influencer_profile=InfluencerProfile(id="", name="", archetypes=[])
        )


    # 2. Parallel Execution (Map Step)
    def run_content_task():
        print("   [Map] 🧠 Content Agent analyzing...")
        # CRITICAL FIX: Pass both the approved script and the transcript
        return caa.analyze(
            approved_script, 
            influencer_transcript, 
            active_policy.compliance_phrases, 
            active_policy.forbidden_topics
        )

    def run_data_task():
        print("   [Map] 🧮 Metrics Engine calculating...")
        return calculate_campaign_metrics(csv_data)

    try:
        content_result, data_result = await asyncio.gather(
            asyncio.to_thread(run_content_task),
            asyncio.to_thread(run_data_task)
        )
        # Update State
        state.content_analysis = content_result
        state.performance_data = data_result
        print("   [Map] ✅ Parallel tasks complete.")
    except Exception as e:
        state.errors.append(f"Map Phase Error: {str(e)}")
        return state

    # 3. Strategic Review (The "Reduce" Step)
    print("   [Reduce] 👔 Coordinator synthesizing strategy...")
    try:
        # FIX 1: Convert Policy object to dict for the LLM prompt consumption
        final_review = await asyncio.to_thread(
            rca.review, 
            state.content_analysis, 
            state.performance_data.model_dump(), 
            state.brand_policy.model_dump(), 
            state.influencer_profile.model_dump() 
        )
        state.final_strategic_review = final_review
        print("   [Reduce] ✅ Synthesis complete.")
    except Exception as e:
        state.errors.append(f"Reduce Phase Error: {str(e)}")

    total_time = time.time() - start_total
    print(f"--- 🏁 Workflow Finished in {total_time:.2f}s ---\n")
    
    return state

# Entry Point for Local Testing
if __name__ == "__main__":
    # 🚨 TEST CASE: Adherence Check (Script vs. Transcript)
    TEST_DATE = "2024-01-20"
    
    # Approved Script (Short and compliant)
    APPROVED_SCRIPT = "Lock in your rate today! Don't wait. Our guarantee is an Equal Housing Lender."
    
    # Transcript (Longer, ad-libbed, and non-compliant on 'guarantee' and '100%')
    INFLUENCER_TRANSCRIPT = "Hey guys, let me tell you, rates are basically guaranteed to go up next month, so lock it in now. You can trust me 100% on this. Don't wait. Our guarantee is an Equal Housing Lender."
    
    sample_csv = "spend,conversions,revenue\n100,10,500\n" # Mock performance data
    
    # Influencer Profile Data: Sarah Skeptic works well with the Rate Spike Pivot message
    influencer_profile_data = {
        "id": "INF-001",
        "name": "Sarah Skeptic",
        "archetypes": ["Skeptic", "Educator"]
    }

    result = asyncio.run(run_agent_system(APPROVED_SCRIPT, INFLUENCER_TRANSCRIPT, sample_csv, TEST_DATE, influencer_profile_data))
    
    print("FINAL OUTPUT PREVIEW:")
    print("-" * 50)
    
    # Access the policy name using dot notation (Pydantic object)
    if result.brand_policy:
        print(f"Policy Used: {result.brand_policy.name}")
    
    print(f"Errors: {result.errors}")
    
    # Displaying the adherence check results
    if result.content_analysis and result.content_analysis.get('deviation_summary'):
        print(f"Risk Check: {result.content_analysis['deviation_summary']}")
        
    if result.final_strategic_review:
        print(result.final_strategic_review[:400] + "...\n(truncated)")