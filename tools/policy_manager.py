import json
from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel
# Note: The BrandPolicy definition is moved to tools/models.py, 
# but the manager uses it.

class PolicyManager:
    def __init__(self, filepath="policies.json"):
        self.filepath = filepath
        self.policies = self._load_policies()

    def _load_policies(self) -> List[BaseModel]: # Use BaseModel to avoid circular dependency
        """Loads and validates the JSON history."""
        from tools.models import BrandPolicy # Local import to break the cycle
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
            # Sort by date to ensure chronological order
            policies = [BrandPolicy(**p) for p in data]
            policies.sort(key=lambda x: x.start_date)
            return policies
        except FileNotFoundError:
            return []

    def get_policy_for_date(self, target_date_str: str) -> Optional[BaseModel]:
        """
        The Time Machine: Returns the rules active on a specific date.
        Input format: 'YYYY-MM-DD'
        """
        target = datetime.strptime(target_date_str, "%Y-%m-%d").date()
        
        for policy in self.policies:
            # Check start date
            if policy.start_date <= target:
                # Check end date (if it exists)
                if policy.end_date is None or policy.end_date >= target:
                    return policy
        return None