from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "Ashu@123"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)
def analyze_risk(description):

    description = description.lower()

    score = 0

    # High Risk Keywords
    high_keywords = [
        "fatal",
        "contraindicated",
        "life-threatening",
        "serious",
        "severe"
    ]

    # Medium Risk Keywords
    medium_keywords = [
        "increase",
        "adverse",
        "risk",
        "toxicit",
        "bleeding",
        "cardiotoxic"
    ]

    # Low Risk Keywords
    low_keywords = [
        "decrease",
        "reduce",
        "lower"
    ]

    for word in high_keywords:
        if word in description:
            score += 40

    for word in medium_keywords:
        if word in description:
            score += 20

    for word in low_keywords:
        if word in description:
            score += 5

    if score >= 60:
        severity = "HIGH 🔴"
    elif score >= 20:
        severity = "MODERATE 🟡"
    else:
        severity = "LOW 🟢"

    return severity, score

drug1 = input("Enter Drug 1: ").strip()
drug2 = input("Enter Drug 2: ").strip()


query = """
MATCH (d1:Drug)-[r:INTERACTS_WITH]-(d2:Drug)

WHERE
(
toLower(d1.name)=toLower($drug1)
AND toLower(d2.name)=toLower($drug2)
)
OR
(
toLower(d1.name)=toLower($drug2)
AND toLower(d2.name)=toLower($drug1)
)

RETURN r.description AS description
LIMIT 1
"""

with driver.session() as session:

    result = session.run(
        query,
        drug1=drug1,
        drug2=drug2
    )

    record = result.single()
if record:

    description = record["description"]

    severity, score = analyze_risk(description)

    print("\nRisk Score:", score, "/100")
    print("\nSeverity:", severity)

    print("\nSeverity:", severity)

    print("\nDescription:")
    print(description)
    
else:
        print("\n✅ No Interaction Found")

driver.close()