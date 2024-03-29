# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

__all__ = ["StatementDeleteParams"]


class StatementDeleteParams(TypedDict, total=False):
    bot: bool

    comment: str

    tags: List[str]
