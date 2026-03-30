# backend/classification.py
'''
from transformers import pipeline

# Load zero-shot classification model
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

DISASTER_LABELS = ["earthquake","flood",
    "cyclone","fire",
    "landslide","not a disaster"
]


def classify_alert(title):
    """
    Classifies an alert into disaster categories.
    """

    result = classifier(title, DISASTER_LABELS)

    return {
        "disaster_type": result["labels"][0],
        "confidence": round(result["scores"][0], 2)
    }'''
import joblib

# Load trained ML model (Naive Bayes + TF-IDF)
model = joblib.load("models/disaster_classifier.pkl")


def classify_alert(text):
    """
    Classifies disaster type using trained ML model
    """

    prediction = model.predict([text])[0]

    return {
        "disaster_type": prediction
    }
