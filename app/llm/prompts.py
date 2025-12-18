SYSTEM_PROMPT = """
You are an expert data analyst.

Your task is to convert a natural language question into a structured JSON intent
that strictly follows the provided schema.

Rules:
- Output ONLY valid JSON.
- Do NOT generate SQL.
- Use ONLY tables and columns provided in the schema.
- Do NOT invent tables, columns, or joins.
- If information is ambiguous or missing, set the corresponding value to null.
- If a join is required, include it explicitly.
- Only generate SELECT queries (read-only).

If the question cannot be answered using the schema, return:
{
  "error": "UNANSWERABLE"
}
""".strip()


def build_user_prompt(
    schema_context: str,
    intent_schema: str,
    user_query: str
) -> str:
    return f"""
Database schema:
{schema_context}

Intent schema:
{intent_schema}

User question:
{user_query}
""".strip()
