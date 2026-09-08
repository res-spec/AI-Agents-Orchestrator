# Private Investment Office MVP

A personal research-and-execution workspace that turns market evidence into an auditable investment memo, requires an explicit human BUY/PASS decision, and routes approved orders to a paper broker by default.

## Safety defaults

- `BROKER_MODE=paper` by default.
- Live order submission is disabled unless `ENABLE_LIVE_TRADING=true` is explicitly set.
- Every order requires a previously approved investment memo.
- Position sizing is capped by portfolio percentage and absolute order value.
- No withdrawal or money-transfer functionality exists in this project.
- The first production milestone is IBKR paper trading, not live capital.

## Architecture

```text
research signals -> scorecard -> investment memo -> human BUY/PASS
                                                -> risk gate -> broker adapter
                                                             -> paper / IBKR TWS
```

The scoring engine deliberately keeps `fundamentals`, `smart_money`, `momentum`, `valuation`, `catalyst`, and `risk` separate so we can later plug in SEC filings, insider transactions, institutional holdings, earnings revisions, and Asian-market disclosures without rewriting the decision layer.

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

Open `http://127.0.0.1:8000/docs` for the API console.

## Current MVP endpoints

- `GET /health` — service and broker mode
- `POST /api/memos` — create a scored investment memo
- `GET /api/memos` — list memos
- `POST /api/memos/{id}/decision` — BUY or PASS
- `POST /api/orders/preview` — calculate safe order size before execution
- `POST /api/orders/submit` — submit an approved order (paper by default)
- `GET /api/orders` — order history
- `GET /api/portfolio` — current paper portfolio

## IBKR plan

IBKR officially supports Python through the TWS API and offers paper accounts for strategy testing. The adapter is kept behind a broker interface so paper execution and IBKR execution use the same application flow.

For the IBKR phase:
1. Open/fund the regular IBKR account.
2. Create the Paper Trading Account in Account Management.
3. Install TWS or IB Gateway and enable API access.
4. Test the complete flow against the paper account.
5. Only after audit/logging/risk checks pass do we enable live mode.

## Not yet implemented

- SEC/13F/Form 4/13D/13G collectors
- Japan/Korea/Hong Kong disclosure collectors
- earnings-revision and fundamental-data providers
- push notifications/mobile UI
- real IBKR order submission

Those are deliberately downstream of the audited decision and risk core.