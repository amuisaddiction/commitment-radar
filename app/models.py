from datetime import datetime, timezone
from pydantic import BaseModel, Field

def utc_now():
    return datetime.now(timezone.utc)

class IngestRequest(BaseModel):
    transcript: str = Field(min_length=3, max_length=20000)
    source: str = "manual_demo"
    captured_at: datetime = Field(default_factory=utc_now)

class Commitment(BaseModel):
    id: str
    task: str
    owner: str | None = None
    recipient: str | None = None
    due_date: str | None = None
    source_text: str
    source: str = "manual_demo"
    confidence: float = 0.65
    created_at: datetime = Field(default_factory=utc_now)
    status: str = "open"

class Conflict(BaseModel):
    id: str
    title: str
    explanation: str
    severity: str = "medium"
    current_commitment_id: str
    related_commitment_id: str | None = None
    evidence: list[str] = Field(default_factory=list)
    suggested_message: str = ""
    created_at: datetime = Field(default_factory=utc_now)
