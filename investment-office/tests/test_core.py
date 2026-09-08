from pathlib import Path

from app.config import Settings
from app.models import (
    HumanDecision,
    InvestmentMemo,
    OrderPreviewRequest,
    ProposedAction,
    ScoreCard,
)
from app.risk import preview_order
from app.scoring import committee_score, committee_view


def test_committee_score_is_weighted_and_transparent():
    scores = ScoreCard(
        smart_money=90,
        fundamentals=80,
        catalyst=70,
        momentum=60,
        valuation=50,
        risk_quality=40,
    )
    assert committee_score(scores) == 71.0
    assert committee_view(71.0, 72.0) == "WATCH"


def test_unapproved_order_is_blocked():
    settings = Settings(
        database_path=Path(":memory:"),
        max_position_pct=0.05,
        max_single_order_base=100,
        allow_fractional=False,
    )
    memo = InvestmentMemo(
        symbol="AAPL",
        market="US",
        currency="USD",
        proposed_action=ProposedAction.BUY,
        thesis="Strong enough thesis for a deterministic unit test.",
        bear_case="Strong enough bear case for a deterministic unit test.",
        scores=ScoreCard(
            smart_money=90,
            fundamentals=90,
            catalyst=90,
            momentum=90,
            valuation=90,
            risk_quality=90,
        ),
        evidence=[],
        committee_score=90,
        committee_view="PROCEED",
    )
    request = OrderPreviewRequest(
        memo_id=memo.id,
        price_base=20,
        portfolio_equity_base=1000,
        current_position_value_base=0,
    )
    result = preview_order(memo, request, settings)
    assert result.blocked is True
    assert result.quantity == 0


def test_approved_order_respects_position_cap():
    settings = Settings(
        database_path=Path(":memory:"),
        max_position_pct=0.05,
        max_single_order_base=100,
        allow_fractional=False,
    )
    memo = InvestmentMemo(
        symbol="AAPL",
        market="US",
        currency="USD",
        proposed_action=ProposedAction.BUY,
        thesis="Strong enough thesis for a deterministic unit test.",
        bear_case="Strong enough bear case for a deterministic unit test.",
        scores=ScoreCard(
            smart_money=90,
            fundamentals=90,
            catalyst=90,
            momentum=90,
            valuation=90,
            risk_quality=90,
        ),
        evidence=[],
        committee_score=90,
        committee_view="PROCEED",
        human_decision=HumanDecision.APPROVE,
    )
    request = OrderPreviewRequest(
        memo_id=memo.id,
        price_base=20,
        portfolio_equity_base=1000,
        current_position_value_base=0,
        requested_notional_base=80,
    )
    result = preview_order(memo, request, settings)
    assert result.blocked is False
    assert result.max_allowed_notional_base == 50
    assert result.quantity == 2
    assert result.approved_notional_base == 40
