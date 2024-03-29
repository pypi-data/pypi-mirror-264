# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, TypedDict

__all__ = ["StatementCreateParams", "Statement"]


class StatementCreateParams(TypedDict, total=False):
    statement: Required[Statement]

    bot: bool

    comment: str

    tags: List[str]


class Statement(TypedDict, total=False):
    property: Required[object]

    value: Required[object]

    qualifiers: object

    rank: Literal["deprecated", "normal", "preferred"]
    """The rank of the Statement"""

    references: object
