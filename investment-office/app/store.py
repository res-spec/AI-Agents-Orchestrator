import json
import sqlite3
from pathlib import Path

from .models import ExecutedOrder, InvestmentMemo, Position


class Repository:
    def __init__(self, path: Path):
        self.path = path
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memos (
                    id TEXT PRIMARY KEY,
                    payload TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS orders (
                    id TEXT PRIMARY KEY,
                    payload TEXT NOT NULL
                )
                """
            )

    def save_memo(self, memo: InvestmentMemo) -> None:
        payload = memo.model_dump_json()
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO memos(id, payload) VALUES(?, ?)",
                (memo.id, payload),
            )

    def get_memo(self, memo_id: str) -> InvestmentMemo | None:
        with self._connect() as conn:
            row = conn.execute("SELECT payload FROM memos WHERE id = ?", (memo_id,)).fetchone()
        return InvestmentMemo.model_validate_json(row["payload"]) if row else None

    def list_memos(self) -> list[InvestmentMemo]:
        with self._connect() as conn:
            rows = conn.execute("SELECT payload FROM memos ORDER BY rowid DESC").fetchall()
        return [InvestmentMemo.model_validate_json(row["payload"]) for row in rows]

    def save_order(self, order: ExecutedOrder) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO orders(id, payload) VALUES(?, ?)",
                (order.id, order.model_dump_json()),
            )

    def list_orders(self) -> list[ExecutedOrder]:
        with self._connect() as conn:
            rows = conn.execute("SELECT payload FROM orders ORDER BY rowid DESC").fetchall()
        return [ExecutedOrder.model_validate_json(row["payload"]) for row in rows]

    def positions(self) -> list[Position]:
        lots: dict[str, dict[str, float]] = {}
        for order in reversed(self.list_orders()):
            if order.status != "FILLED":
                continue
            state = lots.setdefault(order.symbol, {"quantity": 0.0, "cost": 0.0})
            if order.side.value == "BUY":
                state["quantity"] += order.quantity
                state["cost"] += order.notional_base
            else:
                if state["quantity"] <= 0:
                    continue
                avg = state["cost"] / state["quantity"]
                sold = min(order.quantity, state["quantity"])
                state["quantity"] -= sold
                state["cost"] -= avg * sold

        result: list[Position] = []
        for symbol, state in lots.items():
            qty = state["quantity"]
            if qty <= 1e-9:
                continue
            result.append(
                Position(
                    symbol=symbol,
                    quantity=round(qty, 6),
                    average_cost_base=round(state["cost"] / qty, 4),
                    cost_basis_base=round(state["cost"], 2),
                )
            )
        return sorted(result, key=lambda item: item.symbol)
