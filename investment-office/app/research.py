from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx


SEC_BASE = "https://data.sec.gov"
SEC_FILES = "https://www.sec.gov/files"


@dataclass(frozen=True)
class CompanyRef:
    ticker: str
    cik: int
    title: str


class SECClient:
    """Thin client for official SEC JSON endpoints.

    SEC asks automated clients to identify themselves. Pass a descriptive
    user-agent containing an application/contact identifier, for example
    `PrivateInvestmentOffice contact@example.com`.
    """

    def __init__(self, user_agent: str, timeout: float = 20.0):
        if not user_agent or "replace" in user_agent.lower():
            raise ValueError("A real SEC user-agent/contact identifier is required")
        self.client = httpx.Client(
            headers={"User-Agent": user_agent, "Accept-Encoding": "gzip, deflate"},
            timeout=timeout,
            follow_redirects=True,
        )

    def close(self) -> None:
        self.client.close()

    def company_directory(self) -> dict[str, CompanyRef]:
        response = self.client.get(f"{SEC_FILES}/company_tickers.json")
        response.raise_for_status()
        payload = response.json()
        result: dict[str, CompanyRef] = {}
        for row in payload.values():
            ticker = row["ticker"].upper()
            result[ticker] = CompanyRef(
                ticker=ticker,
                cik=int(row["cik_str"]),
                title=row["title"],
            )
        return result

    def submissions(self, cik: int) -> dict[str, Any]:
        response = self.client.get(f"{SEC_BASE}/submissions/CIK{cik:010d}.json")
        response.raise_for_status()
        return response.json()

    def company_facts(self, cik: int) -> dict[str, Any]:
        response = self.client.get(f"{SEC_BASE}/api/xbrl/companyfacts/CIK{cik:010d}.json")
        response.raise_for_status()
        return response.json()

    @staticmethod
    def recent_filings(submissions_payload: dict[str, Any], forms: set[str] | None = None) -> list[dict[str, Any]]:
        recent = submissions_payload.get("filings", {}).get("recent", {})
        keys = ["accessionNumber", "filingDate", "reportDate", "form", "primaryDocument"]
        rows = zip(*(recent.get(key, []) for key in keys))
        output = []
        for accession, filing_date, report_date, form, primary_document in rows:
            if forms and form not in forms:
                continue
            output.append(
                {
                    "accession_number": accession,
                    "filing_date": filing_date,
                    "report_date": report_date,
                    "form": form,
                    "primary_document": primary_document,
                }
            )
        return output
