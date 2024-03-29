# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = [
    "ItemCreateParams",
    "Item",
    "ItemSitelinks",
    "ItemStatement",
    "ItemStatementProperty",
    "ItemStatementQualifier",
    "ItemStatementQualifierProperty",
    "ItemStatementQualifierValue",
    "ItemStatementReference",
    "ItemStatementReferencePart",
    "ItemStatementReferencePartProperty",
    "ItemStatementReferencePartValue",
    "ItemStatementValue",
]


class ItemCreateParams(TypedDict, total=False):
    item: Required[Item]

    bot: bool

    comment: str

    tags: List[str]


class ItemSitelinks(TypedDict, total=False):
    badges: List[str]

    title: str

    url: str


class ItemStatementProperty(TypedDict, total=False):
    id: str
    """The ID of the Property"""


class ItemStatementQualifierProperty(TypedDict, total=False):
    id: str
    """The ID of the Property"""


class ItemStatementQualifierValue(TypedDict, total=False):
    content: object
    """The value, if type == "value", otherwise omitted"""

    type: Literal["value", "somevalue", "novalue"]
    """The value type"""


class ItemStatementQualifier(TypedDict, total=False):
    property: ItemStatementQualifierProperty

    value: ItemStatementQualifierValue


class ItemStatementReferencePartProperty(TypedDict, total=False):
    id: str
    """The ID of the Property"""


class ItemStatementReferencePartValue(TypedDict, total=False):
    content: object
    """The value, if type == "value", otherwise omitted"""

    type: Literal["value", "somevalue", "novalue"]
    """The value type"""


class ItemStatementReferencePart(TypedDict, total=False):
    property: ItemStatementReferencePartProperty

    value: ItemStatementReferencePartValue


class ItemStatementReference(TypedDict, total=False):
    parts: Iterable[ItemStatementReferencePart]


class ItemStatementValue(TypedDict, total=False):
    content: object
    """The value, if type == "value", otherwise omitted"""

    type: Literal["value", "somevalue", "novalue"]
    """The value type"""


class ItemStatement(TypedDict, total=False):
    property: ItemStatementProperty

    qualifiers: Iterable[ItemStatementQualifier]

    rank: Literal["deprecated", "normal", "preferred"]
    """The rank of the Statement"""

    references: Iterable[ItemStatementReference]

    value: ItemStatementValue


class Item(TypedDict, total=False):
    aliases: Dict[str, List[str]]

    descriptions: Dict[str, str]

    labels: Dict[str, str]

    sitelinks: Dict[str, ItemSitelinks]

    statements: Dict[str, Iterable[ItemStatement]]
