import joblib

model = joblib.load("model.pkl")

vectorizer = joblib.load("vectorizer.pkl")


def predict_interaction(drug1, drug2):

    text = drug1 + " " + drug2

    X = vectorizer.transform([text])

    prediction = model.predict(X)[0]

    probabilities = model.predict_proba(X)[0]

    confidence = max(probabilities) * 100

    return {
        "prediction": prediction,
        "confidence": round(confidence, 2)
    }