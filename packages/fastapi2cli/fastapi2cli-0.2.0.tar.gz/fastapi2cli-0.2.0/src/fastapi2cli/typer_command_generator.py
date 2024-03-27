import inspect
import json
import types
import typing
from datetime import datetime
from enum import EnumType
from ipaddress import IPv6Address, IPv4Address
from pathlib import Path
from typing import Callable, Any, Annotated
from uuid import UUID

import typer
from pydantic import HttpUrl, IPvAnyAddress, BaseModel
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined, Url

from fastapi2cli.parsers import parse_url, make_parse_literal
from fastapi2cli.utils import get_optional_type_value

RequestCaller = Callable[..., Any]


def get_inspect_signature(fun: RequestCaller, annotations: dict[str, type],
                          defaults: dict[str, Any]) -> inspect.Signature:
    """
    Get an inspected signature for a function.

    Constructs an inspected signature for a given function based on provided annotations and default values.

    :param fun: The function to inspect.
    :type fun: RequestCaller
    :param annotations: Dictionary containing parameter names and their corresponding annotations.
    :type annotations: Dict[str, type]
    :param defaults: Dictionary containing parameter names and their default values.
    :type defaults: Dict[str, Any]
    :return: The inspected signature for the function.
    :rtype: inspect.Signature
    """
    signature = inspect.signature(fun)
    parameters = []
    for name in annotations:
        if name in defaults:
            parameters.append(inspect.Parameter(name, inspect.Parameter.KEYWORD_ONLY, default=defaults[name],
                                                annotation=annotations[name]))
        else:
            parameters.append(inspect.Parameter(name, inspect.Parameter.KEYWORD_ONLY, annotation=annotations[name]))
    return signature.replace(parameters=parameters)


TYPER_SUPPORTED_TYPES = [str, int, float, bool, datetime, UUID, Path]


class TyperCommandGenerator:
    """
    Generate Typer commands from annotated functions.

    This class is responsible for generating Typer commands from functions with annotated parameters. It inspects the
    annotations and default values of parameters to construct Typer commands with appropriate options and arguments.

    :param additional_parsers: Additional parsers for custom types.
    :type additional_parsers: dict[type, Callable[[str], Any]]
    """
    parsers = {
        HttpUrl: parse_url,
        Url: parse_url,
        IPvAnyAddress: IPvAnyAddress,
        IPv4Address: IPv4Address,
        IPv6Address: IPv6Address,
        bytes: bytes
    }

    def __init__(self, additional_parsers: dict[type, Callable[[str], Any]] = None):
        """
        Initialize TyperCommandGenerator.

        :param additional_parsers: Additional parsers for custom types.
        :type additional_parsers: dict[type, Callable[[str], Any]]
        """
        if additional_parsers is None:
            additional_parsers = {}
        self.additional_parsers = additional_parsers

    def get_parser_for_complex_type(self, type_: type):
        """
        Get parser for a complex type.

        This method retrieves a parser for a complex type, such as lists, dictionaries, or unions.

        :param type_: The complex type to get a parser for.
        :type type_: type
        :return: The parser function.
        :rtype: Callable[[str], Any]
        """
        container_type = typing.get_origin(type_)
        container_args = typing.get_args(type_)

        if container_type in [typing.Union, types.UnionType]:
            return self.get_parser_for_type(get_optional_type_value(type_))
        elif container_type is typing.Literal:
            return make_parse_literal(container_args)
        elif container_type in [typing.List, list] or type_ is list:
            if len(container_args) == 0:
                return None  # we handle list type with no params as a list of str so no need to give a custom parser
            else:
                # if list[type] it will be handled like Optional[type]
                # otherwise handle it like a Union (which is not handled ATM)
                return self.get_parser_for_type(typing.Union[*container_args])
        elif container_type in [typing.Dict, dict] or type_ is dict:
            if len(container_args) == 0:
                return json.loads
            else:
                # TODO handle type coercion in loaded dict
                return json.loads
        else:
            raise TypeError(type_)

    def get_parser_for_type(self, type_: type) -> Callable[[str], Any] | None:
        """
        Get parser for a specific type.

        This method retrieves a parser for a specific type.

        :param type_: The type to get a parser for.
        :type type_: type
        :return: The parser function.
        :rtype: Callable[[str], Any] | None
        """
        if type_ in self.additional_parsers:
            return self.additional_parsers[type_]
        elif type_ in TYPER_SUPPORTED_TYPES:
            return None
        elif type_ in TyperCommandGenerator.parsers:
            return TyperCommandGenerator.parsers[type_]
        elif isinstance(type_, EnumType):
            return None
        elif isinstance(type_, type(BaseModel)):
            type_: type[BaseModel]
            return type_.model_validate_json
        else:
            return self.get_parser_for_complex_type(type_)

    def get_proxy_for_parameter(self, value: FieldInfo, is_option: bool = False):
        """
        Get Typer option/argument proxy for a parameter.

        This method constructs a Typer option/argument proxy for a given parameter.

        :param value: The field info of the parameter.
        :type value: FieldInfo
        :param value: force the generation of an option instead of a parameter even if required.
        :type is_option: bool, optional
        :return: The Typer option/argument proxy.
        :rtype: typer.Option | typer.Argument
        """
        kwargs = {
            "help": value.description,
            "parser": self.get_parser_for_type(value.annotation)
        }
        if value.is_required() and not is_option:
            return typer.Argument(**kwargs)
        else:
            return typer.Option(**kwargs)

    def set_function_annotations_for_route(
            self,
            fun: RequestCaller,
            parameters: dict[str, FieldInfo],
            server_url: str | None = None,
            **extra_params: Any
    ) -> None:
        """
        Set Typer annotations for a function.

        This method sets Typer annotations for a given function based on provided parameters and server URL.

        :param fun: The function to set annotations for.
        :type fun: RequestCaller
        :param parameters: Dictionary containing parameter names and their field info.
        :type parameters: dict[str, FieldInfo]
        :param server_url: The server base URL (e.g., https://127.0.0.1:443).
        :type server_url: str, optional
        """
        annotations = {}
        defaults = {}
        for name, value in parameters.items():
            is_optional = name[0] == "-"
            if is_optional:
                name = name[1:]
            annotations[name] = Annotated[value.annotation, self.get_proxy_for_parameter(value, is_optional)]
            if value.default is not PydanticUndefined:
                defaults[name] = value.default

        annotations["server_url"] = Annotated[
            str, typer.Option(help="the server base url (e.g. https://127.0.0.1:443)",
                              parser=parse_url)]
        if server_url is not None:
            defaults["server_url"] = server_url
        for extra_param in extra_params:
            if extra_param in annotations:
                defaults[extra_param] = extra_params[extra_param]
        fun.__signature__ = get_inspect_signature(fun, annotations, defaults)
        fun.__annotations__ = annotations
        fun.__kwdefaults__ = defaults
