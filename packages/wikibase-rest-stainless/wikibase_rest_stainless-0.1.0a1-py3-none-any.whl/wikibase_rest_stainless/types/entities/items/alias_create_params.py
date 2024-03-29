# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Required, TypedDict

__all__ = ["AliasCreateParams"]


class AliasCreateParams(TypedDict, total=False):
    item_id: Required[str]

    aliases: Required[Iterable[object]]

    bot: bool

    comment: str

    tags: List[str]
