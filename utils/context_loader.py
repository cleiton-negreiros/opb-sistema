import json
import os
from pathlib import Path
from typing import Dict, Any

def load_context() -> Dict[str, Any]:
    """
    Load all context files from the context-brain directory.
    Returns a dictionary with all context data.
    """
    context_dir = Path(__file__).parent.parent / "context-brain"
    
    context = {}
    
    # Load business core
    business_core_path = context_dir / "business-core.json"
    if business_core_path.exists():
        with open(business_core_path, 'r', encoding='utf-8') as f:
            context["business_core"] = json.load(f)
    else:
        raise FileNotFoundError(f"Business core file not found at {business_core_path}")
    
    # Load personal profile
    personal_profile_path = context_dir / "personal-profile.json"
    if personal_profile_path.exists():
        with open(personal_profile_path, 'r', encoding='utf-8') as f:
            context["personal_profile"] = json.load(f)
    else:
        raise FileNotFoundError(f"Personal profile file not found at {personal_profile_path}")
    
    # Load goals
    goals_path = context_dir / "goals.json"
    if goals_path.exists():
        with open(goals_path, 'r', encoding='utf-8') as f:
            context["goals"] = json.load(f)
    else:
        raise FileNotFoundError(f"Goals file not found at {goals_path}")
    
    return context

def get_business_value(context: Dict[str, Any], key: str, default=None):
    """Safely get a value from the business core context."""
    return context.get("business_core", {}).get(key, default)

def get_personal_value(context: Dict[str, Any], key: str, default=None):
    """Safely get a value from the personal profile context."""
    return context.get("personal_profile", {}).get(key, default)

def get_goal_value(context: Dict[str, Any], key: str, default=None):
    """Safely get a value from the goals context."""
    return context.get("goals", {}).get(key, default)