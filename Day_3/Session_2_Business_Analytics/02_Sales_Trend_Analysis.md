#  Sales Trend Analysis

> **Learning Goal:** Learn how to spot patterns, seasonality, and growth in time-series retail data.

---

## 1 Seasonality and Cyclical Patterns

**Seasonality** refers to fluctuations that repeat over a specific period (e.g., Diwali spikes).

- **Month-over-Month (MoM)**: Tracking general business sanity.
- **Year-over-Year (YoY)**: The gold standard. "Did we do better this December than last December?"

---

## 2 Moving Averages (Smoothing)

Daily sales data is often "noisy". Analysts use **moving averages** to smooth out the noise.

```python
# Pandas Example
df['rolling_sales'] = df['amount'].rolling(window=7).mean()
```

---

##  Industry Case: The "Mid-Month Dip"

Many Indian retailers see a dip in sales around the 15th20th of the month.
- **Observation**: Salaries are running low.
- **Business Decision**: Launch "Budget Week" flash sales during the 15th20th.

---

##  Quick Check Questions

1. What is the difference between MoM and YoY growth?
2. Why is a rolling average better than raw daily data?
