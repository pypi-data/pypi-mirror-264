"""The sort model Flask integration.

Supports parsing a GridSortModel from Flask's request.args
"""

from typing import Optional
from zoneinfo import ZoneInfo

from flask import request
from typing_extensions import Literal


def get_grid_timezone_from_request(
    key: str = "timezone", model_format: Literal["json"] = "json"
) -> Optional[ZoneInfo]:
    """Retrieves a timezone from request.args.

    Currently, this only supports a JSON encoded model, but in the future the plan is
    to write a custom querystring parser to support nested arguments as JavaScript
    libraries like Axios create out of the box.

    Args:
        key (str): The key in the request args where the sort model should be parsed
            from. Defaults to "timezone".

    Raises:
        ValidationError: Raised when an invalid type was received.
        ValueError: Raised when an invalid model format was received.

    Returns:
        ZoneInfo: The parsed timezone.
    """
    if model_format == "json":
        value = request.args.get(key=key)
        return ZoneInfo(value) if value is not None else None
    raise ValueError(f"Invalid model format: {model_format}")
