# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

__all__ = ["SitelinkUpdateSiteIDParams", "Sitelink"]


class SitelinkUpdateSiteIDParams(TypedDict, total=False):
    item_id: Required[str]

    sitelink: Required[Sitelink]

    bot: bool

    comment: str

    tags: List[str]


class Sitelink(TypedDict, total=False):
    title: Required[str]

    badges: List[str]
