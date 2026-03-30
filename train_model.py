import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

# Load dataset
data = pd.read_csv("disaster_data.csv")

X = data["text"]
y = data["label"]

# ML Pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english")),
    ("clf", MultinomialNB())
])

# Train model
model.fit(X, y)

# Save trained model
joblib.dump(model, "models/disaster_classifier.pkl")

print("✅ ML model trained and saved successfully")
