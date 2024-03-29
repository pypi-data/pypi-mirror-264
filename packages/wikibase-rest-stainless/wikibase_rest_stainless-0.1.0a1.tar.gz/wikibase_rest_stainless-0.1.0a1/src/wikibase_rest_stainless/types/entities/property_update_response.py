# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = [
    "PropertyUpdateResponse",
    "Statement",
    "StatementProperty",
    "StatementQualifier",
    "StatementQualifierProperty",
    "StatementQualifierValue",
    "StatementReference",
    "StatementReferencePart",
    "StatementReferencePartProperty",
    "StatementReferencePartValue",
    "StatementValue",
]


class StatementProperty(BaseModel):
    id: Optional[str] = None
    """The ID of the Property"""

    data_type: Optional[str] = FieldInfo(alias="data-type", default=None)
    """The data type of the Property"""


class StatementQualifierProperty(BaseModel):
    id: Optional[str] = None
    """The ID of the Property"""

    data_type: Optional[str] = FieldInfo(alias="data-type", default=None)
    """The data type of the Property"""


class StatementQualifierValue(BaseModel):
    content: Optional[object] = None
    """The value, if type == "value", otherwise omitted"""

    type: Optional[Literal["value", "somevalue", "novalue"]] = None
    """The value type"""


class StatementQualifier(BaseModel):
    property: Optional[StatementQualifierProperty] = None

    value: Optional[StatementQualifierValue] = None


class StatementReferencePartProperty(BaseModel):
    id: Optional[str] = None
    """The ID of the Property"""

    data_type: Optional[str] = FieldInfo(alias="data-type", default=None)
    """The data type of the Property"""


class StatementReferencePartValue(BaseModel):
    content: Optional[object] = None
    """The value, if type == "value", otherwise omitted"""

    type: Optional[Literal["value", "somevalue", "novalue"]] = None
    """The value type"""


class StatementReferencePart(BaseModel):
    property: Optional[StatementReferencePartProperty] = None

    value: Optional[StatementReferencePartValue] = None


class StatementReference(BaseModel):
    hash: Optional[str] = None
    """Hash of the Reference"""

    parts: Optional[List[StatementReferencePart]] = None


class StatementValue(BaseModel):
    content: Optional[object] = None
    """The value, if type == "value", otherwise omitted"""

    type: Optional[Literal["value", "somevalue", "novalue"]] = None
    """The value type"""


class Statement(BaseModel):
    id: Optional[str] = None
    """The globally unique identifier for this Statement"""

    property: Optional[StatementProperty] = None

    qualifiers: Optional[List[StatementQualifier]] = None

    rank: Optional[Literal["deprecated", "normal", "preferred"]] = None
    """The rank of the Statement"""

    references: Optional[List[StatementReference]] = None

    value: Optional[StatementValue] = None


class PropertyUpdateResponse(BaseModel):
    id: str

    aliases: Dict[str, List[str]]

    data_type: str = FieldInfo(alias="data-type")

    descriptions: Dict[str, str]

    labels: Dict[str, str]

    statements: Dict[str, List[Statement]]

    type: str
