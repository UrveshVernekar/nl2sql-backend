import uuid
from app.db.connection import get_connection


def create_chat(user_id: str, title: str):
    chat_id = str(uuid.uuid4())
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO chats (id, user_id, title)
        VALUES (%s, %s, %s)
        """,
        (chat_id, user_id, title)
    )

    conn.commit()
    cur.close()
    conn.close()
    return chat_id


def list_chats(user_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, title, created_at
        FROM chats
        WHERE user_id = %s
        ORDER BY updated_at DESC
        """,
        (user_id,)
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {"id": r[0], "title": r[1], "createdAt": r[2].timestamp()}
        for r in rows
    ]
    
    
def rename_chat(chat_id: str, user_id: str, title: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE chats
        SET title = %s, updated_at = NOW()
        WHERE id = %s AND user_id = %s
        """,
        (title, chat_id, user_id)
    )

    conn.commit()
    cur.close()
    conn.close()


def delete_chat(chat_id: str, user_id: str):
    conn = get_connection()
    cur = conn.cursor()

    # Messages first (FK safety)
    cur.execute(
        "DELETE FROM messages WHERE chat_id = %s",
        (chat_id,)
    )

    cur.execute(
        "DELETE FROM chats WHERE id = %s AND user_id = %s",
        (chat_id, user_id)
    )

    conn.commit()
    cur.close()
    conn.close()
    
    
def user_owns_chat(chat_id: str, user_id: int) -> bool:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT 1
        FROM chats
        WHERE id = %s AND user_id = %s
        """,
        (chat_id, user_id),
    )

    exists = cur.fetchone() is not None

    cur.close()
    conn.close()

    return exists