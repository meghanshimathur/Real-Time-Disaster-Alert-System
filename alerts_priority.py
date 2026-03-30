# backend/severity.py

def calculate_severity(disaster_type, title):
    """
    Determines severity level using simple rules.
    """

    text = title.lower()

    if disaster_type == "earthquake":
        for word in text.split():
            try:
                if float(word) >= 4.0:
                    return "HIGH"
            except:
                pass
        return "MEDIUM"

    if disaster_type in ["cyclone", "fire"]:
        return "HIGH"

    if disaster_type == "flood":
        if "severe" in text or "heavy" in text:
            return "HIGH"
        return "MEDIUM"

    if disaster_type == "landslide":
        return "HIGH"

    return "LOW"


def priority_score(severity):
    """
    Converts severity to numeric priority.
    """

    scores = {
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1
    }

    return scores.get(severity, 1)
