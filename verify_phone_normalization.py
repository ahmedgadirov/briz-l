
def normalize_phone(phone):
    """Normalize phone number to E.164-like format (digits only)"""
    if not phone:
        return ""
    # Remove +, spaces, dashes, and parentheses
    clean_phone = "".join(filter(str.isdigit, str(phone)))
    
    # If it starts with 0 (local Azerbaijan format), replace with 994
    if clean_phone.startswith("0") and len(clean_phone) == 10:
        clean_phone = "994" + clean_phone[1:]
    
    return clean_phone

test_cases = [
    ("+994 50 211 51 20", "994502115120"),
    ("994-55-551-24-00", "994555512400"),
    ("0502115120", "994502115120"),
    ("994502115120", "994502115120"),
    ("+1-123-456-7890", "11234567890"),
    (None, ""),
]

for inp, expected in test_cases:
    actual = normalize_phone(inp)
    status = "✅" if actual == expected else "❌"
    print(f"{status} Input: {inp} | Expected: {expected} | Actual: {actual}")
