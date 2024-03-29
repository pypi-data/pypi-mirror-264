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
    DescriptionListResponse,
    DescriptionUpdateResponse,
    description_create_params,
    description_delete_params,
    description_update_params,
)

__all__ = ["Descriptions", "AsyncDescriptions"]


class Descriptions(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DescriptionsWithRawResponse:
        return DescriptionsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DescriptionsWithStreamingResponse:
        return DescriptionsWithStreamingResponse(self)

    def create(
        self,
        language_code: str,
        *,
        property_id: str,
        description: str,
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Add / Replace a Property's description in a specific language

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
        return self._put(
            f"/entities/properties/{property_id}/descriptions/{language_code}",
            body=maybe_transform(
                {
                    "description": description,
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                description_create_params.DescriptionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
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
    ) -> str:
        """
        Retrieve a Property's description in a specific language

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
            f"/entities/properties/{property_id}/descriptions/{language_code}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )

    def update(
        self,
        property_id: str,
        *,
        patch: Iterable[description_update_params.Patch],
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DescriptionUpdateResponse:
        """
        Change a Property's descriptions

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
            f"/entities/properties/{property_id}/descriptions",
            body=maybe_transform(
                {
                    "patch": patch,
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                description_update_params.DescriptionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DescriptionUpdateResponse,
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
    ) -> DescriptionListResponse:
        """
        Retrieve a Property's descriptions

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not property_id:
            raise ValueError(f"Expected a non-empty value for `property_id` but received {property_id!r}")
        return self._get(
            f"/entities/properties/{property_id}/descriptions",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DescriptionListResponse,
        )

    def delete(
        self,
        language_code: str,
        *,
        property_id: str,
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Delete a Property's description in a specific language

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
        return self._delete(
            f"/entities/properties/{property_id}/descriptions/{language_code}",
            body=maybe_transform(
                {
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                description_delete_params.DescriptionDeleteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )


class AsyncDescriptions(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDescriptionsWithRawResponse:
        return AsyncDescriptionsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDescriptionsWithStreamingResponse:
        return AsyncDescriptionsWithStreamingResponse(self)

    async def create(
        self,
        language_code: str,
        *,
        property_id: str,
        description: str,
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Add / Replace a Property's description in a specific language

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
        return await self._put(
            f"/entities/properties/{property_id}/descriptions/{language_code}",
            body=await async_maybe_transform(
                {
                    "description": description,
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                description_create_params.DescriptionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
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
    ) -> str:
        """
        Retrieve a Property's description in a specific language

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
            f"/entities/properties/{property_id}/descriptions/{language_code}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )

    async def update(
        self,
        property_id: str,
        *,
        patch: Iterable[description_update_params.Patch],
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DescriptionUpdateResponse:
        """
        Change a Property's descriptions

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
            f"/entities/properties/{property_id}/descriptions",
            body=await async_maybe_transform(
                {
                    "patch": patch,
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                description_update_params.DescriptionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DescriptionUpdateResponse,
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
    ) -> DescriptionListResponse:
        """
        Retrieve a Property's descriptions

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not property_id:
            raise ValueError(f"Expected a non-empty value for `property_id` but received {property_id!r}")
        return await self._get(
            f"/entities/properties/{property_id}/descriptions",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DescriptionListResponse,
        )

    async def delete(
        self,
        language_code: str,
        *,
        property_id: str,
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Delete a Property's description in a specific language

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
        return await self._delete(
            f"/entities/properties/{property_id}/descriptions/{language_code}",
            body=await async_maybe_transform(
                {
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                description_delete_params.DescriptionDeleteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )


class DescriptionsWithRawResponse:
    def __init__(self, descriptions: Descriptions) -> None:
        self._descriptions = descriptions

        self.create = to_raw_response_wrapper(
            descriptions.create,
        )
        self.retrieve = to_raw_response_wrapper(
            descriptions.retrieve,
        )
        self.update = to_raw_response_wrapper(
            descriptions.update,
        )
        self.list = to_raw_response_wrapper(
            descriptions.list,
        )
        self.delete = to_raw_response_wrapper(
            descriptions.delete,
        )


class AsyncDescriptionsWithRawResponse:
    def __init__(self, descriptions: AsyncDescriptions) -> None:
        self._descriptions = descriptions

        self.create = async_to_raw_response_wrapper(
            descriptions.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            descriptions.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            descriptions.update,
        )
        self.list = async_to_raw_response_wrapper(
            descriptions.list,
        )
        self.delete = async_to_raw_response_wrapper(
            descriptions.delete,
        )


class DescriptionsWithStreamingResponse:
    def __init__(self, descriptions: Descriptions) -> None:
        self._descriptions = descriptions

        self.create = to_streamed_response_wrapper(
            descriptions.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            descriptions.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            descriptions.update,
        )
        self.list = to_streamed_response_wrapper(
            descriptions.list,
        )
        self.delete = to_streamed_response_wrapper(
            descriptions.delete,
        )


class AsyncDescriptionsWithStreamingResponse:
    def __init__(self, descriptions: AsyncDescriptions) -> None:
        self._descriptions = descriptions

        self.create = async_to_streamed_response_wrapper(
            descriptions.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            descriptions.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            descriptions.update,
        )
        self.list = async_to_streamed_response_wrapper(
            descriptions.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            descriptions.delete,
        )
