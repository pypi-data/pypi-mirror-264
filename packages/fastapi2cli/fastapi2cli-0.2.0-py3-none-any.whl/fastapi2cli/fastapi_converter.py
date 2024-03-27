from logging import getLogger
from typing import Callable, Any

import typer
from fastapi import FastAPI
from fastapi.routing import APIRoute
from rich import print

from fastapi2cli.parameters.get_params_for import get_parameters_for_route
from fastapi2cli.parameters.simplifier import convert_parameters_to_typer_supported_format
from fastapi2cli.typer_command_generator import TyperCommandGenerator, RequestCaller
from fastapi2cli.web.server_interactor import ServerInteractor

logger = getLogger(__name__)


class FastAPIConverter:
    """
    Converts FastAPI routes to Typer commands.

    This class is responsible for converting FastAPI routes into Typer commands, enabling them to be used as command-line
    interfaces (CLIs). It generates Typer command functions for each route and registers them with a Typer application.

    :param server_interactor_factory: A factory function for creating server interactors.
    :type server_interactor_factory: Callable[[str], ServerInteractor]
    :param typer_command_generator: A TyperCommandGenerator instance for generating Typer commands.
    :type typer_command_generator: TyperCommandGenerator
    :param server_url: The base URL of the server, optional.
    :type server_url: str, optional
    """

    def __init__(self,
                 server_interactor_factory: Callable[[str], ServerInteractor],
                 typer_command_generator: TyperCommandGenerator,
                 server_url: str | None = None,
                 **kwargs: Any):
        self.server_interactor_factory = server_interactor_factory
        self.typer_command_generator = typer_command_generator
        self.server_url = server_url
        self.extra_params = kwargs

    def generate_function_for_route(
            self,
            route: APIRoute,
    ) -> RequestCaller:
        """
        Generate a function for handling a specific route.

        This method generates a function that corresponds to a specific route. The function is responsible for making
        requests to the server using the provided route.

        :param route: The FastAPI route.
        :type route: APIRoute
        :return: The function for handling the route.
        :rtype: RequestCaller
        """
        original_parameters = get_parameters_for_route(route)
        parameters = convert_parameters_to_typer_supported_format(original_parameters)

        def request(server_url: str, **kwargs: Any) -> route.response_model:
            """
            Send a request to the server for the specified route.

            This function sends a request to the server for the specified route with the provided keyword arguments.

            :param server_url: The base URL of the server.
            :type server_url: str
            :param kwargs: Keyword arguments representing parameters for the request.
            :type kwargs: Any
            :return: The response from the server.
            :rtype: route.response_model
            """
            server_interactor = self.server_interactor_factory(server_url)
            result = server_interactor.request(route, **kwargs)
            print(result)
            return result

        self.typer_command_generator.set_function_annotations_for_route(request, parameters, self.server_url, **self.extra_params)
        return request

    def expose_route_in_typer_cli(
            self,
            route: APIRoute, typer_app: typer.Typer,
    ):
        """
        Expose a route in a Typer CLI.

        This method exposes a specific route in a Typer CLI application. It generates a Typer command function for the
        route and registers it with the Typer application.

        :param route: The FastAPI route to expose.
        :type route: APIRoute
        :param typer_app: The Typer application.
        :type typer_app: typer.Typer
        """
        command_name = route.name.replace('_', '-')
        fun = self.generate_function_for_route(route)
        extra_args = {}

        if len(fun.__annotations__) > 1:  # server_url always specified
            extra_args["no_args_is_help"] = True
        if len(route.tags) == 1:
            extra_args["rich_help_panel"] = route.tags[0]
        typer_app.command(name=command_name, help=route.description, deprecated=route.deprecated, **extra_args)(fun)

    def expose_app_routes_in_typer_cli(
            self,
            app: FastAPI,

    ) -> typer.Typer:
        """
        Expose all routes in a FastAPI application as Typer commands.

        This method exposes all routes in a FastAPI application as Typer commands in a Typer CLI application.

        :param app: The FastAPI application.
        :type app: FastAPI
        :return: The Typer CLI application.
        :rtype: typer.Typer
        """
        typer_app = typer.Typer(no_args_is_help=True)
        for route in app.routes:
            if isinstance(route, APIRoute):
                try:
                    self.expose_route_in_typer_cli(route, typer_app)
                except Exception as exc:
                    logger.error("Cannot register route %s due to exception %s", route, repr(exc))
        return typer_app
