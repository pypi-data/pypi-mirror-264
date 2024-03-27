import typing

from fastapi.routing import APIRoute
from httpx import Response
from pydantic import BaseModel

from fastapi2cli.web.authentication import AuthenticationManager
from fastapi2cli.web.parameters import get_body, get_formatted_url, get_query_parameters, get_header_parameters, \
    get_cookie_parameters


class RequestExecutor(typing.Protocol):
    """
    A protocol representing an HTTP request executor.

    This protocol defines the structure of an object that can execute HTTP requests.

    """
    def request(
            self,
            method: str,
            url: str,
            params: dict[str, typing.Any],
            headers: dict[str, typing.Any],
            cookies: dict[str, typing.Any],
            json: dict[str, typing.Any] | None
    ) -> Response:
        """
        Execute an HTTP request.

        :param method: The HTTP method to use for the request.
        :type method: str
        :param url: The URL to send the request to.
        :type url: str
        :param params: The query parameters for the request.
        :type params: dict[str, typing.Any]
        :param headers: The headers for the request.
        :type headers: dict[str, typing.Any]
        :param cookies: The cookies for the request.
        :type cookies: dict[str, typing.Any]
        :param json: The JSON payload for the request.
        :type json: dict[str, typing.Any] | None
        :return: The response to the request.
        :rtype: Response
        """


class ServerInteractor:
    """
    Interacts with the server by sending requests and handling responses.

    This class provides methods to interact with the server by sending requests and handling responses. It uses a
    request executor to send HTTP requests and an authentication manager to manage authentication.

    """
    def __init__(self, server_url: str,
                 request_executor: RequestExecutor,
                 authentication_manager: AuthenticationManager,
                 ):
        """
        Initialize the ServerInteractor.

        :param server_url: The base URL of the server.
        :type server_url: str
        :param request_executor: The request executor to use for sending requests.
        :type request_executor: RequestExecutor
        :param authentication_manager: The authentication manager to use for managing authentication.
        :type authentication_manager: AuthenticationManager
        """
        self.server_url = server_url
        self.request_executor = request_executor
        self.authentication_manager = authentication_manager

    def get_response(self, route: APIRoute, **http_parameters: typing.Any) -> Response:
        """
        Get the response from the server for a given route.

        This method constructs the URL, parameters, headers, and cookies for the request based on the route and
        provided HTTP parameters. It then sends the request using the request executor and returns the response.

        :param route: The route for which to get the response.
        :type route: APIRoute
        :param http_parameters: The HTTP parameters for the request.
        :type http_parameters: typing.Any
        :return: The response from the server.
        :rtype: Response
        """
        url = get_formatted_url(self.server_url, route, **http_parameters)
        method = list(route.methods)[0]
        body = get_body(route, **http_parameters)
        query_params = get_query_parameters(route, **http_parameters)
        headers = get_header_parameters(route, **http_parameters)
        cookies = get_cookie_parameters(route, **http_parameters)
        if self.authentication_manager.is_route_authenticated(route):
            self.authentication_manager.set_server_url(self.server_url)
            headers.update(self.authentication_manager.headers)
            query_params.update(self.authentication_manager.query_parameters)
            cookies.update(self.authentication_manager.cookies)
        return self.request_executor.request(
            method,
            url,
            params=query_params,
            headers=headers,
            cookies=cookies,
            json=body.model_dump(mode="json") if body is not None else None
        )

    def request[T](self, route: APIRoute, **http_parameters: typing.Any) -> T | list[T]:
        """
        Send a request to the server and handle the response.

        This method sends a request to the server for the given route with the provided HTTP parameters. It then
        handles the response based on the route's response model.

        :param route: The route for which to send the request.
        :type route: APIRoute
        :param http_parameters: The HTTP parameters for the request.
        :type http_parameters: typing.Any
        :return: The response from the server.
        :rtype: T | list[T]
        """
        response_model: type[T] | list[type[T]] | None = route.response_model
        response = self.get_response(route, **http_parameters)
        response.raise_for_status()
        if response_model is None:
            return response.json()
        elif typing.get_origin(response_model) is list and isinstance(
                (model := typing.get_args(response_model)[0]), type(BaseModel)):
            return [model.model_validate(data) for data in response.json()]
        elif isinstance(response_model, type(BaseModel)):
            return response_model.model_validate(response.json())
        else:
            raise ValueError(response_model)
