import typing
from urllib.parse import urljoin

from fastapi.routing import APIRoute
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

from fastapi2cli.parameters.get_params_for import get_parameters_for_route


def get_parameter_value(parameter_name: str, field_info: FieldInfo,
                        **http_parameters: typing.Any) -> typing.Any:
    """
    Get the value of a parameter from HTTP parameters.

    This function retrieves the value of a parameter from the provided HTTP parameters. It checks whether the parameter
    is required, and if not provided, it returns the default value defined in the field info.

    :param parameter_name: The name of the parameter to get the value of.
    :type parameter_name: str
    :param field_info: Information about the parameter field.
    :type field_info: FieldInfo
    :param http_parameters: HTTP parameters to retrieve the value from.
    :type http_parameters: typing.Any
    :return: The value of the parameter.
    :rtype: typing.Any
    :raises KeyError: If a required parameter is missing in the HTTP parameters.
    """
    if parameter_name in http_parameters:
        return http_parameters[parameter_name]
    elif field_info.is_required():
        raise KeyError(parameter_name)
    elif field_info.default is not PydanticUndefined:
        return field_info.default
    else:
        return field_info.default_factory()


def get_body(route: APIRoute, **http_parameters: typing.Any) -> BaseModel | None:
    """
    Get the body parameters for a given route.

    This function retrieves the body parameters for a given route from the provided HTTP parameters.

    :param route: The route for which to retrieve the body parameters.
    :type route: APIRoute
    :param http_parameters: HTTP parameters to retrieve the body parameters from.
    :type http_parameters: typing.Any
    :return: The body parameters.
    :rtype: BaseModel | None
    """
    if route.body_field is None:
        return None
    field_name = route.body_field.alias
    type_: type[BaseModel] = route.body_field.type_
    properties = {}
    for property_name, field_info in type_.model_fields.items():
        properties[property_name] = get_parameter_value(f"{field_name}_{property_name}", field_info, **http_parameters)
    return type_(**properties)


def get_parameters_values(parameter_definitions: dict[str, FieldInfo], **http_parameters):
    """
     Get the values of parameters from HTTP parameters.

     This function retrieves the values of parameters defined by the given parameter definitions from the provided
     HTTP parameters.

     :param parameter_definitions: Definitions of parameters to retrieve values for.
     :type parameter_definitions: dict[str, FieldInfo]
     :param http_parameters: HTTP parameters to retrieve values from.
     :type http_parameters: typing.Any
     :return: The values of the parameters.
     :rtype: dict[str, typing.Any]
     """
    return {
        parameter_name: get_parameter_value(parameter_name, field_info, **http_parameters)
        for parameter_name, field_info in parameter_definitions.items()
    }


def get_formatted_url(url: str, route: APIRoute, **http_parameters: typing.Any) -> str:
    """
    Get the formatted URL for a given route.

    This function formats the URL for a given route with the provided HTTP parameters.

    :param url: The base URL to format.
    :type url: str
    :param route: The route for which to format the URL.
    :type route: APIRoute
    :param http_parameters: HTTP parameters to use for formatting the URL.
    :type http_parameters: typing.Any
    :return: The formatted URL.
    :rtype: str
    """
    path_parameters = get_parameters_for_route(route, property_names_to_include=["path_params"])
    return urljoin(url, route.path).format(**get_parameters_values(path_parameters, **http_parameters))


def get_query_parameters(route: APIRoute, **http_parameters: typing.Any) -> dict[str, typing.Any]:
    """
     Get the query parameters for a given route.

     This function retrieves the query parameters for a given route from the provided HTTP parameters.

     :param route: The route for which to retrieve the query parameters.
     :type route: APIRoute
     :param http_parameters: HTTP parameters to retrieve the query parameters from.
     :type http_parameters: typing.Any
     :return: The query parameters.
     :rtype: dict[str, typing.Any]
     """
    query_parameters = get_parameters_for_route(route, property_names_to_include=["query_params"])
    return get_parameters_values(query_parameters, **http_parameters)


def get_header_parameters(route: APIRoute, **http_parameters: typing.Any) -> dict[str, typing.Any]:
    """
    Get the header parameters for a given route.

    This function retrieves the header parameters for a given route from the provided HTTP parameters.

    :param route: The route for which to retrieve the header parameters.
    :type route: APIRoute
    :param http_parameters: HTTP parameters to retrieve the header parameters from.
    :type http_parameters: typing.Any
    :return: The header parameters.
    :rtype: dict[str, typing.Any]
    """
    header_parameters = get_parameters_for_route(route, property_names_to_include=["header_params"])
    return get_parameters_values(header_parameters, **http_parameters)


def get_cookie_parameters(route: APIRoute, **http_parameters: typing.Any) -> dict[str, typing.Any]:
    """
    Get the cookie parameters for a given route.

    This function retrieves the cookie parameters for a given route from the provided HTTP parameters.

    :param route: The route for which to retrieve the cookie parameters.
    :type route: APIRoute
    :param http_parameters: HTTP parameters to retrieve the cookie parameters from.
    :type http_parameters: typing.Any
    :return: The cookie parameters.
    :rtype: dict[str, typing.Any]
    """
    cookie_parameters = get_parameters_for_route(route, property_names_to_include=["cookie_params"])
    return get_parameters_values(cookie_parameters, **http_parameters)
