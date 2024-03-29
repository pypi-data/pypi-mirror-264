# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from ...._models import BaseModel

__all__ = ["SitelinkUpdateResponse", "SitelinkUpdateResponseItem"]


class SitelinkUpdateResponseItem(BaseModel):
    badges: Optional[List[str]] = None

    title: Optional[str] = None

    url: Optional[str] = None


SitelinkUpdateResponse = Dict[str, SitelinkUpdateResponseItem]
