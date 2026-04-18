#  Chart Selection Principles

> **Learning Goal:** Learn HOW to pick the right chart for the right data — the most common mistake beginners make is using the wrong chart type!

---

##  Why Chart Selection Matters

> "A good chart makes data obvious. A bad chart makes people confused — or worse, misleads them."

Imagine explaining student performance:
- Using a **line chart** for city-wise marks comparison → confusing (implies a trend over time)
- Using a **bar chart** for city-wise marks comparison → perfect (comparison across categories)

**Right chart = Right insight → Right decision.**

---

## ️ The Chart Selection Guide

| What You Want to Show | Best Chart Type |
|----------------------|-----------------|
| Compare categories (city, gender) | **Bar Chart** |
| Show trend over time | **Line Chart** |
| Show part of whole (%) | **Pie / Donut Chart** |
| Show distribution of values | **Histogram** |
| Spot outliers and spread | **Boxplot** |
| Show relationship between 2 variables | **Scatter Plot** |
| Show correlation across many variables | **Heatmap** |
| Compare multiple categories + sub-groups | **Grouped Bar Chart** |
| Show frequency of occurrence | **Count Plot / Bar** |

---

##  Chart Type 1: Bar Chart

**Use when:** Comparing values across categories (cities, genders, products)

```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("students_data.csv")
avg_by_city = df.groupby("city")["marks"].mean().sort_values(ascending=False)

plt.figure(figsize=(7, 4))
plt.bar(avg_by_city.index, avg_by_city.values,
        color=["steelblue", "coral", "seagreen"], edgecolor="black")
plt.title("Average Marks by City")
plt.xlabel("City")
plt.ylabel("Average Marks")
plt.tight_layout()
plt.show()
```

**When NOT to use:** Time series data (use line chart instead)

---

##  Chart Type 2: Line Chart

**Use when:** Showing trends over time (monthly sales, daily temperature)

```python
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales  = [45000, 52000, 48000, 61000, 58000, 67000]

plt.figure(figsize=(8, 4))
plt.plot(months, sales, marker="o", linewidth=2,
         color="steelblue", markersize=8)
plt.fill_between(months, sales, alpha=0.1, color="steelblue")  # Area under line
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales (₹)")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

**When NOT to use:** Categorical comparisons (use bar chart instead)

---

##  Chart Type 3: Pie Chart

**Use when:** Showing how a whole is divided (market share, budget allocation)

```python
city_counts = df["city"].value_counts()

plt.figure(figsize=(6, 6))
plt.pie(city_counts, labels=city_counts.index, autopct="%1.1f%%",
        colors=["steelblue", "coral", "seagreen"],
        explode=[0.05, 0, 0],  # Slightly pull out the first slice
        startangle=90)
plt.title("Students by City")
plt.tight_layout()
plt.show()
```

> ⚠️ **Pie Chart Warning:** Avoid when you have more than 5-6 slices — it becomes unreadable!

---

##  Chart Type 4: Histogram

**Use when:** Showing the distribution/frequency of a numerical variable

```python
plt.figure(figsize=(7, 4))
plt.hist(df["marks"], bins=6, color="steelblue",
         edgecolor="black", alpha=0.8)
plt.axvline(df["marks"].mean(), color="red", linestyle="--",
            label=f"Mean = {df['marks'].mean():.1f}")
plt.title("Distribution of Marks")
plt.xlabel("Marks")
plt.ylabel("Number of Students")
plt.legend()
plt.tight_layout()
plt.show()
```

**Reading a histogram:**
- **Skewed right** (tail on right) → Most values are low, few are very high
- **Skewed left** (tail on left) → Most values are high, few are very low
- **Bell-shaped** (symmetric) → Normal distribution

---

##  Chart Type 5: Boxplot

**Use when:** Spotting outliers and comparing spread between groups

```python
fig, ax = plt.subplots(figsize=(8, 5))

# Group boxplot by city
city_data = [df[df["city"] == c]["marks"].values for c in df["city"].unique()]
ax.boxplot(city_data, labels=df["city"].unique(), patch_artist=True,
           boxprops=dict(facecolor="lightblue"),
           medianprops=dict(color="red", linewidth=2))
ax.set_title("Marks Distribution by City (Boxplot)")
ax.set_ylabel("Marks")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()
```

**Reading a boxplot:**
- The **box** = IQR (middle 50% of data)
- The **line inside box** = Median
- The **whiskers** = 1.5 × IQR boundary
- **Dots beyond whiskers** = Outliers

---

##  Quick Decision Chart

```
My data has TIME? ──── YES → Line Chart
        │
        NO
        │
Is it PARTS of a WHOLE? ─── YES → Pie Chart (< 6 slices)
        │
        NO
        │
Am I COMPARING CATEGORIES? ─── YES → Bar Chart
        │
        NO
        │
Am I showing a DISTRIBUTION? ─── YES → Histogram
        │
        NO
        │
Am I checking OUTLIERS? ──── YES → Boxplot
        │
        NO
        │
Am I showing RELATIONSHIPS? → Scatter Plot / Heatmap
```

---

## ✅ Key Takeaways

1. **Bar chart** = Compare categories
2. **Line chart** = Show trends over time
3. **Pie chart** = Parts of a whole (use sparingly, max 6 slices)
4. **Histogram** = Distribution of one numerical column
5. **Boxplot** = Spot outliers, compare spread
6. Always ask: **"What story am I trying to tell?"** then pick the chart

---

##  Quick Check Questions

1. You want to show monthly website visitors for 2024. Which chart?
2. You want to show how 5 departments split the company budget. Which chart?
3. You want to compare average salary across 4 job roles. Which chart?
4. Your histogram has a long tail on the right — what does this mean?

---

*Next Topic → [Bar, Line, Pie, Histogram, Boxplot (deep dive)](./02_Bar_Line_Pie_Histogram.md)*
