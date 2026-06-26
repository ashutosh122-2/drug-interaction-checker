import pandas as pd

# Load Dataset
df = pd.read_csv("data/drug_interactions.csv")

print("Rows:", len(df))

# Create Labels
def get_label(text):

    text = str(text).lower()

    if "severe" in text:
        return "High"

    elif "increase" in text:
        return "Moderate"

    else:
        return "Low"

# Severity Column
df["severity"] = df["Interaction Description"].apply(get_label)

# Text Feature
df["text"] = (
    df["Drug 1"] + " " +
    df["Drug 2"] + " " +
    df["Interaction Description"]
)

# Preview Data
print(
    df[
        [
            "Drug 1",
            "Drug 2",
            "Interaction Description",
            "severity"
        ]
    ].head(10)
)

# TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(df["text"])

print("\nTF-IDF Shape:", X.shape)

# Target Variable
y = df["severity"]

# Train Test Split
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Random Forest Model
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=20,
    random_state=42
)

# Training
model.fit(X_train, y_train)

print("\nTraining Complete")

# Prediction on Test Data
y_pred = model.predict(X_test)

# Accuracy
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

# Save Model
import joblib

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("\nModel Saved")