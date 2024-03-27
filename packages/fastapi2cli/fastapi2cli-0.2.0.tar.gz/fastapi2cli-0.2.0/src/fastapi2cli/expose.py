from functools import partial
from logging import getLogger
from typing import Any, Callable

import typer
from fastapi import FastAPI

from fastapi2cli.fastapi_converter import FastAPIConverter
from fastapi2cli.typer_command_generator import TyperCommandGenerator
from fastapi2cli.web.authentication import NoAuthResolver, AuthenticationManager, \
    AuthenticationResolverBase
from fastapi2cli.web.server_interactor import ServerInteractor, RequestExecutor

logger = getLogger(__name__)


def expose_app(
        app: FastAPI,
        authentication_resolver: AuthenticationResolverBase = None,
        authenticated_dependencies: list[Callable] = None,
        request_executor: RequestExecutor = None,
        additional_parsers: dict[type, Callable[[str], Any]] = None,
        server_url: str = None,
        **kwargs: Any
) -> typer.Typer:
    """
    Expose FastAPI application routes as a Typer CLI.

    This function creates a Typer CLI based on the routes defined in a FastAPI application.

    :param app: The FastAPI application to expose.
    :type app: FastAPI
    :param authentication_resolver: Authentication resolver for the application, defaults to None.
        which will raise exception if attempting to access an authenticated route
    :type authentication_resolver: AuthenticationResolverBase, optional
    :param authenticated_dependencies: List of authenticated dependencies, defaults to None.
        this allows the app to know what endpoint/route is considered as authenticated.
    :type authenticated_dependencies: list[Callable], optional
    :param request_executor: Request executor for making HTTP requests, defaults to None.
    :type request_executor: RequestExecutor, optional
    :param additional_parsers: Additional parsers for custom types, defaults to None.
        This is for types that Typer don't handle and are present in endpoints/routes you want to expose
    :type additional_parsers: dict[type, Callable[[str], Any]], optional
    :param server_url: The base URL of the server, defaults to None.
        (if set to none the cli server_url parameter will be mandatory)
    :type server_url: str, optional
    :param kwargs: extra arguments to provide to the generated commands as defaults
    :type kwargs: Any, optional
    :return: Typer CLI exposing the FastAPI application routes.
    :rtype: typer.Typer
    """
    if request_executor is None:
        import httpx
        request_executor = httpx
    if authentication_resolver is None:
        authentication_resolver = NoAuthResolver()
    if authenticated_dependencies is None:
        authenticated_dependencies = []
    if additional_parsers is None:
        additional_parsers = {}
    authentication_manager = AuthenticationManager(authenticated_dependencies, authentication_resolver)
    server_interactor_factory = partial(ServerInteractor,
                                        request_executor=request_executor,
                                        authentication_manager=authentication_manager)
    converter = FastAPIConverter(server_interactor_factory, TyperCommandGenerator(additional_parsers), server_url,
                                 **kwargs)
    return converter.expose_app_routes_in_typer_cli(app)
