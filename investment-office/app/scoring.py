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


def model_opinion(score: float, min_buy_score: float) -> str:
    if score >= min_buy_score:
        return "BUY"
    if score >= max(60.0, min_buy_score - 12.0):
        return "WATCH"
    return "PASS"
