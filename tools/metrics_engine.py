import pandas as pd
import io
from tools.models import PerformanceMetrics

def calculate_campaign_metrics(csv_data: str) -> PerformanceMetrics:
    """
    Parses CSV data and returns deterministic performance metrics based on
    the Phase 2 schema: New Leads, SignOffs, Closes.
    """
    try:
        # Wrap string data into a file object for pandas
        df = pd.read_csv(io.StringIO(csv_data))
        
        # 1. VALIDATION: Check for the new, simpler column headers
        # Note: Pandas is case-sensitive, so we check exact matches.
        required_cols = {'New Leads', 'SignOffs', 'Closes'} 
        
        if not required_cols.issubset(df.columns):
            # Fallback check: try lowercase if the user uploaded a messy file
            df.columns = [c.strip() for c in df.columns] # Clean whitespace
            if not required_cols.issubset(df.columns):
                 raise ValueError(f"CSV missing required columns: {required_cols - set(df.columns)}")

        # 2. CALCULATION: Sum the columns directly (No more multiplication simulation)
        # The CSV now contains the actual counts we want.
        raw_leads = int(df['New Leads'].sum())
        # In your new schema, 'SignOffs' likely represents lost leads (leads signed off/disqualified)
        lost_leads = int(df['SignOffs'].sum()) 
        closed_count = int(df['Closes'].sum())
        
        # 3. RETURN: Populate the Pydantic model
        return PerformanceMetrics(
            raw_lead_count=raw_leads,
            lost_leads=lost_leads,
            closed_count=closed_count
        )

    except Exception as e:
        raise ValueError(f"Metric Calculation Failed: {str(e)}")