import re

MAX_INPUT_LENGTH = 10000  # character limit safeguard

def preprocess_text(text: str) -> str:
    """
    Clean and prepare raw text input before running tokenizer / ML models.
    - Strips leading/trailing whitespace
    - Replaces excessive white spaces and newlines with a single space
    """
    if not isinstance(text, str):
        return ""
    
    cleaned = text.strip()
    # Normalize multiple whitespace characters
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    # Enforce maximum character safety limit
    if len(cleaned) > MAX_INPUT_LENGTH:
        cleaned = cleaned[:MAX_INPUT_LENGTH]
        
    return cleaned

def validate_input(data):
    """
    Validates the JSON payload for /api/analyze route.
    Returns (is_valid, cleaned_text_or_error_message)
    """
    if not data or not isinstance(data, dict):
        return False, "Invalid JSON payload"
    
    if "text" not in data:
        return False, "Missing 'text' field in request body"
    
    raw_text = data.get("text")
    if not isinstance(raw_text, str):
        return False, "'text' field must be a string"
    
    cleaned = preprocess_text(raw_text)
    if not cleaned:
        return False, "'text' field cannot be empty or whitespace only"
    
    return True, cleaned
