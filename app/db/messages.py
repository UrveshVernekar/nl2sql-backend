import uuid
import json
from app.db.connection import get_connection
from app.db.utils import make_json_safe


def add_message(chat_id, role, content, sql=None, results=None):
    conn = get_connection()
    cur = conn.cursor()
    
    safe_results = make_json_safe(results) if results else None

    cur.execute(
        """
        INSERT INTO messages (id, chat_id, role, content, sql, results)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            str(uuid.uuid4()),
            chat_id,
            role,
            content,
            sql,
            json.dumps(safe_results) if safe_results else None,
        ),
    )

    conn.commit()
    cur.close()
    conn.close()


def list_messages(chat_id: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT role, content, sql, results
        FROM messages
        WHERE chat_id = %s
        ORDER BY created_at ASC
        """,
        (chat_id,)
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    messages = []
    for r in rows:
        messages.append({
            "role": r[0],
            "content": r[1],
            "sql": r[2],
            "results": r[3],
        })

    return messages