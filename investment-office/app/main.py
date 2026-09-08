from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from .broker import build_broker
from .config import settings
from .models import (
    DecisionRequest,
    ExecutedOrder,
    InvestmentMemo,
    MemoCreate,
    OrderPreview,
    OrderPreviewRequest,
    OrderSubmitRequest,
    Position,
)
from .risk import preview_order
from .scoring import committee_score, committee_view
from .store import Repository


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Personal investment-research and human-approved execution API.",
)
repo = Repository(settings.database_path)
broker = build_broker(settings.broker_mode, settings.enable_live_trading)
WEB_INDEX = Path(__file__).parent / "web" / "index.html"


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse(WEB_INDEX)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "broker_mode": settings.broker_mode,
        "live_trading_enabled": settings.enable_live_trading,
        "min_committee_score": settings.min_committee_score,
    }


@app.post("/api/memos", response_model=InvestmentMemo)
def create_memo(payload: MemoCreate) -> InvestmentMemo:
    score = committee_score(payload.scores)
    memo = InvestmentMemo(
        **payload.model_dump(),
        committee_score=score,
        committee_view=committee_view(score, settings.min_committee_score),
    )
    repo.save_memo(memo)
    return memo


@app.get("/api/memos", response_model=list[InvestmentMemo])
def list_memos() -> list[InvestmentMemo]:
    return repo.list_memos()


@app.get("/api/memos/{memo_id}", response_model=InvestmentMemo)
def get_memo(memo_id: str) -> InvestmentMemo:
    memo = repo.get_memo(memo_id)
    if not memo:
        raise HTTPException(status_code=404, detail="Investment memo not found")
    return memo


@app.post("/api/memos/{memo_id}/decision", response_model=InvestmentMemo)
def decide_memo(memo_id: str, payload: DecisionRequest) -> InvestmentMemo:
    memo = repo.get_memo(memo_id)
    if not memo:
        raise HTTPException(status_code=404, detail="Investment memo not found")

    memo.human_decision = payload.decision
    memo.decided_at = datetime.now(timezone.utc)
    repo.save_memo(memo)
    return memo


def _require_memo(memo_id: str) -> InvestmentMemo:
    memo = repo.get_memo(memo_id)
    if not memo:
        raise HTTPException(status_code=404, detail="Investment memo not found")
    return memo


@app.post("/api/orders/preview", response_model=OrderPreview)
def order_preview(payload: OrderPreviewRequest) -> OrderPreview:
    memo = _require_memo(payload.memo_id)
    return preview_order(memo, payload, settings)


@app.post("/api/orders/submit", response_model=ExecutedOrder)
def submit_order(payload: OrderSubmitRequest) -> ExecutedOrder:
    memo = _require_memo(payload.memo_id)
    preview = preview_order(memo, payload, settings)

    if preview.blocked:
        raise HTTPException(
            status_code=409,
            detail={"message": "Order blocked by risk gate", "reasons": preview.reasons},
        )

    if settings.broker_mode == "ibkr_live" and not settings.enable_live_trading:
        raise HTTPException(status_code=403, detail="Live trading is disabled")

    order = broker.submit(memo, preview)
    repo.save_order(order)
    return order


@app.get("/api/orders", response_model=list[ExecutedOrder])
def list_orders() -> list[ExecutedOrder]:
    return repo.list_orders()


@app.get("/api/portfolio", response_model=list[Position])
def portfolio() -> list[Position]:
    return repo.positions()
