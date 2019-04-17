from .errors import (ApiError, ErrorCodes)


def params(predicates, data):
    """
    Checks the validity of params using a dictionary of predicates.

    Args:
        predicates (dict): A dictionary of predicate functions.
        data (dict): data to validate

    Returns:
        None if all params are valid, raises a 400 ApiError otherwise
    """
    for key, predicate in predicates.items():
        if not predicate(data.get(key)):
            raise ApiError(
                f"Missing or invalid '{key}' parameter",
                400,
                ErrorCodes.INVALID_PARAMETER,
            )


def is_non_empty_string(value):
    return isinstance(value, str) and value.strip() != ''


def is_nil_or_non_empty_string(value):
    return value is None or is_non_empty_string(value)
