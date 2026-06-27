import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load backend/.env
env_path = Path(__file__).resolve().parent.parent / ".env"

print("ENV PATH =", env_path)
print("ENV EXISTS =", env_path.exists())

load_dotenv(dotenv_path=env_path)

# Read variables from .env
URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

print("URI =", repr(URI))
print("USERNAME =", repr(USERNAME))
print("PASSWORD LENGTH =", len(PASSWORD) if PASSWORD else 0)

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
) 
driver.verify_connectivity()

print("✅ Connected to Neo4j Aura")