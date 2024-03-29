# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ...._models import BaseModel

__all__ = ["SitelinkUpdateSiteIDResponse"]


class SitelinkUpdateSiteIDResponse(BaseModel):
    badges: Optional[List[str]] = None

    title: Optional[str] = None

    url: Optional[str] = None
