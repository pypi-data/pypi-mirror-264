# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal

import httpx

from .labels import (
    Labels,
    AsyncLabels,
    LabelsWithRawResponse,
    AsyncLabelsWithRawResponse,
    LabelsWithStreamingResponse,
    AsyncLabelsWithStreamingResponse,
)
from .aliases import (
    Aliases,
    AsyncAliases,
    AliasesWithRawResponse,
    AsyncAliasesWithRawResponse,
    AliasesWithStreamingResponse,
    AsyncAliasesWithStreamingResponse,
)
from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ...._compat import cached_property
from .statements import (
    Statements,
    AsyncStatements,
    StatementsWithRawResponse,
    AsyncStatementsWithRawResponse,
    StatementsWithStreamingResponse,
    AsyncStatementsWithStreamingResponse,
)
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .descriptions import (
    Descriptions,
    AsyncDescriptions,
    DescriptionsWithRawResponse,
    AsyncDescriptionsWithRawResponse,
    DescriptionsWithStreamingResponse,
    AsyncDescriptionsWithStreamingResponse,
)
from ...._base_client import (
    make_request_options,
)
from ....types.entities import (
    PropertyUpdateResponse,
    PropertyRetrieveResponse,
    property_update_params,
    property_retrieve_params,
)

__all__ = ["Properties", "AsyncProperties"]


