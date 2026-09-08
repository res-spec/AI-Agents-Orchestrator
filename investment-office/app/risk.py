import math

from .config import Settings
from .models import InvestmentMemo, OrderPreview, OrderPreviewRequest, ProposedAction


def preview_order(memo: InvestmentMemo, request: OrderPreviewRequest, settings: Settings) -> OrderPreview:
    reasons: list[str] = []

    if memo.human_decision is None or memo.human_decision.value != "APPROVE":
        reasons.append("Investment memo has not been explicitly approved by the owner.")

    if memo.committee_view == "PASS":
        reasons.append("Committee view is PASS; manual approval alone does not bypass the risk gate.")

    if memo.proposed_action == ProposedAction.BUY:
        room = max(
            0.0,
            request.portfolio_equity_base * settings.max_position_pct - request.current_position_value_base,
        )
        max_allowed = min(settings.max_single_order_base, room)
        if max_allowed <= 0:
            reasons.append("Position cap leaves no room for an additional buy order.")
    else:
        max_allowed = min(settings.max_single_order_base, request.current_position_value_base)
        if request.current_position_value_base <= 0:
            reasons.append("There is no recorded position available to sell.")

    desired = max_allowed
    if request.requested_notional_base is not None:
        desired = min(request.requested_notional_base, max_allowed)

    if settings.allow_fractional:
        quantity = desired / request.price_base if desired > 0 else 0.0
    else:
        quantity = math.floor(desired / request.price_base) if desired > 0 else 0.0
        desired = quantity * request.price_base
        if quantity <= 0:
            reasons.append("Order is below the cost of one whole share; fractional trading is disabled.")

    blocked = bool(reasons)

    return OrderPreview(
        memo_id=memo.id,
        symbol=memo.symbol,
        side=memo.proposed_action,
        price_base=request.price_base,
        max_allowed_notional_base=round(max_allowed, 2),
        approved_notional_base=round(desired if not blocked else 0.0, 2),
        quantity=round(quantity if not blocked else 0.0, 6),
        blocked=blocked,
        reasons=reasons,
    )
