import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase

env_path = Path(__file__).resolve().parent.parent / "backend" / ".env"
load_dotenv(env_path)

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

driver.verify_connectivity()

print("✅ Connected to Neo4j Aura")

driver.close()