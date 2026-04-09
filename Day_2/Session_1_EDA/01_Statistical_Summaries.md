# 📊 Statistical Summaries in EDA

> **Learning Goal:** Learn how to quickly understand a dataset using statistical measures — before writing a single line of complex code.

---

## 🔍 What Is EDA?

**Exploratory Data Analysis (EDA)** is the first thing a data analyst does after cleaning data.

Think of it like a **doctor's first examination** of a patient:
- Check height, weight, blood pressure (→ summary statistics)
- Look for anything unusual (→ outliers)
- See how different things relate (→ correlation)

> "In God we trust. All others must bring data." — W. Edwards Deming

---

## 📐 Measures of Central Tendency

These tell you **where the middle of your data is**.

| Measure | Formula | Best For |
|---------|---------|----------|
| **Mean** | Sum ÷ Count | Normal data, no extreme outliers |
| **Median** | Middle value | Data with outliers (e.g., incomes) |
| **Mode** | Most frequent | Categorical data |

### 🧮 Real Example: Student Marks

Marks: `[60, 65, 70, 72, 78, 80, 85, 88, 92, 95]`

- **Mean** = (60+65+...+95) ÷ 10 = **78.5**
- **Median** = (78+80) ÷ 2 = **79** ← middle two values
- **Mode** = No repeat → no mode in this case

> 💡 **When to use Median over Mean?**
> If Bill Gates walks into a room of 10 average people, the **mean** income shoots up dramatically. But the **median** barely changes. For income, housing prices — always use median!

---

## 📏 Measures of Spread (Dispersion)

These tell you **how spread out your data is**.

| Measure | What It Tells You |
|---------|-------------------|
| **Range** | Max − Min (simple but sensitive to outliers) |
| **Variance** | Average of squared differences from mean |
| **Standard Deviation (SD)** | Square root of variance — same unit as data |
| **IQR** | Q3 − Q1 — middle 50% spread, outlier-resistant |

### 📦 Understanding the 5-Number Summary

```
Min ──── Q1 ──── Median ──── Q3 ──── Max
         |←── IQR (Q3−Q1) ──→|
```

| Term | Meaning |
|------|---------|
| **Min** | Smallest value |
| **Q1 (25th percentile)** | 25% of values fall below this |
| **Median (50th percentile)** | Middle value |
| **Q3 (75th percentile)** | 75% of values fall below this |
| **Max** | Largest value |
| **IQR** | Q3 − Q1 (middle 50% of data) |

---

## 🐼 Using Pandas for Statistical Summaries

```python
import pandas as pd

df = pd.read_csv("students_data.csv")

# One command → everything!
df.describe()
```

**Output explained:**

```
       marks  study_hours  attendance
count   10.0        10.0        10.0   ← number of non-null values
mean    78.3         5.5        84.0   ← average
std     11.4         1.6         8.9   ← standard deviation
min     60.0         3.0        70.0   ← smallest
25%     68.8         4.0        78.0   ← Q1
50%     78.5         5.5        84.0   ← median
75%     87.0         6.5        90.0   ← Q3
max     95.0         8.0        98.0   ← largest
```

### 📌 Individual Statistics

```python
df["marks"].mean()      # Average
df["marks"].median()    # Middle value
df["marks"].std()       # Standard deviation
df["marks"].min()       # Minimum
df["marks"].max()       # Maximum
df["marks"].quantile(0.25)   # Q1
df["marks"].quantile(0.75)   # Q3
df["marks"].value_counts()   # Frequency count (great for categories)
```

---

## 📊 Frequency Distribution

Shows how many times each value (or range of values) appears.

```python
# For categorical data
df["city"].value_counts()

# For numerical data (group into ranges)
pd.cut(df["marks"], bins=[50, 60, 70, 80, 90, 100]).value_counts()
```

**Output:**
```
city
Chennai      4
Bangalore    3
Hyderabad    3

marks range
(70, 80]     3
(80, 90]     3
(90, 100]    2
(60, 70]     2
```

---

## 🌍 Real-World Example: E-Commerce

> An e-commerce company wants to understand customer spending:
> - **Mean** order value: ₹2,400 → typical spend
> - **Median** order value: ₹1,800 → better middle (a few expensive orders pull mean up)
> - **Std Dev**: ₹3,200 → HIGH variation → customers are very different!
> - **IQR**: ₹800–₹3,500 → most customers fall in this range

**Decision:** Create different product bundles for ₹500, ₹1500, ₹3500 price points to match customer segments.

---

## ✅ Key Takeaways

1. **Always run `.describe()` first** on any new dataset
2. Use **mean** for data without outliers, **median** for data with extreme values
3. **High std deviation** = data is very spread out → investigate!
4. **IQR** (Q3−Q1) is the most useful measure of spread
5. `value_counts()` is great for understanding categorical columns

---

## 🧠 Quick Check Questions

1. If a dataset has a mean of 50 and median of 30, what does this tell you?
2. A class has marks: [45, 50, 52, 55, 99]. Which is a better summary — mean or median?
3. What does a standard deviation of 0 mean?
4. Why is IQR better than range for detecting spread?

---

*Next Topic → [Correlation Analysis](./02_Correlation_Analysis.md)*
