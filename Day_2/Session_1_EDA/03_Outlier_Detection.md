*  Outlier Detection

> **Learning Goal:** Learn to identify data points that are unusually different from the rest — they can either be errors to fix or rare insights to study!

---

##  What Is an Outlier?

An **outlier** is a data point that is **significantly different** from the rest of the data.

### Real-Life Examples:

| Dataset                | Normal Range  | Outlier                        |
| ---------------------- | ------------- | ------------------------------ |
| Student marks (0–100) | 50–90        | **2** or **150**   |
| Monthly salary         | ₹20k–₹1L   | **₹1 crore** (CEO!)     |
| Product price          | ₹100–₹5000 | **-₹500** (data error!) |
| Human height           | 150–190 cm   | **230 cm**               |

> ⚠️ Not all outliers are errors! Sometimes they're the **most interesting data points**.

---

##  Types of Outliers

### 1. Point Outlier (Most Common)

A single value that is far from the others.

```
Data: [70, 72, 75, 78, 80, 82, 85, 138]
                                   ^^^
                               Outlier!
```

### 2. Contextual Outlier

Normal in one context, unusual in another.

- ₹50,000 salary is normal for a junior developer
- ₹50,000 salary is an outlier for a senior manager

### 3. Collective Outlier

A group of points that together are unusual.

- All transactions from one IP address in 5 minutes (possible fraud!)

---

##  Method 1: IQR Method (Most Common)

The **Interquartile Range (IQR)** method finds outliers using Q1 and Q3.

```
Lower Fence = Q1 - (1.5 × IQR)
Upper Fence = Q3 + (1.5 × IQR)

Anything outside the fences = OUTLIER
```

### Step-by-Step Example:

```python
import pandas as pd

df = pd.read_csv("students_data.csv")

Q1 = df["marks"].quantile(0.25)   # 68.75
Q3 = df["marks"].quantile(0.75)   # 87.00
IQR = Q3 - Q1                     # 18.25

lower_fence = Q1 - 1.5 * IQR     # 68.75 - 27.37 = 41.38
upper_fence = Q3 + 1.5 * IQR     # 87.00 + 27.37 = 114.37

print(f"Q1={Q1}, Q3={Q3}, IQR={IQR}")
print(f"Outlier range: below {lower_fence:.2f} or above {upper_fence:.2f}")

# Find outliers
outliers = df[(df["marks"] < lower_fence) | (df["marks"] > upper_fence)]
print(f"\nOutliers found:\n{outliers[['name', 'marks']]}")
```

---

##  Method 2: Z-Score Method

The **Z-score** tells you how many standard deviations a value is from the mean.

```
Z-score = (value - mean) / std_deviation

Rule: |Z| > 3 → Outlier
```

```python
from scipy import stats
import numpy as np

z_scores = stats.zscore(df["marks"])
print("\nZ-scores for marks:")
for name, score, z in zip(df["name"], df["marks"], z_scores):
    flag = " ← OUTLIER!" if abs(z) > 2 else ""
    print(f"  {name:10s}: {score}  (z={z:.2f}){flag}")
```

| Student        | Marks | Z-score | Status             |
| -------------- | ----- | ------- | ------------------ |
| Divya          | 60    | -1.57   | Normal             |
| Vikram         | 95    | +1.43   | Normal             |
| (hypothetical) | 20    | -5.0    | **Outlier!** |

---

##  Method 3: Boxplot (Visual Method)

The **boxplot** is the fastest visual way to spot outliers.

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(12, 5))

for ax, col in zip(axes, ["marks", "study_hours", "attendance"]):
    ax.boxplot(df[col].dropna(), patch_artist=True,
               boxprops=dict(facecolor="lightblue"),
               medianprops=dict(color="red", linewidth=2))
    ax.set_title(f"{col}")
    ax.set_ylabel("Value")

plt.suptitle("Boxplots — Outliers appear as dots above/below whiskers")
plt.tight_layout()
plt.show()
```

### Reading a Boxplot:

```
         ┌────────────────────┐
    ●    │    ████████████    │         ●   ● ← Individual outlier dots
         │       ████         │
─────────┼────────────────────┼──────────────
        Q1     Median        Q3
         │←────── IQR ───────→│
         │                    │
     Min whisker          Max whisker
     (Q1 - 1.5×IQR)      (Q3 + 1.5×IQR)
```

---

##  What To Do With Outliers?

| Option                   | When to Use                                           |
| ------------------------ | ----------------------------------------------------- |
| **Keep it**        | It's real, genuine data (e.g., a real genius student) |
| **Remove it**      | It's clearly a data entry error (e.g., marks = -50)   |
| **Cap it**         | Replace with max/min boundary (Winsorization)         |
| **Investigate it** | Fraud detection, quality control                      |

### Decision Flowchart:

```
Is the outlier a data ERROR?
    ├── YES → Remove or correct it
    └── NO  → Is it a rare but valid case?
                   ├── YES → Keep it, note it
                   └── NO  → Investigate further!
```

---

##  Real-World Importance

| Domain                  | Why Outliers Matter                                      |
| ----------------------- | -------------------------------------------------------- |
| **Banking**       | One ₹50 lakh transaction in a student account → Fraud! |
| **Manufacturing** | One defective batch in 10,000 → Recall before damage    |
| **Healthcare**    | One patient with 400 blood pressure → Emergency!        |
| **E-commerce**    | Negative quantity order → Data bug → Fix immediately   |

---

## ✅ Key Takeaways

1. Outliers are data points far from the rest
2. Use **IQR method** (Q1 - 1.5×IQR, Q3 + 1.5×IQR) to detect them
3. Use **Z-score** for normally distributed data (|z| > 3)
4. **Boxplots** visually show outliers as dots
5. Always ask: is this outlier an **error** or a **genuine rare value**?

---

##  Quick Check Questions

1. A student scored 200 marks out of 100. What type of issue is this?
2. Calculate the IQR for: [10, 20, 25, 30, 35, 40, 100]
3. Billionaires in a salary dataset — remove or keep?
4. What does a Z-score of -3.5 mean?

---

*Next: Session 2 → [Chart Selection Principles](../Session_2_Visualization_Fundamentals/01_Chart_Selection_Principles.md)*
