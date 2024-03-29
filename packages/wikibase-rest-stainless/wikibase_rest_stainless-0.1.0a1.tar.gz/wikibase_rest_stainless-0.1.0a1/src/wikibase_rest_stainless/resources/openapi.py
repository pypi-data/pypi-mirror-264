# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import (
    make_request_options,
)

__all__ = ["Openapi", "AsyncOpenapi"]


class Openapi(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> OpenapiWithRawResponse:
        return OpenapiWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OpenapiWithStreamingResponse:
        return OpenapiWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Retrieve the OpenAPI document"""
        return self._get(
            "/openapi.json",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncOpenapi(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncOpenapiWithRawResponse:
        return AsyncOpenapiWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOpenapiWithStreamingResponse:
        return AsyncOpenapiWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Retrieve the OpenAPI document"""
        return await self._get(
            "/openapi.json",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class OpenapiWithRawResponse:
    def __init__(self, openapi: Openapi) -> None:
        self._openapi = openapi

        self.retrieve = to_raw_response_wrapper(
            openapi.retrieve,
        )


class AsyncOpenapiWithRawResponse:
    def __init__(self, openapi: AsyncOpenapi) -> None:
        self._openapi = openapi

        self.retrieve = async_to_raw_response_wrapper(
            openapi.retrieve,
        )


class OpenapiWithStreamingResponse:
    def __init__(self, openapi: Openapi) -> None:
        self._openapi = openapi

        self.retrieve = to_streamed_response_wrapper(
            openapi.retrieve,
        )


class AsyncOpenapiWithStreamingResponse:
    def __init__(self, openapi: AsyncOpenapi) -> None:
        self._openapi = openapi

        self.retrieve = async_to_streamed_response_wrapper(
            openapi.retrieve,
        )