class Properties(SyncAPIResource):
    @cached_property
    def descriptions(self) -> Descriptions:
        return Descriptions(self._client)

    @cached_property
    def labels(self) -> Labels:
        return Labels(self._client)

    @cached_property
    def aliases(self) -> Aliases:
        return Aliases(self._client)

    @cached_property
    def statements(self) -> Statements:
        return Statements(self._client)

    @cached_property
    def with_raw_response(self) -> PropertiesWithRawResponse:
        return PropertiesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PropertiesWithStreamingResponse:
        return PropertiesWithStreamingResponse(self)

    def retrieve(
        self,
        property_id: str,
        *,
        _fields: List[Literal["type", "data-type", "labels", "descriptions", "aliases", "statements"]]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PropertyRetrieveResponse:
        """
        Retrieve a single Wikibase Property by ID

        Args:
          _fields: Comma-separated list of fields to include in each response object.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not property_id:
            raise ValueError(f"Expected a non-empty value for `property_id` but received {property_id!r}")
        return self._get(
            f"/entities/properties/{property_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"_fields": _fields}, property_retrieve_params.PropertyRetrieveParams),
            ),
            cast_to=PropertyRetrieveResponse,
        )

    def update(
        self,
        property_id: str,
        *,
        patch: Iterable[property_update_params.Patch],
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PropertyUpdateResponse:
        """
        This endpoint is currently in development and is not recommended for production
        use

        Args:
          patch: A JSON Patch document as defined by RFC 6902

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not property_id:
            raise ValueError(f"Expected a non-empty value for `property_id` but received {property_id!r}")
        return self._patch(
            f"/entities/properties/{property_id}",
            body=maybe_transform(
                {
                    "patch": patch,
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                property_update_params.PropertyUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PropertyUpdateResponse,
        )


class AsyncProperties(AsyncAPIResource):
    @cached_property
    def descriptions(self) -> AsyncDescriptions:
        return AsyncDescriptions(self._client)

    @cached_property
    def labels(self) -> AsyncLabels:
        return AsyncLabels(self._client)

    @cached_property
    def aliases(self) -> AsyncAliases:
        return AsyncAliases(self._client)

    @cached_property
    def statements(self) -> AsyncStatements:
        return AsyncStatements(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncPropertiesWithRawResponse:
        return AsyncPropertiesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPropertiesWithStreamingResponse:
        return AsyncPropertiesWithStreamingResponse(self)

    async def retrieve(
        self,
        property_id: str,
        *,
        _fields: List[Literal["type", "data-type", "labels", "descriptions", "aliases", "statements"]]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PropertyRetrieveResponse:
        """
        Retrieve a single Wikibase Property by ID

        Args:
          _fields: Comma-separated list of fields to include in each response object.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not property_id:
            raise ValueError(f"Expected a non-empty value for `property_id` but received {property_id!r}")
        return await self._get(
            f"/entities/properties/{property_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"_fields": _fields}, property_retrieve_params.PropertyRetrieveParams
                ),
            ),
            cast_to=PropertyRetrieveResponse,
        )

    async def update(
        self,
        property_id: str,
        *,
        patch: Iterable[property_update_params.Patch],
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PropertyUpdateResponse:
        """
        This endpoint is currently in development and is not recommended for production
        use

        Args:
          patch: A JSON Patch document as defined by RFC 6902

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not property_id:
            raise ValueError(f"Expected a non-empty value for `property_id` but received {property_id!r}")
        return await self._patch(
            f"/entities/properties/{property_id}",
            body=await async_maybe_transform(
                {
                    "patch": patch,
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                property_update_params.PropertyUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PropertyUpdateResponse,
        )


class PropertiesWithRawResponse:
    def __init__(self, properties: Properties) -> None:
        self._properties = properties

        self.retrieve = to_raw_response_wrapper(
            properties.retrieve,
        )
        self.update = to_raw_response_wrapper(
            properties.update,
        )

    @cached_property
    def descriptions(self) -> DescriptionsWithRawResponse:
        return DescriptionsWithRawResponse(self._properties.descriptions)

    @cached_property
    def labels(self) -> LabelsWithRawResponse:
        return LabelsWithRawResponse(self._properties.labels)

    @cached_property
    def aliases(self) -> AliasesWithRawResponse:
        return AliasesWithRawResponse(self._properties.aliases)

    @cached_property
    def statements(self) -> StatementsWithRawResponse:
        return StatementsWithRawResponse(self._properties.statements)


class AsyncPropertiesWithRawResponse:
    def __init__(self, properties: AsyncProperties) -> None:
        self._properties = properties

        self.retrieve = async_to_raw_response_wrapper(
            properties.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            properties.update,
        )

    @cached_property
    def descriptions(self) -> AsyncDescriptionsWithRawResponse:
        return AsyncDescriptionsWithRawResponse(self._properties.descriptions)

    @cached_property
    def labels(self) -> AsyncLabelsWithRawResponse:
        return AsyncLabelsWithRawResponse(self._properties.labels)

    @cached_property
    def aliases(self) -> AsyncAliasesWithRawResponse:
        return AsyncAliasesWithRawResponse(self._properties.aliases)

    @cached_property
    def statements(self) -> AsyncStatementsWithRawResponse:
        return AsyncStatementsWithRawResponse(self._properties.statements)


class PropertiesWithStreamingResponse:
    def __init__(self, properties: Properties) -> None:
        self._properties = properties

        self.retrieve = to_streamed_response_wrapper(
            properties.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            properties.update,
        )

    @cached_property
    def descriptions(self) -> DescriptionsWithStreamingResponse:
        return DescriptionsWithStreamingResponse(self._properties.descriptions)

    @cached_property
    def labels(self) -> LabelsWithStreamingResponse:
        return LabelsWithStreamingResponse(self._properties.labels)

    @cached_property
    def aliases(self) -> AliasesWithStreamingResponse:
        return AliasesWithStreamingResponse(self._properties.aliases)

    @cached_property
    def statements(self) -> StatementsWithStreamingResponse:
        return StatementsWithStreamingResponse(self._properties.statements)


class AsyncPropertiesWithStreamingResponse:
    def __init__(self, properties: AsyncProperties) -> None:
        self._properties = properties

        self.retrieve = async_to_streamed_response_wrapper(
            properties.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            properties.update,
        )

    @cached_property
    def descriptions(self) -> AsyncDescriptionsWithStreamingResponse:
        return AsyncDescriptionsWithStreamingResponse(self._properties.descriptions)

    @cached_property
    def labels(self) -> AsyncLabelsWithStreamingResponse:
        return AsyncLabelsWithStreamingResponse(self._properties.labels)

    @cached_property
    def aliases(self) -> AsyncAliasesWithStreamingResponse:
        return AsyncAliasesWithStreamingResponse(self._properties.aliases)

    @cached_property
    def statements(self) -> AsyncStatementsWithStreamingResponse:
        return AsyncStatementsWithStreamingResponse(self._properties.statements)
