import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List
from tools.finance_tools import get_current_mortgage_rate

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class ContentAnalyzerAgent:
    def __init__(self):
        self.tools = [get_current_mortgage_rate]
        
        self.system_instruction_template = """
            You are an expert Content Strategist and Compliance Auditor. Analyze the script delivery.
            
            CRITICAL: Use the 'get_current_mortgage_rate' tool if the script mentions rates or payments.
            
            PROTOCOL:
            1. Compare the APPROVED SCRIPT (The Plan) against the INFLUENCER TRANSCRIPT (The Reality).
            2. Check the script against the mandatory compliance phrases and Forbidden Topics.
            3. Output valid JSON matching the ContentMetrics schema.
        """
        
        self.model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            tools=self.tools
        )

    def analyze(self, approved_script: str, influencer_transcript: str, compliance_phrases: List[str], forbidden_topics: List[str]) -> dict:
        """The agent receives the APPROVED SCRIPT and the INFLUENCER TRANSCRIPT for comparison."""
        try:
            # 1. Inject ALL dynamic rules into the system instruction for the LLM's context
            full_system_instruction = self.system_instruction_template + \
                                     f"\n\nMANDATORY COMPLIANCE PHRASES: {compliance_phrases}" + \
                                     f"\nFORBIDDEN TOPICS (Risk Check - List specific violation sentences): {forbidden_topics}"
            
            # 2. Re-initialize the model to set the instruction (SDK FIX)
            model_with_instruction = genai.GenerativeModel(
                model_name=self.model.model_name,
                tools=self.tools,
                system_instruction=full_system_instruction
            )
            
            chat = model_with_instruction.start_chat(
                enable_automatic_function_calling=True
            )
            
            # 3. Define the primary prompt for semantic comparison
            prompt = f"""
            Perform a DUAL SCORE ADHERENCE check (Semantic Fidelity & Risk Deviation).
            
            COMPARE:
            A) Approved Script (PLAN): "{approved_script}"
            B) Influencer Transcript (REALITY): "{influencer_transcript}"
            
            1. Check Compliance: Were all MANDATORY PHRASES used?
            2. Check Fidelity: Does the Transcript's meaning align with the Approved Script?
            3. Check Deviation: Scan for sentences violating Forbidden Topics and list them in 'deviation_summary'.
            
            Return ONLY the JSON object matching the ContentMetrics schema.
            """
            
            # 4. Send the message
            response = chat.send_message(prompt)
            
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            
            return json.loads(clean_text)
            
        except Exception as e:
            print(f"CAA Error: {e}")
            return {
                "tone_score": 0, 
                "hook_strength": "Low", 
                "key_themes": ["ERROR"], 
                "rate_check": "Error", 
                "deviation_summary": [f"System Error: {e}"]
            }