from datetime import datetime, timezone
from enum import Enum
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class HumanDecision(str, Enum):
    APPROVE = "APPROVE"
    PASS = "PASS"


class ProposedAction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class ScoreCard(BaseModel):
    smart_money: float = Field(ge=0, le=100)
    fundamentals: float = Field(ge=0, le=100)
    catalyst: float = Field(ge=0, le=100)
    momentum: float = Field(ge=0, le=100)
    valuation: float = Field(ge=0, le=100)
    risk_quality: float = Field(ge=0, le=100, description="100 means lower/better-understood risk")


class EvidenceItem(BaseModel):
    kind: str = Field(min_length=1, max_length=80)
    source: str = Field(min_length=1, max_length=240)
    summary: str = Field(min_length=1, max_length=1200)
    observed_at: datetime | None = None
    stale_after_days: int | None = Field(default=None, ge=0, le=3650)


class MemoCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=24)
    market: str = Field(min_length=1, max_length=40)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    proposed_action: ProposedAction = ProposedAction.BUY
    thesis: str = Field(min_length=10, max_length=4000)
    bear_case: str = Field(min_length=10, max_length=4000)
    scores: ScoreCard
    evidence: list[EvidenceItem] = Field(default_factory=list)

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return value.strip().upper()


class InvestmentMemo(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    symbol: str
    market: str
    currency: str
    proposed_action: ProposedAction
    thesis: str
    bear_case: str
    scores: ScoreCard
    evidence: list[EvidenceItem]
    committee_score: float
    model_opinion: Literal["BUY", "WATCH", "PASS"]
    human_decision: HumanDecision | None = None
    created_at: datetime = Field(default_factory=utc_now)
    decided_at: datetime | None = None


class DecisionRequest(BaseModel):
    decision: HumanDecision
    note: str | None = Field(default=None, max_length=1000)


class OrderPreviewRequest(BaseModel):
    memo_id: str
    price_base: float = Field(gt=0, description="Instrument price converted to portfolio base currency")
    portfolio_equity_base: float = Field(gt=0)
    current_position_value_base: float = Field(default=0, ge=0)
    requested_notional_base: float | None = Field(default=None, gt=0)


class OrderPreview(BaseModel):
    memo_id: str
    symbol: str
    side: ProposedAction
    price_base: float
    max_allowed_notional_base: float
    approved_notional_base: float
    quantity: float
    blocked: bool
    reasons: list[str] = Field(default_factory=list)


class OrderSubmitRequest(OrderPreviewRequest):
    explicit_confirmation: Literal["EXECUTE"]


class ExecutedOrder(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    memo_id: str
    symbol: str
    side: ProposedAction
    quantity: float
    fill_price_base: float
    notional_base: float
    broker_mode: str
    status: Literal["FILLED", "REJECTED"]
    created_at: datetime = Field(default_factory=utc_now)
    broker_order_id: str | None = None
    message: str | None = None


class Position(BaseModel):
    symbol: str
    quantity: float
    average_cost_base: float
    cost_basis_base: float
