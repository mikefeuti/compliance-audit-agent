from typing import List, Optional
from datetime import date
from enum import Enum
from pydantic import BaseModel, Field

# --- Gear 3: Content Metrics Output ---
class ContentMetrics(BaseModel):
    """Structured output from the Content Analyzer Agent"""
    tone_score: int = Field(..., description="Rating 1-10 of tone appropriateness")
    hook_strength: str = Field(..., pattern="^(High|Medium|Low)$", description="Strength of the first 3 seconds")
    key_themes: List[str] = Field(default_factory=list, description="Main topics identified")
    rate_check: str = Field(
        "Not Applicable", 
        description="Did the script match current market rates? (Valid, Invalid, or Not Applicable)"
    )
    # NEW FIELD: Capture the risk data for the Deviation Score
    deviation_summary: List[str] = Field(
        default_factory=list, 
        description="Specific sentences from the transcript that violate Forbidden Topics or compliance rules."
    )

# --- Gear 2: Influencer Persona Tags ---
class InfluencerTag(str, Enum):
    # Values
    SKEPTIC = "Skeptic"
    CONSERVATIVE = "Conservative"
    COMMUNITY = "Community"
    # Format
    NEWS = "News"
    CULTURE = "Culture"
    EDUCATOR = "Educator"

class InfluencerProfile(BaseModel):
    id: str
    name: str
    # We allow multiple tags to capture the multi-dimensional persona
    archetypes: List[InfluencerTag] = Field(..., description="List of Persona Tags")
    avg_lead_volume: Optional[int] = Field(None, description="Their 'Par' score")

# --- Gear 3: Brand Policy (Time Travel Logic) ---
class BrandPolicy(BaseModel):
    """
    Defines the rules active during a specific time window.
    """
    policy_id: str
    name: str
    start_date: date
    end_date: Optional[date]
    market_trigger: str
    focus_phrases: List[str] = Field(..., description="Dynamic brand themes (Fuzzy Match)")
    compliance_phrases: List[str] = Field(
        default=["NMLS #12345", "Equal Housing Lender"], 
        description="Static legal phrases (100% Match required)."
    )
    # NEW FIELD: Dynamic rules for risk/deviation analysis
    forbidden_topics: List[str] = Field(
        default_factory=list, description="Phrases/concepts that must NOT appear (Fuzzy violation check)."
    )

    def is_active_for(self, check_date: date) -> bool:
        """Helper to see if this policy applies to a specific script date."""
        if self.end_date:
            return self.start_date <= check_date <= self.end_date
        return self.start_date <= check_date

# --- Gear 4: Performance Metrics ---
class PerformanceMetrics(BaseModel):
    raw_lead_count: int      # The North Star (Volume)
    lost_leads: int          # "Fall out"
    closed_count: int        # Revenue Event Proxy
    
    @property
    def qualified_lead_count(self) -> int:
        """Calculated field: Leads minus those that fell out."""
        return self.raw_lead_count - self.lost_leads
        
    @property
    def win_rate(self) -> float:
        """Calculated field: Closed count / Raw leads."""
        if self.raw_lead_count == 0: return 0.0
        return round(self.closed_count / self.raw_lead_count, 3)

# --- The Central State (The Multi-Agent Contract) ---
class AgentState(BaseModel):
    """The central state object passed between all agents."""
    # FIX: Two separate fields for the adherence check
    approved_script: str = Field(..., description="The original, approved copy provided to the influencer.")
    influencer_transcript: str = Field(..., description="The actual text or audio read by the influencer.")
    csv_data: str
    campaign_date: date = Field(..., description="The date the campaign ran.")
    
    # GEARS INTEGRATED
    influencer_profile: InfluencerProfile
    brand_policy: Optional[BrandPolicy] = Field(None, description="The rules active on campaign_date.")
    
    # ... (Rest of the fields) ...
    content_analysis: Optional[ContentMetrics] = None
    performance_data: Optional[PerformanceMetrics] = None
    final_strategic_review: Optional[str] = None
    errors: List[str] = Field(default_factory=list)