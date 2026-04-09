# 🔥 Heatmaps & Distribution Plots

> **Learning Goal:** Master heatmaps for correlation data and learn 4 types of distribution plots to deeply understand how your data is shaped.

---

## 🔥 Heatmaps

A **heatmap** uses color intensity to show values in a matrix (table). Perfect for correlation matrices.

### Basic Correlation Heatmap

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("students_data.csv")
df["study_hours"] = df["study_hours"].fillna(df["study_hours"].mean())
df["attendance"]  = df["attendance"].fillna(df["attendance"].mean())
df = df.drop_duplicates()

corr = df[["study_hours", "attendance", "marks", "age"]].corr()

plt.figure(figsize=(7, 5))
sns.heatmap(
    corr,
    annot=True,        # Show numbers inside cells
    fmt=".2f",         # 2 decimal places
    cmap="coolwarm",   # Color: red=positive, blue=negative
    vmin=-1, vmax=1,   # Always fix to -1 to +1
    linewidths=0.5,    # Grid lines between cells
    square=True        # Make cells square
)
plt.title("Correlation Heatmap — Student Data", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.show()
```

### Heatmap Color Map Options

| `cmap` | Best For |
|--------|----------|
| `"coolwarm"` | Correlation (red=positive, blue=negative) |
| `"Blues"` | Values where 0 is minimum |
| `"RdYlGn"` | Red=bad, Yellow=neutral, Green=good |
| `"YlOrRd"` | Density / frequency maps |
| `"viridis"` | General purpose, colorblind-friendly |

### Annotated Styled Heatmap

```python
plt.figure(figsize=(6, 5))
mask = corr > 0  # Mask positive values to highlight negatives

sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn",
            center=0, linewidths=1, linecolor="white",
            annot_kws={"size": 12, "weight": "bold"})

plt.title("Styled Correlation Heatmap")
plt.tight_layout()
plt.show()
```

---

## 📊 Distribution Plots

Distribution plots show **how values are spread** across a range.

### 1. Histogram (covered in Session 2)

```python
sns.histplot(df["marks"], bins=6, kde=True, color="steelblue")
plt.title("Marks Distribution")
plt.show()
```

---

### 2. KDE Plot (Kernel Density Estimate)

Like a smooth histogram — shows the **shape of distribution**.

```python
plt.figure(figsize=(8, 4))

# One KDE per city
for city in df["city"].unique():
    subset = df[df["city"] == city]["marks"]
    sns.kdeplot(subset, label=city, fill=True, alpha=0.3, linewidth=2)

plt.title("Marks Distribution by City (KDE)")
plt.xlabel("Marks")
plt.ylabel("Density")
plt.legend(title="City")
plt.tight_layout()
plt.show()
```

> 💡 KDE is great for **comparing distributions** across groups side-by-side.

---

### 3. Violin Plot (Boxplot + KDE combined)

Shows the full distribution AND statistics in one chart.

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Violin plot by city
sns.violinplot(data=df, x="city", y="marks", palette="Set2",
               inner="box", ax=axes[0])
axes[0].set_title("Violin Plot: Marks by City", fontweight="bold")
axes[0].set_ylabel("Marks")

# Violin plot by gender
sns.violinplot(data=df, x="gender", y="marks",
               palette=["#3498db", "#e91e63"],
               inner="quartile",  # Shows Q1, median, Q3 inside
               ax=axes[1])
axes[1].set_title("Violin Plot: Marks by Gender", fontweight="bold")
axes[1].set_ylabel("Marks")

plt.tight_layout()
plt.show()
```

**Reading a violin plot:**
```
Wide shape = Many students have this mark value
Narrow shape = Few students have this mark value
Inner box = IQR (like a boxplot)
Inner line = Median
```

---

### 4. Strip Plot + Swarm Plot (Show actual data points)

When you have small datasets, show **every individual data point**.

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Strip plot (points may overlap)
sns.stripplot(data=df, x="city", y="marks", palette="Set1",
              size=10, jitter=True, edgecolor="black", linewidth=1,
              ax=axes[0])
axes[0].set_title("Strip Plot: Every Student Shown", fontweight="bold")

# Swarm plot (no overlap — auto-adjusts)
sns.swarmplot(data=df, x="city", y="marks", palette="Set2",
              size=10, edgecolor="black", linewidth=1,
              ax=axes[1])
axes[1].set_title("Swarm Plot: No Overlapping Points", fontweight="bold")

plt.tight_layout()
plt.show()
```

> 💡 For small datasets (< 50 rows), **always show the actual data points** — it's more honest than just showing averages!

---

## 📊 Choosing the Right Distribution Plot

| Plot | Dataset Size | Shows |
|------|-------------|-------|
| Histogram | Any | Frequency bins |
| KDE | Medium-Large | Smooth shape |
| Boxplot | Any | Stats + outliers |
| Violin | Medium+ | Full shape + stats |
| Strip/Swarm | Small (<100) | Every data point |

---

## 🔥 Combined: Violin + Strip (Best of Both)

```python
plt.figure(figsize=(8, 5))
sns.violinplot(data=df, x="city", y="marks", palette="Pastel1", inner=None)
sns.stripplot(data=df, x="city", y="marks", color="black", size=8,
              jitter=False, zorder=2)  # Overlay actual points
plt.title("Violin + Data Points: Best of Both Worlds", fontweight="bold")
plt.tight_layout()
plt.show()
```

---

## ✅ Key Takeaways

1. **Heatmaps** are perfect for correlation matrices — always use `vmin=-1, vmax=1`
2. **KDE** shows a smooth distribution curve — great for comparing groups
3. **Violin plots** = boxplot + distribution shape in one chart
4. **Strip/Swarm** = best for small datasets where every point matters
5. For **small datasets like ours (10 students)**, always show the raw data points!

---

*Next Topic → [Interactive Visual Insights](./03_Interactive_Visual_Insights.md)*
