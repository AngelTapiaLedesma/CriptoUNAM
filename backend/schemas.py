from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class ReportStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    NEEDS_INFORMATION = "NEEDS_INFORMATION"
    VALIDATED = "VALIDATED"
    REJECTED = "REJECTED"
    PAID = "PAID"
    REMEDIATED = "REMEDIATED"
    VERIFIED = "VERIFIED"


class ReportCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    bounty_id: int = Field(alias="bountyId")

    researcher: str
    title: str
    description: str
    severity: str
    evidence: str


class ReportStatusUpdate(BaseModel):
    status: ReportStatus


class ReportResponse(BaseModel):
    id: int
    bountyId: int

    title: str
    company: str

    severity: str
    description: str

    status: ReportStatus

    researcher: str
    submittedAt: datetime

    reward: str

    evidenceHash: str

    transactionHash: str | None = None