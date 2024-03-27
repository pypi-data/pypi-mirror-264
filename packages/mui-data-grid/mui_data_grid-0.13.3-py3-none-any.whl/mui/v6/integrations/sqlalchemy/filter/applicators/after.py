"""The is after applicator applies the is after operator to the data."""

from datetime import datetime
from operator import gt
from typing import Any, Optional
from zoneinfo import ZoneInfo

from mui.v6.integrations.sqlalchemy.utils import is_timezone_aware


def apply_after_operator(column: Any, value: Any, timezone: Optional[ZoneInfo]) -> Any:
    """Handles applying the after x-data-grid operator to a column.

    Args:
        column (Any): The column the operator is being applied to, or equivalent
            property, expression, subquery, etc.
        value (Any): The value being filtered.

    Returns:
        Any: The column after applying the after filter using the provided value.
    """
    # if the column is after the received date, it will be greater than the
    # received date
    parsed = datetime.fromisoformat(value)
    parsed = (
        parsed.astimezone(timezone)
        if is_timezone_aware(parsed) and timezone is not None
        else parsed.replace(tzinfo=timezone)
    )
    return gt(column, parsed) if value is not None else column
