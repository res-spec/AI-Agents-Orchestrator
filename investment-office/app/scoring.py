from .models import ScoreCard


WEIGHTS = {
    "smart_money": 0.25,
    "fundamentals": 0.25,
    "catalyst": 0.15,
    "momentum": 0.15,
    "valuation": 0.10,
    "risk_quality": 0.10,
}


def committee_score(scores: ScoreCard) -> float:
    raw = sum(getattr(scores, key) * weight for key, weight in WEIGHTS.items())
    return round(raw, 2)


def committee_view(score: float, min_proceed_score: float) -> str:
    if score >= min_proceed_score:
        return "PROCEED"
    if score >= max(60.0, min_proceed_score - 12.0):
        return "WATCH"
    return "PASS"
