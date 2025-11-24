import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class ReviewCoordinatorAgent:
    def __init__(self):
        # Base model initialized without instruction (it's dynamic)
        self.model = genai.GenerativeModel(
            model_name='gemini-2.5-pro'
        )

    def review(self, content_data: dict, performance_data: dict, policy_data: dict, influencer_data: dict) -> str:
        """Receives all context data and synthesizes the strategic review."""
        
        # 1. Construct the Comprehensive System Instruction
        system_instruction = f"""
        You are the Lead Performance Strategist. Your goal is multivariate attribution: finding if performance was due to the Market, the Message, or the Messenger.
        
        CORE PHILOSOPHY: Market Rates are the primary driver of Lead Performance, serving as the Contextual Lens (Headwind/Tailwind).
        
        INPUT CONTEXT:
        - Campaign Policy: {policy_data['name']} (Trigger: {policy_data['market_trigger']})
        - Brand Focus: {policy_data['focus_phrases']}
        - Influencer Persona: {influencer_data['name']} (Archetypes: {influencer_data['archetypes']})
        
        ANALYSIS PROTOCOL (Chain-of-Thought required in <thought_process> tags):
        1. Contextualize Market: Determine if the {policy_data['market_trigger']} suggests a 'Headwind' or 'Tailwind'.
        2. Evaluate Persona Fit: Does the Content Analyzer's score (Tone/Hook) align with the Influencer's Archetype ({influencer_data['archetypes']})?
        3. Correlate Performance: Weigh the Lead Volume (North Star) against the Market Context. Use the 'Steady Hand' protocol (Low volume in Headwind = Acceptable, No Change needed).
        4. Strategy Generation: Provide actionable recommendations (copy changes, scaling, or maintenance).
        """
        
        try:
            # CRITICAL FIX: Dynamically create a new model instance with the instruction 
            # as a top-level argument, which satisfies the SDK syntax requirement.
            model_with_instruction = genai.GenerativeModel(
                model_name=self.model.model_name,
                system_instruction=system_instruction
            )
            
            prompt = f"""
            Content Analysis (Quality/Compliance): {content_data}
            Performance Metrics (Volume/Quality): {performance_data}
            
            Provide a final Strategic Review.
            """
            
            # Call generate_content on the new model instance
            response = model_with_instruction.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"RCA Error during synthesis: {e}"