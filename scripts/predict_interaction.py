import joblib

# Load saved model and vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

print("=" * 50)
print("DRUG INTERACTION PREDICTOR")
print("=" * 50)

# User input
drug1 = input("Enter Drug 1: ").strip()
drug2 = input("Enter Drug 2: ").strip()

# Create text
text = drug1 + " " + drug2

# Convert into TF-IDF features
X = vectorizer.transform([text])

# Prediction
prediction = model.predict(X)[0]

# Probability scores
probabilities = model.predict_proba(X)[0]

# Highest confidence
confidence = max(probabilities) * 100

# Risk score mapping
if prediction == "High":
    risk_score = 90
    emoji = "🔴"

elif prediction == "Moderate":
    risk_score = 60
    emoji = "🟡"

else:
    risk_score = 25
    emoji = "🟢"

print("\n" + "=" * 50)
print("PREDICTION RESULT")
print("=" * 50)

print(f"\nDrug 1: {drug1}")
print(f"Drug 2: {drug2}")

print(f"\nPredicted Severity: {prediction} {emoji}")

print(f"Confidence Score: {confidence:.2f}%")

print(f"Risk Score: {risk_score}/100")

print("\nDetailed Probabilities:")

for cls, prob in zip(model.classes_, probabilities):
    print(f"{cls}: {prob*100:.2f}%")

print("\n" + "=" * 50)