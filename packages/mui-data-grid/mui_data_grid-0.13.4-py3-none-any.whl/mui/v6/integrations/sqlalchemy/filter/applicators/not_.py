"""The is not applicator applies the is not operator to the data."""

from datetime import date, datetime, time
from operator import ne
from typing import Any, Optional
from zoneinfo import ZoneInfo

from mui.v6.integrations.sqlalchemy.utils import (
    get_python_type_from_column,
    is_timezone_aware,
)


def apply_not_operator(column: Any, value: Any, timezone: Optional[ZoneInfo]) -> Any:
    """Handles applying the not x-data-grid operator to a column.

    The not operator exists on enum selections as well as datetimes. Care
    needs to be given as a result.

    Args:
        column (Any): The column the operator is being applied to, or equivalent
            property, expression, subquery, etc.
        value (Any): The value being filtered.

    Returns:
        Any: The column after applying the is filter using the provided value.
    """
    python_type = get_python_type_from_column(column=column)

    if python_type in {datetime, time, date} and value is not None:
        parsed = datetime.fromisoformat(value)
        parsed = (
            parsed.astimezone(timezone)
            if is_timezone_aware(parsed) and timezone is not None
            else parsed.replace(tzinfo=timezone)
        )
        return ne(column, parsed)
    return ne(column, value)
