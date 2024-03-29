# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["StatementRetrieveResponse"]


class StatementRetrieveResponse(BaseModel):
    id: str
    """The globally unique identifier for this Statement"""

    property: object

    qualifiers: object

    rank: Literal["deprecated", "normal", "preferred"]
    """The rank of the Statement"""

    references: object

    value: object
