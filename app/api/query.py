from fastapi import APIRouter
from app.llm.intent_extractor import extract_intent
from app.intent.validator import validate_intent_against_schema
from app.intent.ambiguity import detect_ambiguity
from app.sql.builder import PostgresSQLBuilder
from app.schema.metadata import SCHEMA_CONTEXT
from app.db.executor import execute_readonly_sql

router = APIRouter()

@router.post("/query")
def handle_query(payload: dict):
    user_query = payload["query"]

    intent = extract_intent(user_query)

    errors = validate_intent_against_schema(intent, SCHEMA_CONTEXT)
    if errors:
        return {"error": errors}

    questions = detect_ambiguity(intent)
    if questions:
        return {
            "clarification_required": True,
            "questions": questions
        }

    sql = PostgresSQLBuilder(intent).build()
    results = execute_readonly_sql(sql)
    
    # return {"sql": sql}
    return {
        "sql": sql,
        "results": results
    }