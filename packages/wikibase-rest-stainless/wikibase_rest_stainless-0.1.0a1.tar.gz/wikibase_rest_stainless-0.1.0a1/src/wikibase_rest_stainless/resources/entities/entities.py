# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .items import (
    Items,
    AsyncItems,
    ItemsWithRawResponse,
    AsyncItemsWithRawResponse,
    ItemsWithStreamingResponse,
    AsyncItemsWithStreamingResponse,
)
from ..._compat import cached_property
from .properties import (
    Properties,
    AsyncProperties,
    PropertiesWithRawResponse,
    AsyncPropertiesWithRawResponse,
    PropertiesWithStreamingResponse,
    AsyncPropertiesWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from .items.items import Items, AsyncItems
from .properties.properties import Properties, AsyncProperties

__all__ = ["Entities", "AsyncEntities"]


class Entities(SyncAPIResource):
    @cached_property
    def items(self) -> Items:
        return Items(self._client)

    @cached_property
    def properties(self) -> Properties:
        return Properties(self._client)

    @cached_property
    def with_raw_response(self) -> EntitiesWithRawResponse:
        return EntitiesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EntitiesWithStreamingResponse:
        return EntitiesWithStreamingResponse(self)


class AsyncEntities(AsyncAPIResource):
    @cached_property
    def items(self) -> AsyncItems:
        return AsyncItems(self._client)

    @cached_property
    def properties(self) -> AsyncProperties:
        return AsyncProperties(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncEntitiesWithRawResponse:
        return AsyncEntitiesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEntitiesWithStreamingResponse:
        return AsyncEntitiesWithStreamingResponse(self)


class EntitiesWithRawResponse:
    def __init__(self, entities: Entities) -> None:
        self._entities = entities

    @cached_property
    def items(self) -> ItemsWithRawResponse:
        return ItemsWithRawResponse(self._entities.items)

    @cached_property
    def properties(self) -> PropertiesWithRawResponse:
        return PropertiesWithRawResponse(self._entities.properties)


class AsyncEntitiesWithRawResponse:
    def __init__(self, entities: AsyncEntities) -> None:
        self._entities = entities

    @cached_property
    def items(self) -> AsyncItemsWithRawResponse:
        return AsyncItemsWithRawResponse(self._entities.items)

    @cached_property
    def properties(self) -> AsyncPropertiesWithRawResponse:
        return AsyncPropertiesWithRawResponse(self._entities.properties)


class EntitiesWithStreamingResponse:
    def __init__(self, entities: Entities) -> None:
        self._entities = entities

    @cached_property
    def items(self) -> ItemsWithStreamingResponse:
        return ItemsWithStreamingResponse(self._entities.items)

    @cached_property
    def properties(self) -> PropertiesWithStreamingResponse:
        return PropertiesWithStreamingResponse(self._entities.properties)


class AsyncEntitiesWithStreamingResponse:
    def __init__(self, entities: AsyncEntities) -> None:
        self._entities = entities

    @cached_property
    def items(self) -> AsyncItemsWithStreamingResponse:
        return AsyncItemsWithStreamingResponse(self._entities.items)

    @cached_property
    def properties(self) -> AsyncPropertiesWithStreamingResponse:
        return AsyncPropertiesWithStreamingResponse(self._entities.properties)
