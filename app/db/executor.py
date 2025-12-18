from app.db.connection import get_connection


def execute_readonly_sql(sql: str):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(sql)

        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        return {
            "columns": columns,
            "rows": rows
        }

    finally:
        cursor.close()
        conn.close()
