from logging import getLogger
from typing import Literal
from typing import Sequence

from fastapi.dependencies.models import Dependant
from fastapi.params import Security, Depends
from fastapi.routing import APIRoute
from pydantic.fields import FieldInfo

from fastapi2cli.parameters.validation import validate_parameter_consistency

logger = getLogger(__name__)

AllowedPropertyName = Literal["path_params", "query_params", "header_params", "cookie_params", "body_params"]


def _get_parameters_for_dependency_own_properties(
        dependency: Dependant,
        property_names_to_include: Sequence[AllowedPropertyName]
) -> dict[str, FieldInfo]:
    """
    Retrieve parameters associated with a dependency's own properties.

    :param dependency: The dependency object for which parameters are retrieved.
    :type dependency: Dependant
    :param property_names_to_include: A list of property names to include in parameter retrieval.
    :type property_names_to_include: Sequence[AllowedPropertyName]
    :return: A dictionary containing parameter names as keys and corresponding FieldInfo objects as values.
    :rtype: Dict[str, FieldInfo]
    """
    parameters: dict[str, FieldInfo] = {}
    for property_name in property_names_to_include:
        for dependency_parameter in getattr(dependency, property_name):
            validate_parameter_consistency(dependency_parameter.alias, dependency_parameter.field_info, parameters)
            parameters[dependency_parameter.alias] = dependency_parameter.field_info
    return parameters


def _get_parameters_for_dependency_child_dependencies(
        parameters: dict[str, FieldInfo],
        dependency: Dependant,
        property_names_to_include: Sequence[AllowedPropertyName]):
    """
    Retrieve parameters associated with a dependency's child dependencies.

    :param parameters: The dictionary containing previously retrieved parameters.
    :type parameters: Dict[str, FieldInfo]
    :param dependency: The dependency object for which parameters are retrieved.
    :type dependency: Dependant
    :param property_names_to_include: A list of property names to include in parameter retrieval.
    :type property_names_to_include: Sequence[AllowedPropertyName]
    """
    for dependency in dependency.dependencies:
        child_dependency_parameters = get_parameters_for_dependency(dependency, property_names_to_include)
        for child_parameter_name, child_parameter_type in child_dependency_parameters.items():
            validate_parameter_consistency(child_parameter_name, child_parameter_type, parameters)
        parameters.update(child_dependency_parameters)
    return parameters


def get_parameters_for_dependency(
        dependency: Dependant,
        property_names_to_include: Sequence[AllowedPropertyName] = None
) -> dict[str, FieldInfo]:
    """
    Recursively retrieves parameters associated with a dependency.

    This function traverses through the dependency tree and collects all parameters associated with the dependency,
    including path, query, header, cookie, and body parameters.

    :param dependency: The dependency object for which parameters are retrieved.
    :type dependency: Dependant
    :param property_names_to_include: A list of property names to include in parameter retrieval. Default is None,
                                    which includes all properties (path_params, query_params, header_params,
                                    cookie_params, body_params).
    :type property_names_to_include: Sequence[AllowedPropertyName], optional
    :return: A dictionary containing parameter names as keys and corresponding ModelField objects as values.
    :rtype: Dict[str, FieldInfo]
    """
    if property_names_to_include is None:
        property_names_to_include = ["path_params", "query_params", "header_params", "cookie_params", "body_params"]
    parameters = _get_parameters_for_dependency_own_properties(dependency, property_names_to_include)
    return _get_parameters_for_dependency_child_dependencies(parameters, dependency, property_names_to_include)


def get_parameters_for_route(
        route: APIRoute,
        *,
        property_names_to_include: Sequence[AllowedPropertyName] = None
) -> dict[str, FieldInfo]:
    """
    Retrieves parameters associated with a route.

    This function collects all parameters associated with a given route, including those defined in the route
    dependency tree.

    :param route: The route for which parameters are retrieved.
    :type route: APIRoute
    :param property_names_to_include: A list of property names to include in parameter retrieval. Default is None,
                                which includes all properties (path_params, query_params, header_params,
                                cookie_params, body_params).
    :type property_names_to_include: Sequence[AllowedPropertyName], optional
    :return: A dictionary containing parameter names as keys and corresponding ModelField objects as values.
    :rtype: Dict[str, ModelField]
    """
    parameters = get_parameters_for_dependency(route.dependant, property_names_to_include)
    return parameters
