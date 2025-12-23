from app.db.connection import get_connection


def get_user_by_email(email: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, email, password_hash FROM users WHERE email = %s",
            (email,),
        )
        row = cur.fetchone()
        if not row:
            return None

        return {
            "id": row[0],
            "email": row[1],
            "password_hash": row[2],
        }
    finally:
        cur.close()
        conn.close()


def create_user(email: str, password_hash: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO users (email, password_hash)
            VALUES (%s, %s)
            RETURNING id
            """,
            (email, password_hash),
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id
    finally:
        cur.close()
        conn.close()


def get_user_by_id(user_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, email FROM users WHERE id = %s",
            (user_id,),
        )
        row = cur.fetchone()
        if not row:
            return None

        return {
            "id": row[0],
            "email": row[1],
        }
    finally:
        cur.close()
        conn.close()