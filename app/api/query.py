from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.llm.intent_extractor import extract_intent
from app.intent.validator import validate_intent_against_schema
from app.intent.ambiguity import detect_ambiguity
from app.sql.builder import PostgresSQLBuilder
from app.schema.metadata import SCHEMA_CONTEXT

from app.db.executor import execute_readonly_sql
from app.db.messages import add_message
from app.db.chats import user_owns_chat

from app.auth.deps import get_current_user
from app.db.utils import make_json_safe


router = APIRouter(prefix="/api/query", tags=["Query"])


class QueryRequest(BaseModel):
    query: str
    chat_id: str


@router.post("/")
def handle_query(
    body: QueryRequest,
    user=Depends(get_current_user),
):
    query = body.query
    chat_id = body.chat_id

    # 🔐 Security: verify ownership
    if not user_owns_chat(chat_id, user["id"]):
        raise HTTPException(status_code=403, detail="Forbidden")

    # 1️⃣ Save user message
    add_message(
        chat_id=chat_id,
        role="user",
        content=query,
    )

    # 2️⃣ Intent extraction
    intent = extract_intent(query)

    # 3️⃣ Schema validation
    errors = validate_intent_against_schema(intent, SCHEMA_CONTEXT)
    if errors:
        add_message(
            chat_id=chat_id,
            role="assistant",
            content="Your query could not be validated against the schema.",
        )
        return {"error": errors}

    # 4️⃣ Ambiguity detection
    questions = detect_ambiguity(intent)
    if questions:
        add_message(
            chat_id=chat_id,
            role="assistant",
            content="I need clarification before generating SQL.",
        )
        return {
            "clarification_required": True,
            "questions": questions,
        }

    # 5️⃣ Build SQL
    sql = PostgresSQLBuilder(intent).build()

    # 6️⃣ Execute SQL
    raw_results = execute_readonly_sql(sql)
    results = make_json_safe(raw_results)

    # 7️⃣ Save assistant message (IMPORTANT)
    add_message(
        chat_id=chat_id,
        role="assistant",
        content="Here is the SQL generated for your query:",
        sql=sql,
        results=results,
    )

    # 8️⃣ Return response for UI
    return {
        "sql": sql,
        "results": results,
    }