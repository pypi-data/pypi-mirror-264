# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import PropertyDataTypeListResponse
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

__all__ = ["PropertyDataTypes", "AsyncPropertyDataTypes"]


class PropertyDataTypes(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PropertyDataTypesWithRawResponse:
        return PropertyDataTypesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PropertyDataTypesWithStreamingResponse:
        return PropertyDataTypesWithStreamingResponse(self)

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PropertyDataTypeListResponse:
        """Retrieve the map of property data types to value types"""
        return self._get(
            "/property-data-types",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PropertyDataTypeListResponse,
        )


class AsyncPropertyDataTypes(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPropertyDataTypesWithRawResponse:
        return AsyncPropertyDataTypesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPropertyDataTypesWithStreamingResponse:
        return AsyncPropertyDataTypesWithStreamingResponse(self)

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PropertyDataTypeListResponse:
        """Retrieve the map of property data types to value types"""
        return await self._get(
            "/property-data-types",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PropertyDataTypeListResponse,
        )


class PropertyDataTypesWithRawResponse:
    def __init__(self, property_data_types: PropertyDataTypes) -> None:
        self._property_data_types = property_data_types

        self.list = to_raw_response_wrapper(
            property_data_types.list,
        )


class AsyncPropertyDataTypesWithRawResponse:
    def __init__(self, property_data_types: AsyncPropertyDataTypes) -> None:
        self._property_data_types = property_data_types

        self.list = async_to_raw_response_wrapper(
            property_data_types.list,
        )


class PropertyDataTypesWithStreamingResponse:
    def __init__(self, property_data_types: PropertyDataTypes) -> None:
        self._property_data_types = property_data_types

        self.list = to_streamed_response_wrapper(
            property_data_types.list,
        )


class AsyncPropertyDataTypesWithStreamingResponse:
    def __init__(self, property_data_types: AsyncPropertyDataTypes) -> None:
        self._property_data_types = property_data_types

        self.list = async_to_streamed_response_wrapper(
            property_data_types.list,
        )
