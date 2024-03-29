# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Dict, Union, Mapping, cast
from typing_extensions import Self, Literal, override

import httpx

from . import resources, _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import (
    is_given,
    get_async_library,
)
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError, WikibaseRestStainlessError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = [
    "ENVIRONMENTS",
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "resources",
    "WikibaseRestStainless",
    "AsyncWikibaseRestStainless",
    "Client",
    "AsyncClient",
]

ENVIRONMENTS: Dict[str, str] = {
    "test": "https://test.wikidata.org/w/rest.php/wikibase/v0",
    "production": "https://wikidata.org/w/rest.php/wikibase/v0",
}


class WikibaseRestStainless(SyncAPIClient):
    openapi: resources.Openapi
    property_data_types: resources.PropertyDataTypes
    entities: resources.Entities
    statements: resources.Statements
    with_raw_response: WikibaseRestStainlessWithRawResponse
    with_streaming_response: WikibaseRestStainlessWithStreamedResponse

    # client options
    access_token: str

    _environment: Literal["test", "production"] | NotGiven

    def __init__(
        self,
        *,
        access_token: str | None = None,
        environment: Literal["test", "production"] | NotGiven = NOT_GIVEN,
        base_url: str | httpx.URL | None | NotGiven = NOT_GIVEN,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client. See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous wikibase-rest-stainless client instance.

        This automatically infers the `access_token` argument from the `WIKIBASE_BEARER_TOKEN` environment variable if it is not provided.
        """
        if access_token is None:
            access_token = os.environ.get("WIKIBASE_BEARER_TOKEN")
        if access_token is None:
            raise WikibaseRestStainlessError(
                "The access_token client option must be set either by passing access_token to the client or by setting the WIKIBASE_BEARER_TOKEN environment variable"
            )
        self.access_token = access_token

        self._environment = environment

        base_url_env = os.environ.get("WIKIBASE_REST_STAINLESS_BASE_URL")
        if is_given(base_url) and base_url is not None:
            # cast required because mypy doesn't understand the type narrowing
            base_url = cast("str | httpx.URL", base_url)  # pyright: ignore[reportUnnecessaryCast]
        elif is_given(environment):
            if base_url_env and base_url is not None:
                raise ValueError(
                    "Ambiguous URL; The `WIKIBASE_REST_STAINLESS_BASE_URL` env var and the `environment` argument are given. If you want to use the environment, you must pass base_url=None",
                )

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc
        elif base_url_env is not None:
            base_url = base_url_env
        else:
            self._environment = environment = "test"

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.openapi = resources.Openapi(self)
        self.property_data_types = resources.PropertyDataTypes(self)
        self.entities = resources.Entities(self)
        self.statements = resources.Statements(self)
        self.with_raw_response = WikibaseRestStainlessWithRawResponse(self)
        self.with_streaming_response = WikibaseRestStainlessWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        access_token = self.access_token
        return {"Authorization": f"Bearer {access_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        access_token: str | None = None,
        environment: Literal["test", "production"] | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            access_token=access_token or self.access_token,
            base_url=base_url or self.base_url,
            environment=environment or self._environment,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncWikibaseRestStainless(AsyncAPIClient):
    openapi: resources.AsyncOpenapi
    property_data_types: resources.AsyncPropertyDataTypes
    entities: resources.AsyncEntities
    statements: resources.AsyncStatements
    with_raw_response: AsyncWikibaseRestStainlessWithRawResponse
    with_streaming_response: AsyncWikibaseRestStainlessWithStreamedResponse

    # client options
    access_token: str

    _environment: Literal["test", "production"] | NotGiven

    def __init__(
        self,
        *,
        access_token: str | None = None,
        environment: Literal["test", "production"] | NotGiven = NOT_GIVEN,
        base_url: str | httpx.URL | None | NotGiven = NOT_GIVEN,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client. See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async wikibase-rest-stainless client instance.

        This automatically infers the `access_token` argument from the `WIKIBASE_BEARER_TOKEN` environment variable if it is not provided.
        """
        if access_token is None:
            access_token = os.environ.get("WIKIBASE_BEARER_TOKEN")
        if access_token is None:
            raise WikibaseRestStainlessError(
                "The access_token client option must be set either by passing access_token to the client or by setting the WIKIBASE_BEARER_TOKEN environment variable"
            )
        self.access_token = access_token

        self._environment = environment

        base_url_env = os.environ.get("WIKIBASE_REST_STAINLESS_BASE_URL")
        if is_given(base_url) and base_url is not None:
            # cast required because mypy doesn't understand the type narrowing
            base_url = cast("str | httpx.URL", base_url)  # pyright: ignore[reportUnnecessaryCast]
        elif is_given(environment):
            if base_url_env and base_url is not None:
                raise ValueError(
                    "Ambiguous URL; The `WIKIBASE_REST_STAINLESS_BASE_URL` env var and the `environment` argument are given. If you want to use the environment, you must pass base_url=None",
                )

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc
        elif base_url_env is not None:
            base_url = base_url_env
        else:
            self._environment = environment = "test"

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.openapi = resources.AsyncOpenapi(self)
        self.property_data_types = resources.AsyncPropertyDataTypes(self)
        self.entities = resources.AsyncEntities(self)
        self.statements = resources.AsyncStatements(self)
        self.with_raw_response = AsyncWikibaseRestStainlessWithRawResponse(self)
        self.with_streaming_response = AsyncWikibaseRestStainlessWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        access_token = self.access_token
        return {"Authorization": f"Bearer {access_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        access_token: str | None = None,
        environment: Literal["test", "production"] | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            access_token=access_token or self.access_token,
            base_url=base_url or self.base_url,
            environment=environment or self._environment,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class WikibaseRestStainlessWithRawResponse:
    def __init__(self, client: WikibaseRestStainless) -> None:
        self.openapi = resources.OpenapiWithRawResponse(client.openapi)
        self.property_data_types = resources.PropertyDataTypesWithRawResponse(client.property_data_types)
        self.entities = resources.EntitiesWithRawResponse(client.entities)
        self.statements = resources.StatementsWithRawResponse(client.statements)


class AsyncWikibaseRestStainlessWithRawResponse:
    def __init__(self, client: AsyncWikibaseRestStainless) -> None:
        self.openapi = resources.AsyncOpenapiWithRawResponse(client.openapi)
        self.property_data_types = resources.AsyncPropertyDataTypesWithRawResponse(client.property_data_types)
        self.entities = resources.AsyncEntitiesWithRawResponse(client.entities)
        self.statements = resources.AsyncStatementsWithRawResponse(client.statements)


class WikibaseRestStainlessWithStreamedResponse:
    def __init__(self, client: WikibaseRestStainless) -> None:
        self.openapi = resources.OpenapiWithStreamingResponse(client.openapi)
        self.property_data_types = resources.PropertyDataTypesWithStreamingResponse(client.property_data_types)
        self.entities = resources.EntitiesWithStreamingResponse(client.entities)
        self.statements = resources.StatementsWithStreamingResponse(client.statements)


class AsyncWikibaseRestStainlessWithStreamedResponse:
    def __init__(self, client: AsyncWikibaseRestStainless) -> None:
        self.openapi = resources.AsyncOpenapiWithStreamingResponse(client.openapi)
        self.property_data_types = resources.AsyncPropertyDataTypesWithStreamingResponse(client.property_data_types)
        self.entities = resources.AsyncEntitiesWithStreamingResponse(client.entities)
        self.statements = resources.AsyncStatementsWithStreamingResponse(client.statements)


Client = WikibaseRestStainless

AsyncClient = AsyncWikibaseRestStainless
