class PostgresSQLBuilder:
    def __init__(self, intent):
        self.intent = intent


    def build(self) -> str:
        parts = [
            self._select(),
            self._from(),
            self._where(),
            self._group_by(),
            self._order_by(),
            self._limit(),
        ]

        # remove None parts
        return " ".join(p for p in parts if p)


    def _select(self):
        metrics = []

        for m in self.intent.output.metrics or []:
            expr = f"{m.aggregation.upper()}({m.field})"
            if m.alias:
                expr += f" AS {m.alias}"
            metrics.append(expr)

        if not metrics:
            return None

        return "SELECT " + ", ".join(metrics)


    def _from(self):
        return f"FROM {self.intent.entities.primary}"


    def _where(self):
        if not self.intent.filters:
            return None

        clauses = []
        for f in self.intent.filters:
            if f.operator == "last_n_days":
                clauses.append(
                    f"{f.field} >= CURRENT_DATE - INTERVAL '{f.value} days'"
                )
            else:
                clauses.append(
                    f"{f.field} {f.operator} '{f.value}'"
                )

        return "WHERE " + " AND ".join(clauses)


    def _group_by(self):
        if not self.intent.group_by:
            return None
        return "GROUP BY " + ", ".join(self.intent.group_by)


    def _order_by(self):
        if not self.intent.order_by:
            return None
        return "ORDER BY " + ", ".join(
            f"{o.field} {o.direction.upper()}"
            for o in self.intent.order_by
        )


    def _limit(self):
        if not self.intent.limit:
            return None
        return f"LIMIT {self.intent.limit}"