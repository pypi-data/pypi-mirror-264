# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["PropertyRetrieveParams"]


class PropertyRetrieveParams(TypedDict, total=False):
    _fields: List[Literal["type", "data-type", "labels", "descriptions", "aliases", "statements"]]
    """Comma-separated list of fields to include in each response object."""
