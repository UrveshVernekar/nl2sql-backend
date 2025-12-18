INTENT_SCHEMA = """
{
  "query_type": "select",
  "entities": {
    "primary": "string",
    "joins": [
      { "table": "string", "on": "string" }
    ]
  },
  "output": {
    "metrics": [
      { "field": "string", "aggregation": "sum|count|avg|min|max", "alias": "string" }
    ]
  },
  "group_by": ["string"],
  "filters": [
    { "field": "string", "operator": "=|!=|>|<|>=|<=|between|in|like|last_n_days", "value": "any|null" }
  ],
  "order_by": [
    { "field": "string", "direction": "asc|desc" }
  ],
  "limit": "number|null"
}
"""
