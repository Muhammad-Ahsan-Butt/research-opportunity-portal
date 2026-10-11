from datetime import datetime

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


# validate request body for creating or updating an opportunity
def validate_opportunity_payload(data, is_update=False):
    if not isinstance(data, dict):
        return False, "Request body must be a valid JSON object.", None

    cleaned = {}

    if not is_update:
        for field in REQUIRED_FIELDS:
            if field not in data or data[field] is None:
                return False, f"Missing required field: '{field}'", None
            if isinstance(data[field], str) and not data[field].strip():
                return False, f"Field '{field}' cannot be empty.", None

    # check string fields
    string_fields = ["title", "description", "research_area", "faculty_name", "department", "required_skills"]
    for field in string_fields:
        if field in data:
            val = data[field]
            if not isinstance(val, str) or not val.strip():
                return False, f"Field '{field}' must be a non-empty string.", None
            cleaned[field] = val.strip()

    # check positions available
    if "positions_available" in data:
        val = data["positions_available"]
        try:
            val_int = int(val)
            if val_int <= 0:
                return False, "Field 'positions_available' must be a positive integer greater than 0.", None
            cleaned["positions_available"] = val_int
        except (ValueError, TypeError):
            return False, "Field 'positions_available' must be a valid integer.", None

    # check deadline format (YYYY-MM-DD)
    if "deadline" in data:
        val = data["deadline"]
        if not isinstance(val, str) or not val.strip():
            return False, "Field 'deadline' must be a valid date string in YYYY-MM-DD format.", None
        try:
            parsed_date = datetime.strptime(val.strip(), "%Y-%m-%d").date()
            cleaned["deadline"] = parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            return False, "Invalid 'deadline' format. Expected YYYY-MM-DD.", None

    # check status
    if "status" in data:
        val = str(data["status"]).strip()
        if val not in VALID_STATUSES:
            return False, f"Field 'status' must be either 'Open' or 'Closed'.", None
        cleaned["status"] = val
    elif not is_update:
        cleaned["status"] = "Open"

    if is_update and not cleaned:
        return False, "At least one field must be provided for update.", None

    return True, None, cleaned
