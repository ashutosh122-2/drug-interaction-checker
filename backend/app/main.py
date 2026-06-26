from fastapi import FastAPI
from backend.app.database import driver
from backend.app.ml_model import predict_interaction
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_risk_score(severity):

    if severity == "High":
        return 90

    elif severity == "Moderate":
        return 60

    return 25


def get_severity(description):

    text = description.lower()

    if "severe" in text:
        return "High"

    elif "increase" in text:
        return "Moderate"

    else:
        return "Low"


@app.get("/")
def home():
    return {
        "message": "Drug Interaction API Running"
    }


@app.get("/drugs/count")
def drug_count():

    query = """
    MATCH (d:Drug)
    RETURN count(d) AS total
    """

    with driver.session() as session:
        result = session.run(query)
        record = result.single()

    return {
        "total_drugs": record["total"]
    }


@app.get("/drug/{drug_name}")
def get_drug(drug_name: str):

    query = """
    MATCH (d:Drug)
    WHERE toLower(d.name) = toLower($drug_name)
    RETURN d.name AS name
    LIMIT 1
    """

    with driver.session() as session:

        result = session.run(
            query,
            drug_name=drug_name
        )

        record = result.single()

    if record:
        return {
            "drug": record["name"]
        }

    return {
        "message": "Drug Not Found"
    }



@app.get("/interaction")
def check_interaction(drug1: str, drug2: str):

    query = """
    MATCH (d1:Drug)-[r:INTERACTS_WITH]-(d2:Drug)

    WHERE
    (
        toLower(d1.name)=toLower($drug1)
        AND
        toLower(d2.name)=toLower($drug2)
    )
    OR
    (
        toLower(d1.name)=toLower($drug2)
        AND
        toLower(d2.name)=toLower($drug1)
    )

    RETURN
        d1.name AS drug1,
        d2.name AS drug2,
        r.description AS description

    LIMIT 1
    """

    with driver.session() as session:
        record = session.run(
            query,
            drug1=drug1,
            drug2=drug2
        ).single()

    if record:

        description = record["description"]

        severity = get_severity(description)

        risk_score = get_risk_score(severity)

        return {
            "interaction_found": True,
            "drug1": record["drug1"],
            "drug2": record["drug2"],
            "severity": severity,
            "risk_score": risk_score,
            "description": description
        }

    prediction = predict_interaction(drug1, drug2)

    return {
        "interaction_found": False,
        "message": "No Interaction Found In Database",
        "ml_prediction": prediction["prediction"],
        "confidence": prediction["confidence"]
    }
    
@app.get("/drugs/search")
def search_drugs(search_term: str):

    cypher_query = """
    MATCH (d:Drug)
    WHERE toLower(d.name)
    CONTAINS toLower($search_term)

    RETURN d.name AS name

    LIMIT 10
    """

    with driver.session() as session:

        result = session.run(
            cypher_query,
            search_term=search_term
        )

        drugs = [
            record["name"]
            for record in result
        ]

    return drugs
@app.get("/dashboard/stats")
def dashboard_stats():

    with driver.session() as session:

        total_drugs = session.run("""
            MATCH (d:Drug)
            RETURN count(d) AS count
        """).single()["count"]

        total_interactions = session.run("""
            MATCH ()-[r:INTERACTS_WITH]->()
            RETURN count(r) AS count
        """).single()["count"]

    return {
        "total_drugs": total_drugs,
        "total_interactions": total_interactions,
        "ai_model": "Active"
    }
    
@app.get("/graph")
def get_graph(drug1: str, drug2: str):

    with driver.session() as session:

        query = """
        MATCH (d1:Drug)-[r:INTERACTS_WITH]-(d2:Drug)

        WHERE
        (
            toLower(d1.name)=toLower($drug1)
            AND
            toLower(d2.name)=toLower($drug2)
        )
        OR
        (
            toLower(d1.name)=toLower($drug2)
            AND
            toLower(d2.name)=toLower($drug1)
        )

        RETURN
        d1.name AS drug1,
        d2.name AS drug2,
        r.description AS description

        LIMIT 1
        """

        result = session.run(
            query,
            drug1=drug1,
            drug2=drug2
        ).single()

        if result is None:
            return {
                "nodes": [],
                "edges": []
            }

        return {

            "nodes": [

                {
                    "id": result["drug1"],
                    "label": result["drug1"]
                },

                {
                    "id": result["drug2"],
                    "label": result["drug2"]
                }

            ],

            "edges": [

                {
                    "id": "1",
                    "source": result["drug1"],
                    "target": result["drug2"],
                    "label": result["description"]
                }

            ]
        }