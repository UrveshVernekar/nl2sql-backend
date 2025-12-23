def is_safe_sql(sql: str) -> bool:
    return sql.lower().startswith("select")