
from typing import Literal, Optional
from pydantic import BaseModel, Field


class CodeReviewRequest(BaseModel):
    language: Literal["python", "java"]
    code: str = Field(min_length=1, max_length=20000)


class Finding(BaseModel):
    severity: Literal["error", "warning", "info"]
    line: Optional[int] = None
    message: str
    suggestion: Optional[str] = None


class CodeReviewResponse(BaseModel):
    language: str
    static_findings: list[Finding]
    ai_review: Optional[dict] = None
    status: str
