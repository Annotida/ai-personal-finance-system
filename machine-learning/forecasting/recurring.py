"""
Detect recurring transactions (salary, rent, subscriptions) from transaction history.

A merchant is considered recurring if it shows up at least min_occurrences times
AND the gaps between occurrences are consistent (within gap_tolerance_pct) —
this second check is important: without it, everyday purchases that just happen
to repeat often (like a favorite coffee shop) get wrongly flagged as recurring.
"""

import pandas as pd


def detect_recurring(df, min_occurrences=3, gap_tolerance_pct=0.3):
    recurring = []
    for merchant, group in df.groupby("merchant_clean"):
        group = group.sort_values("date")
        if len(group) < min_occurrences:
            continue

        amounts = group["amount"].values
        avg_amount = amounts.mean()

        dates = pd.to_datetime(group["date"]).values
        gaps = pd.Series(dates).diff().dropna().dt.days.values
        if len(gaps) == 0:
            continue

        avg_gap = gaps.mean()
        gap_consistent = all(abs(g - avg_gap) <= avg_gap * gap_tolerance_pct for g in gaps)
        if not gap_consistent:
            continue

        recurring.append({
            "merchant": merchant,
            "avg_amount": round(avg_amount, 2),
            "frequency_days": round(avg_gap, 1),
            "occurrences": len(group),
        })
    return recurring


def project_recurring(recurring, last_known_date, start_date, end_date):
    """Project detected recurring transactions forward onto future dates."""
    events = {}
    for r in recurring:
        current = pd.Timestamp(last_known_date) + pd.Timedelta(days=r["frequency_days"])
        while current <= end_date:
            if current >= start_date:
                day = pd.Timestamp(current.date())
                events[day] = events.get(day, 0) + r["avg_amount"]
            current += pd.Timedelta(days=r["frequency_days"])
    return events
