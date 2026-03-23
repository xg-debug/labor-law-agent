from typing import Literal

from pydantic import BaseModel, Field


class MessageItem(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str = Field(min_length=1)


class LawReference(BaseModel):
    name: str
    summary: str
    source: str


class RiskItem(BaseModel):
    title: str
    level: str
    description: str
    suggestion: str


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    history: list[MessageItem] = Field(default_factory=list)


class ChatResponse(BaseModel):
    question_summary: str
    facts: list[str]
    issues: list[str]
    law_references: list[LawReference]
    analysis: str
    conclusion: str
    risk_tips: list[str]
    suggestions: list[str]
    evidence_list: list[str]


class ContractReviewRequest(BaseModel):
    contract_text: str = Field(min_length=1)


class ContractReviewResponse(BaseModel):
    contract_type: str
    review_items: list[str]
    risks: list[RiskItem]
    suggestions: list[str]
    law_references: list[LawReference]


class DocumentGenerateRequest(BaseModel):
    doc_type: str = Field(min_length=1)
    facts: str = Field(min_length=1)
    claim: str = Field(min_length=1)
    context: str = ""


class DocumentGenerateResponse(BaseModel):
    title: str
    content: str
    usage_notes: str
    risk_tips: list[str]


class HealthResponse(BaseModel):
    status: str
    service: str
