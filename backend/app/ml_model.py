from pathlib import Path
import joblib

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load ML model
model = joblib.load(BASE_DIR / "model.pkl")

# Load TF-IDF vectorizer
vectorizer = joblib.load(BASE_DIR / "vectorizer.pkl")


def predict_interaction(drug1, drug2):

    text = f"{drug1} {drug2}"

    X = vectorizer.transform([text])

    prediction = model.predict(X)[0]

    probabilities = model.predict_proba(X)[0]

    confidence = max(probabilities) * 100

    return {
        "prediction": prediction,
        "confidence": round(confidence, 2),
    }