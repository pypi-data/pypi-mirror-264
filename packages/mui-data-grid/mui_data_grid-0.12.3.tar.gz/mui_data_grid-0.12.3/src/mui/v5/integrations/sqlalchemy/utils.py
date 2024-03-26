from contextlib import suppress
from typing import Any


def get_python_type_from_column(column: Any) -> Any:
    """Retrieve the python_type value for a SQLAlchemy column.

    This is used to ensure that we can retrieve the python_type from both native
    datatypes in SQLAlchemy as well as custom data types implemented using the
    TypeDecorator class, as described in the documentation:

    https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator
    """
    with suppress(AttributeError, NotImplementedError):
        # built-in types and type decorators
        return column.type.python_type
    with suppress(AttributeError, NotImplementedError):
        # if implementing a type decorator without a python type
        return column.type.impl.python_type
    return None
