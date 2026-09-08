# Private Investment Office MVP

A personal research-and-execution workspace that turns market evidence into an auditable investment memo, requires an explicit human APPROVE/PASS decision, and routes approved orders to a paper broker by default.

## Safety defaults

- `BROKER_MODE=paper` by default.
- Live order submission is disabled unless `ENABLE_LIVE_TRADING=true` is explicitly set.
- Every order requires a previously approved investment memo.
- Position sizing is capped by portfolio percentage and absolute order value.
- No withdrawal or money-transfer functionality exists in this project.
- The first production milestone is IBKR paper trading, not live capital.

## Architecture

```text
research signals -> scorecard -> investment memo -> human APPROVE/PASS
                                                -> risk gate -> broker adapter
                                                             -> paper / IBKR TWS
```

The scoring engine keeps `smart_money`, `fundamentals`, `catalyst`, `momentum`, `valuation`, and `risk_quality` separate so new data sources can be added without rewriting the decision layer.

## Run locally

```bash
cd investment-office
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open:
- `http://127.0.0.1:8000/` — owner dashboard
- `http://127.0.0.1:8000/docs` — API console

## Current MVP

- `GET /health` — service, broker and research configuration status
- `GET /api/research/us/{symbol}/filings` — recent official SEC company filings
- `GET /api/research/sec/entity/{cik}/filings` — manager/entity filings such as 13F-HR
- `POST /api/memos` — create a scored investment memo
- `GET /api/memos` — list memos
- `POST /api/memos/{id}/decision` — owner APPROVE or PASS
- `POST /api/orders/preview` — calculate capped order size before execution
- `POST /api/orders/submit` — submit an approved order (local paper broker by default)
- `GET /api/orders` — audited order history
- `GET /api/portfolio` — reconstructed paper portfolio

SEC endpoints use the SEC's official JSON services. Set a real application/contact identifier in `SEC_USER_AGENT`; do not leave the placeholder value.

## IBKR plan

IBKR officially supports Python through the TWS API and provides a Paper Trading environment. The adapter is behind a broker interface so local simulation and IBKR execution share the same decision/risk flow.

Current IBKR documentation lists these defaults:
- TWS live: `7946`
- TWS paper: `7947`
- IB Gateway live: `4001`
- IB Gateway paper: `4002`

For the IBKR phase:
1. Open and complete the regular IBKR account.
2. Create/enable the Paper Trading environment when available for the account.
3. Install TWS or IB Gateway and enable API access.
4. Wire and verify account/contract/market-data connectivity.
5. Place only paper orders until fills, portfolio sync, currency conversion, and risk checks are verified.
6. Live mode remains fail-closed until explicitly enabled.

## Next build milestones

1. IBKR TWS paper connectivity and contract resolution.
2. Account equity/cash/positions synchronized directly from IBKR instead of manual inputs.
3. Market-price/FX normalization for US, Japan, Korea and Hong Kong.
4. 13F manager holdings parser and manager track-record database.
5. Form 4 / 13D / 13G signals plus fundamental and earnings-revision feeds.
6. Japan/Korea/Hong Kong disclosure adapters.
7. Daily investment-committee generation and notifications.

The system is intentionally designed so a day with no qualifying idea can return `HOLD CASH` rather than forcing a trade.