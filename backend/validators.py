"""
Input validation and standardized response utilities for Research Opportunity Portal.
"""

from datetime import datetime
from typing import Tuple, Optional, Dict, Any


VALID_STATUSES = {"Open", "Closed"}

REQUIRED_FIELDS = [
    "title",
    "description",
    "research_area",
    "faculty_name",
    "department",
    "required_skills",
    "positions_available",
    "deadline"
]


def validate_opportunity_payload(data: Any, is_update: bool = False) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
    """
    Validate research opportunity payload for create (POST) or update (PUT).
    
    Args:
        data: Parsed JSON dictionary.
        is_update: If True, partial fields can be accepted if at least one valid field is provided.
        
    Returns:
        (is_valid, error_message, cleaned_data)
    """
    if not isinstance(data, dict):
        return False, "Request body must be a valid JSON object.", None

    cleaned: Dict[str, Any] = {}

    if not is_update:
        # For creation, all REQUIRED_FIELDS must be present
        for field in REQUIRED_FIELDS:
            if field not in data or data[field] is None:
                return False, f"Missing required field: '{field}'", None
            if isinstance(data[field], str) and not data[field].strip():
                return False, f"Field '{field}' cannot be empty.", None

    # String fields validation
    string_fields = ["title", "description", "research_area", "faculty_name", "department", "required_skills"]
    for field in string_fields:
        if field in data:
            val = data[field]
            if not isinstance(val, str) or not val.strip():
                return False, f"Field '{field}' must be a non-empty string.", None
            cleaned[field] = val.strip()

    # Positions available validation
    if "positions_available" in data:
        val = data["positions_available"]
        try:
            val_int = int(val)
            if val_int <= 0:
                return False, "Field 'positions_available' must be a positive integer greater than 0.", None
            cleaned["positions_available"] = val_int
        except (ValueError, TypeError):
            return False, "Field 'positions_available' must be a valid integer.", None

    # Deadline validation (YYYY-MM-DD)
    if "deadline" in data:
        val = data["deadline"]
        if not isinstance(val, str) or not val.strip():
            return False, "Field 'deadline' must be a valid date string in YYYY-MM-DD format.", None
        try:
            # Parse to ensure valid calendar date
            parsed_date = datetime.strptime(val.strip(), "%Y-%m-%d").date()
            cleaned["deadline"] = parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            return False, "Invalid 'deadline' format. Expected YYYY-MM-DD.", None

    # Status validation
    if "status" in data:
        val = str(data["status"]).strip()
        if val not in VALID_STATUSES:
            return False, f"Field 'status' must be either 'Open' or 'Closed' (received '{val}').", None
        cleaned["status"] = val
    elif not is_update:
        # Default status for new opportunities
        cleaned["status"] = "Open"

    if is_update and not cleaned:
        return False, "At least one valid field must be provided for update.", None

    return True, None, cleaned
