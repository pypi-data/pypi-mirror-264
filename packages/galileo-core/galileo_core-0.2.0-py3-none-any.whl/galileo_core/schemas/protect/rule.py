from enum import Enum
from typing import Union

from pydantic import BaseModel, Field

ValueType = Union[int, bool, str, float, None]


class RuleOperator(str, Enum):
    gt = "gt"
    lt = "lt"
    gte = "gte"
    lte = "lte"
    eq = "eq"
    neq = "neq"
    contains = "contains"


class Rule(BaseModel):
    metric: str = Field(description="Name of the metric.")
    operator: RuleOperator = Field(description="Operator to use for comparison.")
    target_value: ValueType = Field(description="Value to compare with for this metric (right hand side).")
