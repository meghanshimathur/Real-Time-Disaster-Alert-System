from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

# Cache to reduce API calls
advice_cache = {}


def build_prompt(disaster_type, severity, location):
    """
    Builds a safe prompt for Gemini.
    """
    return f"""
    A {severity} level {disaster_type} has occurred in {location}.
    Provide 3 short and clear safety instructions.
    """


def fallback_advice(disaster_type):
    """
    Rule-based advice if Gemini quota is exhausted.
    """
    advice_map = {
        "earthquake": "Drop, cover, and hold on.",
        "flood": "Move to higher ground and avoid floodwater.",
        "cyclone": "Stay indoors and follow evacuation orders.",
        "fire": "Evacuate immediately and avoid smoke.",
        "landslide": "Move away from slopes and unstable areas."
    }
    return advice_map.get(disaster_type, "Stay alert and follow official instructions.")


def advisory_agent(disaster_type, severity, location):
    """
    Generates safety advice using Gemini with caching.
    """

    key = f"{disaster_type}_{severity}"

    if key in advice_cache:
        return advice_cache[key]


    try:
        prompt = build_prompt(disaster_type, severity, location)

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
    )

        advice = response.choices[0].message.content

    except Exception:
        advice = fallback_advice(disaster_type)

    advice_cache[key] = advice
    return advice

