import pandas as pd
from neo4j import GraphDatabase
from pathlib import Path
from dotenv import load_dotenv
import os

# -----------------------------
# Load Environment Variables
# -----------------------------
env_path = Path(__file__).resolve().parent.parent / "backend" / ".env"
load_dotenv(env_path)

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

# -----------------------------
# Read Dataset
# -----------------------------
df = pd.read_csv("data/drug_interactions.csv")

print(f"Rows Loaded: {len(df)}")

records = []

for _, row in df.iterrows():
    records.append({
        "drug1": str(row["Drug 1"]).strip(),
        "drug2": str(row["Drug 2"]).strip(),
        "description": str(row["Interaction Description"]).strip()
    })

BATCH_SIZE = 1000

query = """
UNWIND $rows AS row

MERGE (d1:Drug {name: row.drug1})
MERGE (d2:Drug {name: row.drug2})

MERGE (d1)-[r:INTERACTS_WITH]->(d2)

SET r.description = row.description
"""

with driver.session() as session:

    total = len(records)

    for i in range(0, total, BATCH_SIZE):

        batch = records[i:i+BATCH_SIZE]

        session.run(query, rows=batch)

        print(f"Imported {min(i+BATCH_SIZE,total)} / {total}")

print("Import Completed Successfully!")

driver.close()