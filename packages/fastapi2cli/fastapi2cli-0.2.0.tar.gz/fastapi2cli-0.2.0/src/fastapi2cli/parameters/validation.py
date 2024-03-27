from pydantic.fields import FieldInfo


def validate_parameter_consistency(new_parameter_name: str, new_parameter_value: FieldInfo,
                                   existing_parameters: dict[str, FieldInfo]):
    """
    Validate consistency of a new parameter with existing parameters.

    This function checks whether a new parameter being added to a dictionary of existing parameters
    is consistent with the types of parameters with the same name already present in the dictionary.

    :param new_parameter_name: The name of the new parameter to be validated.
    :type new_parameter_name: str
    :param new_parameter_value: Information about the new parameter to be validated.
    :type new_parameter_value: FieldInfo
    :param existing_parameters: Dictionary containing information about existing parameters.
    :type existing_parameters: dict[str, FieldInfo]
    :raises ValueError: If the new parameter conflicts with an existing parameter in terms of type.
    """
    if (new_parameter_name in existing_parameters and
            existing_parameters[new_parameter_name].annotation != new_parameter_value.annotation):
        raise ValueError(
            f"Multiple values for {new_parameter_value} that don't match each others: (existing one: "
            f"{existing_parameters[new_parameter_name]}, replacing one {new_parameter_value})")
