import asyncio
import os
import io
import json
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, ValidationError
# Removed unnecessary starlette import
from main_graph import run_agent_system 
from tools.models import AgentState, InfluencerProfile 

# --- SERVICE ACCOUNT SETUP (for Sheets integration) ---
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_EMAIL = "sheets-connector-sa@influencer-agent-dev-phase2.iam.gserviceaccount.com"

# Load environment variable for safety/API key 
from dotenv import load_dotenv
load_dotenv()

# --- 1. DEFINE INPUT SCHEMA ---
class AnalyzeRequestSchema(BaseModel):
    approved_script: str
    influencer_transcript: str
    campaign_date: str
    influencer_profile: dict 

# --- 2. INITIALIZE APP ---
is_prod = os.getenv("ENV") == "production"

app = FastAPI(
    title="Influencer Review Agent API (Phase 2)",
    version="1.1.0",
    description="Multi-Agent System with File Upload and Sheets Integration.",
    docs_url="/docs", 
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# --- 3. DEFINE ENDPOINT ---
@app.post("/analyze_live", response_model=AgentState)
async def analyze_campaign_live(
    # File upload field
    csv_file: UploadFile = File(..., description="Lead Performance Data (CSV file)"),
    
    # Text/JSON inputs are passed as Form data
    approved_script: str = Form(..., description="The approved marketing copy."),
    influencer_transcript: str = Form(..., description="The actual video transcript."),
    campaign_date: str = Form(..., description="The date the campaign ran (YYYY-MM-DD)."),
    influencer_profile: str = Form(..., description="Influencer details (JSON string).")
):
    """
    Triggers the Async 4-Gear Attribution Workflow using a file upload.
    """
    try:
        # 3a. Read and decode the CSV file contents
        file_contents = await csv_file.read()
        csv_data = file_contents.decode("utf-8")
        
        # 3b. Parse the JSON strings from Form data
        try:
            profile_data = json.loads(influencer_profile)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON format in 'influencer_profile' field.")
        
        # 3c. Run the core logic DIRECTLY (Fixing the Coroutine Error)
        # run_agent_system is already async, so we just await it.
        result_state = await run_agent_system(
            approved_script,
            influencer_transcript,
            csv_data,
            campaign_date,
            profile_data,
        )
        
        if result_state.errors:
             # Log errors but return state (or raise 500 if preferred)
             pass

        return result_state
        
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=f"Input Validation Error: {ve.errors()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# --- 4. HEALTH CHECK ---
@app.get("/health")
def health_check():
    """Simple heartbeat."""
    return {"status": "ok", "service": "influencer-agent"}