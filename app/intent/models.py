from typing import List, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum


class QueryType(str, Enum):
    select = "select"


class Aggregation(str, Enum):
    sum = "sum"
    count = "count"
    avg = "avg"
    min = "min"
    max = "max"


class Operator(str, Enum):
    eq = "="
    ne = "!="
    gt = ">"
    lt = "<"
    gte = ">="
    lte = "<="
    between = "between"
    in_ = "in"
    like = "like"
    last_n_days = "last_n_days"


class OrderDirection(str, Enum):
    asc = "asc"
    desc = "desc"


class Join(BaseModel):
    table: str
    on: str


class Entities(BaseModel):
    primary: str
    joins: Optional[List[Join]] = []


class Metric(BaseModel):
    field: str
    aggregation: Aggregation
    alias: Optional[str] = None


class Output(BaseModel):
    metrics: Optional[List[Metric]] = []


class Filter(BaseModel):
    field: str
    operator: Operator
    value: Optional[Union[str, int, float, List, None]]


class OrderBy(BaseModel):
    field: str
    direction: OrderDirection


class NL2SQLIntent(BaseModel):
    query_type: QueryType = QueryType.select
    entities: Entities
    output: Output
    group_by: Optional[List[str]] = []
    filters: Optional[List[Filter]] = []
    order_by: Optional[List[OrderBy]] = []
    limit: Optional[int] = Field(default=None, ge=1, le=1000)
