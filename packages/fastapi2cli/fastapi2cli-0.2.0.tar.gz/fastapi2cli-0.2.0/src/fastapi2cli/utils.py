import types
import typing
from typing import Callable

from fastapi import FastAPI
from fastapi.routing import APIRoute


def get_route_for_function(fastapi_app: FastAPI, fun: Callable):
    """
    Get the route in FastAPI for a given function.

    :param fastapi_app: The FastAPI application where the function is registered as a route.
    :type fastapi_app: FastAPI
    :param fun: The function to get the route of.
    :type fun: Callable
    :return: The route of the given function.
    :rtype: APIRoute
    :raises ValueError: If the function is not registered inside the FastAPI app.
    """
    for route in fastapi_app.routes:
        if isinstance(route, APIRoute):
            if route.endpoint == fun:
                return route
    raise ValueError(fun)


def get_optional_type_value(type_: type) -> type:
    """
    Get the non-optional type from an Optional[type] or type | None.

    This function extracts the non-optional type from a type hint that represents either an Optional[type]
    or a Union[type, None]. It is used to handle the conversion of Optional[type] into type for compatibility
    with certain libraries or frameworks.

    :param type_: The type hint from which to extract the non-optional type.
    :type type_: type
    :return: The non-optional type.
    :rtype: type
    :raises TypeError: If the provided type hint does not match the expected format.
    """
    container_args = typing.get_args(type_)
    real_types = [t for t in container_args if t is not type(None)]
    if len(real_types) == 1:  # Optional[type] or type | None
        return real_types[0]
    else:
        raise TypeError(f"Union not supported yet")


def is_optional(field: type) -> bool:
    """
    Check if a type is optional.

    :param field: The type to check.
    :type field: type
    :return: True if the type is optional, False otherwise.
    :rtype: bool
    """
    return typing.get_origin(field) in [typing.Union, types.UnionType] and \
        type(None) in typing.get_args(field)
