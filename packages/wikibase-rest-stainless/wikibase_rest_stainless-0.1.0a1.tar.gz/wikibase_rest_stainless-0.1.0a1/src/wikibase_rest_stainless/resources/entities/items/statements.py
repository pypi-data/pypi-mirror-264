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
    StatementListResponse,
    StatementCreateResponse,
    StatementUpdateResponse,
    StatementRetrieveResponse,
    statement_list_params,
    statement_create_params,
    statement_delete_params,
    statement_update_params,
)

__all__ = ["Statements", "AsyncStatements"]


class Statements(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> StatementsWithRawResponse:
        return StatementsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> StatementsWithStreamingResponse:
        return StatementsWithStreamingResponse(self)

    def create(
        self,
        item_id: str,
        *,
        statement: statement_create_params.Statement,
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StatementCreateResponse:
        """
        Add a new Statement to an Item

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        return self._post(
            f"/entities/items/{item_id}/statements",
            body=maybe_transform(
                {
                    "statement": statement,
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                statement_create_params.StatementCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StatementCreateResponse,
        )

    def retrieve(
        self,
        statement_id: str,
        *,
        item_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StatementRetrieveResponse:
        """
        This endpoint is also accessible through `/statements/{statement_id}`

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        if not statement_id:
            raise ValueError(f"Expected a non-empty value for `statement_id` but received {statement_id!r}")
        return self._get(
            f"/entities/items/{item_id}/statements/{statement_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StatementRetrieveResponse,
        )

    def update(
        self,
        statement_id: str,
        *,
        item_id: str,
        patch: Iterable[statement_update_params.Patch],
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StatementUpdateResponse:
        """
        This endpoint is also accessible through `/statements/{statement_id}`.

        Args:
          patch: A JSON Patch document as defined by RFC 6902

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        if not statement_id:
            raise ValueError(f"Expected a non-empty value for `statement_id` but received {statement_id!r}")
        return self._patch(
            f"/entities/items/{item_id}/statements/{statement_id}",
            body=maybe_transform(
                {
                    "patch": patch,
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                statement_update_params.StatementUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StatementUpdateResponse,
        )

    def list(
        self,
        item_id: str,
        *,
        property: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StatementListResponse:
        """
        Retrieve Statements from an Item

        Args:
          property: Single property ID to filter statements by.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        return self._get(
            f"/entities/items/{item_id}/statements",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"property": property}, statement_list_params.StatementListParams),
            ),
            cast_to=StatementListResponse,
        )

    def delete(
        self,
        statement_id: str,
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
        This endpoint is also accessible through `/statements/{statement_id}`

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        if not statement_id:
            raise ValueError(f"Expected a non-empty value for `statement_id` but received {statement_id!r}")
        return self._delete(
            f"/entities/items/{item_id}/statements/{statement_id}",
            body=maybe_transform(
                {
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                statement_delete_params.StatementDeleteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )


class AsyncStatements(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncStatementsWithRawResponse:
        return AsyncStatementsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncStatementsWithStreamingResponse:
        return AsyncStatementsWithStreamingResponse(self)

    async def create(
        self,
        item_id: str,
        *,
        statement: statement_create_params.Statement,
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StatementCreateResponse:
        """
        Add a new Statement to an Item

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        return await self._post(
            f"/entities/items/{item_id}/statements",
            body=await async_maybe_transform(
                {
                    "statement": statement,
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                statement_create_params.StatementCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StatementCreateResponse,
        )

    async def retrieve(
        self,
        statement_id: str,
        *,
        item_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StatementRetrieveResponse:
        """
        This endpoint is also accessible through `/statements/{statement_id}`

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        if not statement_id:
            raise ValueError(f"Expected a non-empty value for `statement_id` but received {statement_id!r}")
        return await self._get(
            f"/entities/items/{item_id}/statements/{statement_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StatementRetrieveResponse,
        )

    async def update(
        self,
        statement_id: str,
        *,
        item_id: str,
        patch: Iterable[statement_update_params.Patch],
        bot: bool | NotGiven = NOT_GIVEN,
        comment: str | NotGiven = NOT_GIVEN,
        tags: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StatementUpdateResponse:
        """
        This endpoint is also accessible through `/statements/{statement_id}`.

        Args:
          patch: A JSON Patch document as defined by RFC 6902

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        if not statement_id:
            raise ValueError(f"Expected a non-empty value for `statement_id` but received {statement_id!r}")
        return await self._patch(
            f"/entities/items/{item_id}/statements/{statement_id}",
            body=await async_maybe_transform(
                {
                    "patch": patch,
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                statement_update_params.StatementUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StatementUpdateResponse,
        )

    async def list(
        self,
        item_id: str,
        *,
        property: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StatementListResponse:
        """
        Retrieve Statements from an Item

        Args:
          property: Single property ID to filter statements by.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        return await self._get(
            f"/entities/items/{item_id}/statements",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"property": property}, statement_list_params.StatementListParams),
            ),
            cast_to=StatementListResponse,
        )

    async def delete(
        self,
        statement_id: str,
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
        This endpoint is also accessible through `/statements/{statement_id}`

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        if not statement_id:
            raise ValueError(f"Expected a non-empty value for `statement_id` but received {statement_id!r}")
        return await self._delete(
            f"/entities/items/{item_id}/statements/{statement_id}",
            body=await async_maybe_transform(
                {
                    "bot": bot,
                    "comment": comment,
                    "tags": tags,
                },
                statement_delete_params.StatementDeleteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )


class StatementsWithRawResponse:
    def __init__(self, statements: Statements) -> None:
        self._statements = statements

        self.create = to_raw_response_wrapper(
            statements.create,
        )
        self.retrieve = to_raw_response_wrapper(
            statements.retrieve,
        )
        self.update = to_raw_response_wrapper(
            statements.update,
        )
        self.list = to_raw_response_wrapper(
            statements.list,
        )
        self.delete = to_raw_response_wrapper(
            statements.delete,
        )


class AsyncStatementsWithRawResponse:
    def __init__(self, statements: AsyncStatements) -> None:
        self._statements = statements

        self.create = async_to_raw_response_wrapper(
            statements.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            statements.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            statements.update,
        )
        self.list = async_to_raw_response_wrapper(
            statements.list,
        )
        self.delete = async_to_raw_response_wrapper(
            statements.delete,
        )


class StatementsWithStreamingResponse:
    def __init__(self, statements: Statements) -> None:
        self._statements = statements

        self.create = to_streamed_response_wrapper(
            statements.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            statements.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            statements.update,
        )
        self.list = to_streamed_response_wrapper(
            statements.list,
        )
        self.delete = to_streamed_response_wrapper(
            statements.delete,
        )


class AsyncStatementsWithStreamingResponse:
    def __init__(self, statements: AsyncStatements) -> None:
        self._statements = statements

        self.create = async_to_streamed_response_wrapper(
            statements.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            statements.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            statements.update,
        )
        self.list = async_to_streamed_response_wrapper(
            statements.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            statements.delete,
        )
