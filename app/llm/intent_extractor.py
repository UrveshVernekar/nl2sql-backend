from app.schema.metadata import SCHEMA_CONTEXT
from app.intent.schema import INTENT_SCHEMA
from app.llm.prompts import SYSTEM_PROMPT, build_user_prompt
from app.intent.models import NL2SQLIntent
from app.llm.client import client

import json
import os
from openai import RateLimitError


# =========================
# CONFIG
# =========================
USE_MOCK_LLM = True  # <-- toggle this


# =========================
# MOCK RESPONSE (DEV MODE)
# =========================
def mock_intent(user_query: str) -> NL2SQLIntent:
    mock_data = {
        "query_type": "select",
        "entities": {
            "primary": "orders",
            "joins": []
        },
        "output": {
            "metrics": [
                {
                    "field": "amount",
                    "aggregation": "sum",
                    "alias": "total_sales"
                }
            ]
        },
        "filters": [
            {
                "field": "order_date",
                "operator": "last_n_days",
                "value": 30
            }
        ],
        "group_by": [],
        "order_by": [],
        "limit": None
    }

    return NL2SQLIntent.model_validate(mock_data)


# =========================
# REAL LLM CALL
# =========================
def real_intent(user_query: str) -> NL2SQLIntent:
    user_prompt = build_user_prompt(
        schema_context=SCHEMA_CONTEXT,
        intent_schema=INTENT_SCHEMA,
        user_query=user_query
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    data = json.loads(response.choices[0].message.content)
    return NL2SQLIntent.model_validate(data)


# =========================
# PUBLIC API
# =========================
def extract_intent(user_query: str) -> NL2SQLIntent:
    if USE_MOCK_LLM:
        return mock_intent(user_query)

    try:
        return real_intent(user_query)

    except RateLimitError:
        raise RuntimeError(
            "LLM quota exceeded. Enable USE_MOCK_LLM or check billing."
        )

    except Exception as e:
        raise RuntimeError(f"Intent extraction failed: {str(e)}")
