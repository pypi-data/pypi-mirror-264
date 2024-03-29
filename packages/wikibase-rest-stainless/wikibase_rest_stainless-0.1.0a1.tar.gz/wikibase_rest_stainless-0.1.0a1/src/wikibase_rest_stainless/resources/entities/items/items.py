# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
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
from .sitelinks import (
    Sitelinks,
    AsyncSitelinks,
    SitelinksWithRawResponse,
    AsyncSitelinksWithRawResponse,
    SitelinksWithStreamingResponse,
    AsyncSitelinksWithStreamingResponse,
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
from ....types.entities import ItemCreateResponse, ItemRetrieveResponse, item_create_params, item_retrieve_params

__all__ = ["Items", "AsyncItems"]


class Items(SyncAPIResource):
    @cached_property
    def sitelinks(self) -> Sitelinks:
        return Sitelinks(self._client)

    @cached_property
    def descriptions(self) -> Descriptions:
        return Descriptions(self._client)

    @cached_property
    def statements(self) -> Statements:
        return Statements(self._client)

    @cached_property
    def labels(self) -> Labels:
        return Labels(self._client)

    @cached_property
    def aliases(self) -> Aliases:
        return Aliases(self._client)

    @cached_property
    def with_raw_response(self) -> ItemsWithRawResponse:
        return ItemsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ItemsWithStreamingResponse:
        return ItemsWithStreamingResponse(self)

    def create(
        self,
        *,
        item: item_create_params.Item,
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ItemCreateResponse:
        """
        This endpoint is currently in development and is not recommended for production
        use

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/entities/items",
            body=maybe_transform(
                {
                    "item": item,
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                item_create_params.ItemCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ItemCreateResponse,
        )

    def retrieve(
        self,
        item_id: str,
        *,
        _fields: List[Literal["type", "labels", "descriptions", "aliases", "statements", "sitelinks"]]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ItemRetrieveResponse:
        """
        Retrieve a single Wikibase Item by ID

        Args:
          _fields: Comma-separated list of fields to include in each response object.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        return self._get(
            f"/entities/items/{item_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"_fields": _fields}, item_retrieve_params.ItemRetrieveParams),
            ),
            cast_to=ItemRetrieveResponse,
        )


class AsyncItems(AsyncAPIResource):
    @cached_property
    def sitelinks(self) -> AsyncSitelinks:
        return AsyncSitelinks(self._client)

    @cached_property
    def descriptions(self) -> AsyncDescriptions:
        return AsyncDescriptions(self._client)

    @cached_property
    def statements(self) -> AsyncStatements:
        return AsyncStatements(self._client)

    @cached_property
    def labels(self) -> AsyncLabels:
        return AsyncLabels(self._client)

    @cached_property
    def aliases(self) -> AsyncAliases:
        return AsyncAliases(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncItemsWithRawResponse:
        return AsyncItemsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncItemsWithStreamingResponse:
        return AsyncItemsWithStreamingResponse(self)

    async def create(
        self,
        *,
        item: item_create_params.Item,
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ItemCreateResponse:
        """
        This endpoint is currently in development and is not recommended for production
        use

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/entities/items",
            body=await async_maybe_transform(
                {
                    "item": item,
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                item_create_params.ItemCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ItemCreateResponse,
        )

    async def retrieve(
        self,
        item_id: str,
        *,
        _fields: List[Literal["type", "labels", "descriptions", "aliases", "statements", "sitelinks"]]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ItemRetrieveResponse:
        """
        Retrieve a single Wikibase Item by ID

        Args:
          _fields: Comma-separated list of fields to include in each response object.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        return await self._get(
            f"/entities/items/{item_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"_fields": _fields}, item_retrieve_params.ItemRetrieveParams),
            ),
            cast_to=ItemRetrieveResponse,
        )


class ItemsWithRawResponse:
    def __init__(self, items: Items) -> None:
        self._items = items

        self.create = to_raw_response_wrapper(
            items.create,
        )
        self.retrieve = to_raw_response_wrapper(
            items.retrieve,
        )

    @cached_property
    def sitelinks(self) -> SitelinksWithRawResponse:
        return SitelinksWithRawResponse(self._items.sitelinks)

    @cached_property
    def descriptions(self) -> DescriptionsWithRawResponse:
        return DescriptionsWithRawResponse(self._items.descriptions)

    @cached_property
    def statements(self) -> StatementsWithRawResponse:
        return StatementsWithRawResponse(self._items.statements)

    @cached_property
    def labels(self) -> LabelsWithRawResponse:
        return LabelsWithRawResponse(self._items.labels)

    @cached_property
    def aliases(self) -> AliasesWithRawResponse:
        return AliasesWithRawResponse(self._items.aliases)


class AsyncItemsWithRawResponse:
    def __init__(self, items: AsyncItems) -> None:
        self._items = items

        self.create = async_to_raw_response_wrapper(
            items.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            items.retrieve,
        )

    @cached_property
    def sitelinks(self) -> AsyncSitelinksWithRawResponse:
        return AsyncSitelinksWithRawResponse(self._items.sitelinks)

    @cached_property
    def descriptions(self) -> AsyncDescriptionsWithRawResponse:
        return AsyncDescriptionsWithRawResponse(self._items.descriptions)

    @cached_property
    def statements(self) -> AsyncStatementsWithRawResponse:
        return AsyncStatementsWithRawResponse(self._items.statements)

    @cached_property
    def labels(self) -> AsyncLabelsWithRawResponse:
        return AsyncLabelsWithRawResponse(self._items.labels)

    @cached_property
    def aliases(self) -> AsyncAliasesWithRawResponse:
        return AsyncAliasesWithRawResponse(self._items.aliases)


class ItemsWithStreamingResponse:
    def __init__(self, items: Items) -> None:
        self._items = items

        self.create = to_streamed_response_wrapper(
            items.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            items.retrieve,
        )

    @cached_property
    def sitelinks(self) -> SitelinksWithStreamingResponse:
        return SitelinksWithStreamingResponse(self._items.sitelinks)

    @cached_property
    def descriptions(self) -> DescriptionsWithStreamingResponse:
        return DescriptionsWithStreamingResponse(self._items.descriptions)

    @cached_property
    def statements(self) -> StatementsWithStreamingResponse:
        return StatementsWithStreamingResponse(self._items.statements)

    @cached_property
    def labels(self) -> LabelsWithStreamingResponse:
        return LabelsWithStreamingResponse(self._items.labels)

    @cached_property
    def aliases(self) -> AliasesWithStreamingResponse:
        return AliasesWithStreamingResponse(self._items.aliases)


class AsyncItemsWithStreamingResponse:
    def __init__(self, items: AsyncItems) -> None:
        self._items = items

        self.create = async_to_streamed_response_wrapper(
            items.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            items.retrieve,
        )

    @cached_property
    def sitelinks(self) -> AsyncSitelinksWithStreamingResponse:
        return AsyncSitelinksWithStreamingResponse(self._items.sitelinks)

    @cached_property
    def descriptions(self) -> AsyncDescriptionsWithStreamingResponse:
        return AsyncDescriptionsWithStreamingResponse(self._items.descriptions)

    @cached_property
    def statements(self) -> AsyncStatementsWithStreamingResponse:
        return AsyncStatementsWithStreamingResponse(self._items.statements)

    @cached_property
    def labels(self) -> AsyncLabelsWithStreamingResponse:
        return AsyncLabelsWithStreamingResponse(self._items.labels)

    @cached_property
    def aliases(self) -> AsyncAliasesWithStreamingResponse:
        return AsyncAliasesWithStreamingResponse(self._items.aliases)
