import pandas as pd

# CSV file read karna
df = pd.read_csv("data/drug_interactions.csv")

# User input lena
drug1 = input("Enter Drug 1: ")
drug2 = input("Enter Drug 2: ")

# Interaction search
result = df[
    ((df["drug1"] == drug1) &
     (df["drug2"] == drug2))
]

# Output
if len(result) > 0:
    print("\n⚠ Interaction Found!")
    print("Risk:", result.iloc[0]["risk"])
    print("Effect:", result.iloc[0]["effect"])
else:
    print("\n✅ No Interaction Found")