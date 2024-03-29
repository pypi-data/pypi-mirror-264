# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import (
    make_request_options,
)
from ....types.entities.properties import (
    AliasListResponse,
    AliasCreateResponse,
    AliasUpdateResponse,
    AliasRetrieveResponse,
    alias_create_params,
    alias_update_params,
)

__all__ = ["Aliases", "AsyncAliases"]


class Aliases(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AliasesWithRawResponse:
        return AliasesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AliasesWithStreamingResponse:
        return AliasesWithStreamingResponse(self)

    def create(
        self,
        language_code: str,
        *,
        property_id: str,
        aliases: Iterable[object],
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AliasCreateResponse:
        """
        Create / Add a Property's aliases in a specific language

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not property_id:
            raise ValueError(f"Expected a non-empty value for `property_id` but received {property_id!r}")
        if not language_code:
            raise ValueError(f"Expected a non-empty value for `language_code` but received {language_code!r}")
        return self._post(
            f"/entities/properties/{property_id}/aliases/{language_code}",
            body=maybe_transform(
                {
                    "aliases": aliases,
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                alias_create_params.AliasCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AliasCreateResponse,
        )

    def retrieve(
        self,
        language_code: str,
        *,
        property_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AliasRetrieveResponse:
        """
        Retrieve a Property's aliases in a specific language

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not property_id:
            raise ValueError(f"Expected a non-empty value for `property_id` but received {property_id!r}")
        if not language_code:
            raise ValueError(f"Expected a non-empty value for `language_code` but received {language_code!r}")
        return self._get(
            f"/entities/properties/{property_id}/aliases/{language_code}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AliasRetrieveResponse,
        )

    def update(
        self,
        property_id: str,
        *,
        patch: Iterable[alias_update_params.Patch],
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AliasUpdateResponse:
        """
        Change a Property's aliases

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
            f"/entities/properties/{property_id}/aliases",
            body=maybe_transform(
                {
                    "patch": patch,
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                alias_update_params.AliasUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AliasUpdateResponse,
        )

    def list(
        self,
        property_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AliasListResponse:
        """
        Retrieve a Property's aliases

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not property_id:
            raise ValueError(f"Expected a non-empty value for `property_id` but received {property_id!r}")
        return self._get(
            f"/entities/properties/{property_id}/aliases",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AliasListResponse,
        )


class AsyncAliases(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAliasesWithRawResponse:
        return AsyncAliasesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAliasesWithStreamingResponse:
        return AsyncAliasesWithStreamingResponse(self)

    async def create(
        self,
        language_code: str,
        *,
        property_id: str,
        aliases: Iterable[object],
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AliasCreateResponse:
        """
        Create / Add a Property's aliases in a specific language

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not property_id:
            raise ValueError(f"Expected a non-empty value for `property_id` but received {property_id!r}")
        if not language_code:
            raise ValueError(f"Expected a non-empty value for `language_code` but received {language_code!r}")
        return await self._post(
            f"/entities/properties/{property_id}/aliases/{language_code}",
            body=await async_maybe_transform(
                {
                    "aliases": aliases,
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                alias_create_params.AliasCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AliasCreateResponse,
        )

    async def retrieve(
        self,
        language_code: str,
        *,
        property_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AliasRetrieveResponse:
        """
        Retrieve a Property's aliases in a specific language

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not property_id:
            raise ValueError(f"Expected a non-empty value for `property_id` but received {property_id!r}")
        if not language_code:
            raise ValueError(f"Expected a non-empty value for `language_code` but received {language_code!r}")
        return await self._get(
            f"/entities/properties/{property_id}/aliases/{language_code}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AliasRetrieveResponse,
        )

    async def update(
        self,
        property_id: str,
        *,
        patch: Iterable[alias_update_params.Patch],
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AliasUpdateResponse:
        """
        Change a Property's aliases

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
            f"/entities/properties/{property_id}/aliases",
            body=await async_maybe_transform(
                {
                    "patch": patch,
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                alias_update_params.AliasUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AliasUpdateResponse,
        )

    async def list(
        self,
        property_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AliasListResponse:
        """
        Retrieve a Property's aliases

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not property_id:
            raise ValueError(f"Expected a non-empty value for `property_id` but received {property_id!r}")
        return await self._get(
            f"/entities/properties/{property_id}/aliases",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AliasListResponse,
        )


class AliasesWithRawResponse:
    def __init__(self, aliases: Aliases) -> None:
        self._aliases = aliases

        self.create = to_raw_response_wrapper(
            aliases.create,
        )
        self.retrieve = to_raw_response_wrapper(
            aliases.retrieve,
        )
        self.update = to_raw_response_wrapper(
            aliases.update,
        )
        self.list = to_raw_response_wrapper(
            aliases.list,
        )


class AsyncAliasesWithRawResponse:
    def __init__(self, aliases: AsyncAliases) -> None:
        self._aliases = aliases

        self.create = async_to_raw_response_wrapper(
            aliases.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            aliases.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            aliases.update,
        )
        self.list = async_to_raw_response_wrapper(
            aliases.list,
        )


class AliasesWithStreamingResponse:
    def __init__(self, aliases: Aliases) -> None:
        self._aliases = aliases

        self.create = to_streamed_response_wrapper(
            aliases.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            aliases.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            aliases.update,
        )
        self.list = to_streamed_response_wrapper(
            aliases.list,
        )


class AsyncAliasesWithStreamingResponse:
    def __init__(self, aliases: AsyncAliases) -> None:
        self._aliases = aliases

        self.create = async_to_streamed_response_wrapper(
            aliases.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            aliases.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            aliases.update,
        )
        self.list = async_to_streamed_response_wrapper(
            aliases.list,
        )
