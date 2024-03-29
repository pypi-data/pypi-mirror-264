# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["StatementListParams"]


class StatementListParams(TypedDict, total=False):
    property: str
    """Single property ID to filter statements by."""
