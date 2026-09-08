from abc import ABC, abstractmethod

from .models import ExecutedOrder, InvestmentMemo, OrderPreview


class Broker(ABC):
    mode: str

    @abstractmethod
    def submit(self, memo: InvestmentMemo, preview: OrderPreview) -> ExecutedOrder:
        raise NotImplementedError


class PaperBroker(Broker):
    mode = "paper"

    def submit(self, memo: InvestmentMemo, preview: OrderPreview) -> ExecutedOrder:
        if preview.blocked or preview.quantity <= 0:
            return ExecutedOrder(
                memo_id=memo.id,
                symbol=memo.symbol,
                side=memo.proposed_action,
                quantity=0,
                fill_price_base=preview.price_base,
                notional_base=0,
                broker_mode=self.mode,
                status="REJECTED",
                message="Risk gate blocked this order.",
            )

        return ExecutedOrder(
            memo_id=memo.id,
            symbol=memo.symbol,
            side=memo.proposed_action,
            quantity=preview.quantity,
            fill_price_base=preview.price_base,
            notional_base=round(preview.quantity * preview.price_base, 2),
            broker_mode=self.mode,
            status="FILLED",
            broker_order_id=f"paper-{memo.id[:10]}",
            message="Simulated immediate fill. Paper fills do not model real execution quality.",
        )


class IBKRBroker(Broker):
    def __init__(self, mode: str, live_enabled: bool):
        if mode not in {"ibkr_paper", "ibkr_live"}:
            raise ValueError("Unsupported IBKR mode")
        if mode == "ibkr_live" and not live_enabled:
            raise RuntimeError("Live IBKR trading is disabled by configuration")
        self.mode = mode

    def submit(self, memo: InvestmentMemo, preview: OrderPreview) -> ExecutedOrder:
        # Intentionally fail closed until the account connection has been tested
        # against IBKR Paper Trading. The next milestone wires the official TWS API
        # here without changing the rest of the application.
        return ExecutedOrder(
            memo_id=memo.id,
            symbol=memo.symbol,
            side=memo.proposed_action,
            quantity=0,
            fill_price_base=preview.price_base,
            notional_base=0,
            broker_mode=self.mode,
            status="REJECTED",
            message="IBKR adapter is not activated yet; use paper mode until TWS/IB Gateway connectivity is verified.",
        )


def build_broker(mode: str, live_enabled: bool) -> Broker:
    if mode == "paper":
        return PaperBroker()
    return IBKRBroker(mode=mode, live_enabled=live_enabled)
