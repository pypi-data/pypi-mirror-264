"""The is_ applicator applies the is operator to the data.

Meant as an equality check.
"""

from datetime import date, datetime, time
from operator import eq
from typing import Any

from mui.v5.integrations.sqlalchemy.utils import get_python_type_from_column


def apply_is_operator(column: Any, value: Any) -> Any:
    """Handles applying the is x-data-grid operator to a column.

    The is operator requires special handling when differentiating between data
    types.

    Args:
        column (Any): The column the operator is being applied to, or equivalent
            property, expression, subquery, etc.
        value (Any): The value being filtered.

    Returns:
        Any: The column after applying the is filter using the provided value.
    """
    python_type = get_python_type_from_column(column=column)

    if python_type in {datetime, time, date} and value is not None:
        return eq(column, datetime.fromisoformat(value))
    if python_type in {bool} and value is not None:
        # "" is used to represent "any" in MUI v5
        if value in {"", "any"}:
            return column.in_((True, False))
        elif value == "true":
            return eq(column, True)
        elif value == "false":
            return eq(column, False)
        else:
            raise ValueError(f"Unexpected boolean filter value received: {value}")
    return eq(column, value)
