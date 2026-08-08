"""
Cash-flow forecast: project a balance forward day by day using detected
recurring transactions and average daily discretionary spending.
"""

import pandas as pd

from recurring import project_recurring


def calculate_daily_spend(df, recurring_merchants):
    """Average daily spend on everything that ISN'T a recurring transaction."""
    discretionary = df[~df["merchant_clean"].isin(recurring_merchants)]
    total_days = (pd.to_datetime(df["date"]).max() - pd.to_datetime(df["date"]).min()).days
    daily_spend = discretionary[discretionary["amount"] > 0]["amount"].sum() / total_days
    return daily_spend


def forecast_balance(df, recurring, current_balance, horizon_days=30, safety_buffer=1500.0):
    start = pd.Timestamp(df["date"].max()) + pd.Timedelta(days=1)
    end = start + pd.Timedelta(days=horizon_days)

    recurring_merchants = [r["merchant"] for r in recurring]
    daily_spend = calculate_daily_spend(df, recurring_merchants)
    future_events = project_recurring(recurring, df["date"].max(), start, end)

    balance = current_balance
    low_point = current_balance
    low_date = start
    days = []

    for i in range(horizon_days + 1):
        day = start + pd.Timedelta(days=i)
        if i > 0:
            balance -= daily_spend
            balance -= future_events.get(day, 0)
        if balance < low_point:
            low_point = balance
            low_date = day
        days.append({"date": day, "balance": round(balance, 2)})

    return {
        "days": days,
        "low_point": round(low_point, 2),
        "low_date": low_date,
        "below_buffer": low_point < safety_buffer,
    }
