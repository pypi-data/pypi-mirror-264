import typing

from pydantic_core import Url

HTTP_SCHEMES = ["http", "https"]


def parse_url(value: str, valid_schemes: list[str] = None) -> str:
    """
    Parse a URL and return it if valid.

    This function parses the given URL string and validates its scheme against the list of valid schemes. If the URL
    scheme is not in the list of valid schemes, a ValueError is raised.

    :param value: The URL string to parse.
    :type value: str
    :param valid_schemes: The list of schemes to allow (default is ['http', 'https']).
    :type valid_schemes: list[str], optional
    :return: The parsed URL as a string.
    :rtype: str
    :raises ValueError: If the URL does not have a valid scheme.
    """
    if valid_schemes is None:
        valid_schemes = HTTP_SCHEMES
    parsed_result = Url(value)
    if parsed_result.scheme not in valid_schemes:
        raise ValueError(f"{value=} does not have a valid scheme ({'|'.join(valid_schemes)})")
    return str(parsed_result)


def make_parse_literal(container_args: typing.Sequence[str]):
    """
    Create a function to validate a value against a list of allowed literals.

    This function returns a validation function that checks if a given value is in the provided list of literals. If
    the value is not in the list, a ValueError is raised.

    :param container_args: The list of allowed literals.
    :type container_args: typing.Sequence[str]
    :return: The validation function.
    :rtype: typing.Callable[[str], str]
    """

    def validate_value(value: str):
        if value in container_args:
            return value
        raise ValueError(f"{value=} is not a valid value. Allowed values: {','.join(container_args)}")

    validate_value.__name__ = "|".join(container_args)
    return validate_value
