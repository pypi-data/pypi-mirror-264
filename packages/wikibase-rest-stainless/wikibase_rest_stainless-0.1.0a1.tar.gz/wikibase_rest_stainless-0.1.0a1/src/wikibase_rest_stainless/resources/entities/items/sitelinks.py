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
from ....types.entities.items import (
    SitelinkUpdateResponse,
    SitelinkRetrieveResponse,
    SitelinkUpdateSiteIDResponse,
    SitelinkRetrieveSiteIDResponse,
    sitelink_update_params,
    sitelink_delete_site_id_params,
    sitelink_update_site_id_params,
)

__all__ = ["Sitelinks", "AsyncSitelinks"]


class Sitelinks(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SitelinksWithRawResponse:
        return SitelinksWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SitelinksWithStreamingResponse:
        return SitelinksWithStreamingResponse(self)

    def retrieve(
        self,
        item_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SitelinkRetrieveResponse:
        """
        Retrieve an Item's sitelinks

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        return self._get(
            f"/entities/items/{item_id}/sitelinks",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SitelinkRetrieveResponse,
        )

    def update(
        self,
        item_id: str,
        *,
        patch: Iterable[sitelink_update_params.Patch],
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SitelinkUpdateResponse:
        """
        Change an Item's sitelinks

        Args:
          patch: A JSON Patch document as defined by RFC 6902

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        return self._patch(
            f"/entities/items/{item_id}/sitelinks",
            body=maybe_transform(
                {
                    "patch": patch,
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                sitelink_update_params.SitelinkUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SitelinkUpdateResponse,
        )

    def delete_site_id(
        self,
        site_id: str,
        *,
        item_id: str,
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
        Delete an Item's sitelink

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        if not site_id:
            raise ValueError(f"Expected a non-empty value for `site_id` but received {site_id!r}")
        return self._delete(
            f"/entities/items/{item_id}/sitelinks/{site_id}",
            body=maybe_transform(
                {
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                sitelink_delete_site_id_params.SitelinkDeleteSiteIDParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )

    def retrieve_site_id(
        self,
        site_id: str,
        *,
        item_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SitelinkRetrieveSiteIDResponse:
        """
        Retrieve an Item's sitelink

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        if not site_id:
            raise ValueError(f"Expected a non-empty value for `site_id` but received {site_id!r}")
        return self._get(
            f"/entities/items/{item_id}/sitelinks/{site_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SitelinkRetrieveSiteIDResponse,
        )

    def update_site_id(
        self,
        site_id: str,
        *,
        item_id: str,
        sitelink: sitelink_update_site_id_params.Sitelink,
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SitelinkUpdateSiteIDResponse:
        """
        Add / Replace an item's sitelink

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        if not site_id:
            raise ValueError(f"Expected a non-empty value for `site_id` but received {site_id!r}")
        return self._put(
            f"/entities/items/{item_id}/sitelinks/{site_id}",
            body=maybe_transform(
                {
                    "sitelink": sitelink,
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                sitelink_update_site_id_params.SitelinkUpdateSiteIDParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SitelinkUpdateSiteIDResponse,
        )


class AsyncSitelinks(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSitelinksWithRawResponse:
        return AsyncSitelinksWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSitelinksWithStreamingResponse:
        return AsyncSitelinksWithStreamingResponse(self)

    async def retrieve(
        self,
        item_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SitelinkRetrieveResponse:
        """
        Retrieve an Item's sitelinks

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        return await self._get(
            f"/entities/items/{item_id}/sitelinks",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SitelinkRetrieveResponse,
        )

    async def update(
        self,
        item_id: str,
        *,
        patch: Iterable[sitelink_update_params.Patch],
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SitelinkUpdateResponse:
        """
        Change an Item's sitelinks

        Args:
          patch: A JSON Patch document as defined by RFC 6902

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        return await self._patch(
            f"/entities/items/{item_id}/sitelinks",
            body=await async_maybe_transform(
                {
                    "patch": patch,
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                sitelink_update_params.SitelinkUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SitelinkUpdateResponse,
        )

    async def delete_site_id(
        self,
        site_id: str,
        *,
        item_id: str,
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
        Delete an Item's sitelink

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        if not site_id:
            raise ValueError(f"Expected a non-empty value for `site_id` but received {site_id!r}")
        return await self._delete(
            f"/entities/items/{item_id}/sitelinks/{site_id}",
            body=await async_maybe_transform(
                {
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                sitelink_delete_site_id_params.SitelinkDeleteSiteIDParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )

    async def retrieve_site_id(
        self,
        site_id: str,
        *,
        item_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SitelinkRetrieveSiteIDResponse:
        """
        Retrieve an Item's sitelink

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        if not site_id:
            raise ValueError(f"Expected a non-empty value for `site_id` but received {site_id!r}")
        return await self._get(
            f"/entities/items/{item_id}/sitelinks/{site_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SitelinkRetrieveSiteIDResponse,
        )

    async def update_site_id(
        self,
        site_id: str,
        *,
        item_id: str,
        sitelink: sitelink_update_site_id_params.Sitelink,
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SitelinkUpdateSiteIDResponse:
        """
        Add / Replace an item's sitelink

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        if not site_id:
            raise ValueError(f"Expected a non-empty value for `site_id` but received {site_id!r}")
        return await self._put(
            f"/entities/items/{item_id}/sitelinks/{site_id}",
            body=await async_maybe_transform(
                {
                    "sitelink": sitelink,
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                sitelink_update_site_id_params.SitelinkUpdateSiteIDParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SitelinkUpdateSiteIDResponse,
        )


class SitelinksWithRawResponse:
    def __init__(self, sitelinks: Sitelinks) -> None:
        self._sitelinks = sitelinks

        self.retrieve = to_raw_response_wrapper(
            sitelinks.retrieve,
        )
        self.update = to_raw_response_wrapper(
            sitelinks.update,
        )
        self.delete_site_id = to_raw_response_wrapper(
            sitelinks.delete_site_id,
        )
        self.retrieve_site_id = to_raw_response_wrapper(
            sitelinks.retrieve_site_id,
        )
        self.update_site_id = to_raw_response_wrapper(
            sitelinks.update_site_id,
        )


class AsyncSitelinksWithRawResponse:
    def __init__(self, sitelinks: AsyncSitelinks) -> None:
        self._sitelinks = sitelinks

        self.retrieve = async_to_raw_response_wrapper(
            sitelinks.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            sitelinks.update,
        )
        self.delete_site_id = async_to_raw_response_wrapper(
            sitelinks.delete_site_id,
        )
        self.retrieve_site_id = async_to_raw_response_wrapper(
            sitelinks.retrieve_site_id,
        )
        self.update_site_id = async_to_raw_response_wrapper(
            sitelinks.update_site_id,
        )


class SitelinksWithStreamingResponse:
    def __init__(self, sitelinks: Sitelinks) -> None:
        self._sitelinks = sitelinks

        self.retrieve = to_streamed_response_wrapper(
            sitelinks.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            sitelinks.update,
        )
        self.delete_site_id = to_streamed_response_wrapper(
            sitelinks.delete_site_id,
        )
        self.retrieve_site_id = to_streamed_response_wrapper(
            sitelinks.retrieve_site_id,
        )
        self.update_site_id = to_streamed_response_wrapper(
            sitelinks.update_site_id,
        )


class AsyncSitelinksWithStreamingResponse:
    def __init__(self, sitelinks: AsyncSitelinks) -> None:
        self._sitelinks = sitelinks

        self.retrieve = async_to_streamed_response_wrapper(
            sitelinks.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            sitelinks.update,
        )
        self.delete_site_id = async_to_streamed_response_wrapper(
            sitelinks.delete_site_id,
        )
        self.retrieve_site_id = async_to_streamed_response_wrapper(
            sitelinks.retrieve_site_id,
        )
        self.update_site_id = async_to_streamed_response_wrapper(
            sitelinks.update_site_id,
        )
