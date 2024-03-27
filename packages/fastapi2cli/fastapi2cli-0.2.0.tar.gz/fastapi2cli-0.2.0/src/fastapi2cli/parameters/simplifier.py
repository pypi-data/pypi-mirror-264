import typing

from pydantic import BaseModel
from pydantic.fields import FieldInfo

from fastapi2cli.parameters.validation import validate_parameter_consistency
from fastapi2cli.utils import get_optional_type_value, is_optional


def explode_parameter(parent_key: str, parent_type: type[BaseModel]) -> dict[str, FieldInfo]:
    """
    Explode parameters from a parent BaseModel type.

    Recursively explores the fields of a parent BaseModel type and returns a dictionary containing parameter names
    as keys and corresponding ModelField objects as values.

    :param parent_key: The key of the parent parameter.
    :type parent_key: str
    :param parent_type: The parent BaseModel type.
    :type parent_type: type[BaseModel]
    :return: A dictionary containing exploded parameters.
    :rtype: Dict[str, ModelField]
    """
    parameters = {}
    for key, field_info in parent_type.model_fields.items():
        type_ = field_info.annotation
        parameter_key = parent_key + "_" + key
        if isinstance(type_, type(BaseModel)):
            child_parameters = explode_parameter(parameter_key, type_)
            for child_parameter_name, child_parameter in child_parameters.items():
                validate_parameter_consistency(child_parameter_name, child_parameter, parameters)
            parameters.update(child_parameters)
        elif is_optional(type_):
            # typing only handle Optional[type] and not type | None we need to correct it here
            field_info.annotation = typing.Optional[get_optional_type_value(type_)]
            parameters[parameter_key] = field_info
        else:
            parameters[parameter_key] = field_info
    return parameters


def convert_parameters_to_typer_supported_format(original_parameters: dict[str, FieldInfo]) -> dict[str, FieldInfo]:
    """
    Convert parameters from an original dictionary into a dict of typer supported FieldInfo.

    Convert parameters by removing nested BaseModel types and returning a dictionary containing flattened parameters.
    Also, convert 'type | None' into Optional[type] as typer don't support the first format

    :param original_parameters: The original dictionary containing parameters.
    :type original_parameters: dict[str, ModelField]
    :return: A dictionary containing simplified parameters.
    :rtype: dict[str, ModelField]
    """
    parameters = {}
    for key, value in original_parameters.items():
        type_ = value.annotation
        if is_optional(type_):
            underlying_type = get_optional_type_value(type_)
            # should we handle Optional[BaseModel] other than loading them though json not required?
            # we could explode the model and mark the child as not required but that would require mapping all the
            # generated params with a conditional check that if one is present all the non required one in the model
            # should also be present. and i don't think typer handle that at all
            # if not isinstance(underlying_type,type(BaseModel)):
            #
            # typing only handle Optional[type] and not type | None we need to correct it here
            value.annotation = typing.Optional[underlying_type]
            parameters[key] = value

        elif isinstance(type_, type(BaseModel)):
            child_parameters = explode_parameter("-" + key, type_)
            for child_parameter_name, child_parameter in child_parameters.items():
                validate_parameter_consistency(child_parameter_name, child_parameter, parameters)
            parameters.update(child_parameters)
        else:
            parameters[key] = value
    return parameters
