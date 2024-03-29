# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["PropertyUpdateParams", "Patch"]


class PropertyUpdateParams(TypedDict, total=False):
    patch: Required[Iterable[Patch]]
    """A JSON Patch document as defined by RFC 6902"""

    bot: bool

    comment: str

    tags: List[str]


class Patch(TypedDict, total=False):
    op: Required[Literal["add", "copy", "move", "remove", "replace", "test"]]
    """The operation to perform"""

    path: Required[str]
    """A JSON Pointer for the property to manipulate"""

    value: object
    """The value to be used within the operation"""
