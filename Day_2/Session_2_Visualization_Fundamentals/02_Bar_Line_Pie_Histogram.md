# 📊 Bar, Line, Pie, Histogram & Boxplot — Deep Dive

> **Learning Goal:** Master the 5 most commonly used charts in data analysis using Matplotlib and Seaborn.

---

## 🛠️ Setup

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Apply a clean style
plt.style.use("seaborn-v0_8-whitegrid")  # Clean white background

df = pd.read_csv("students_data.csv")
```

---

## 1️⃣ Bar Chart — "Which group is bigger?"

**Matplotlib:**
```python
avg = df.groupby("city")["marks"].mean()

plt.figure(figsize=(7, 4))
bars = plt.bar(avg.index, avg.values, color=["#3498db","#e74c3c","#2ecc71"], edgecolor="black")

# Add value labels on top of each bar
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f"{bar.get_height():.1f}", ha="center", fontsize=10, fontweight="bold")

plt.title("Average Marks by City", fontsize=13, fontweight="bold")
plt.xlabel("City")
plt.ylabel("Average Marks")
plt.ylim(0, 100)
plt.tight_layout()
plt.show()
```

**Seaborn (even easier!):**
```python
plt.figure(figsize=(7, 4))
sns.barplot(data=df, x="city", y="marks", palette="Set2",
            estimator="mean", errorbar=None)
plt.title("Average Marks by City (Seaborn)")
plt.tight_layout()
plt.show()
```

> 💡 **Seaborn Tip:** `palette="Set2"` gives beautiful pre-made color combinations. Try `"pastel"`, `"coolwarm"`, `"Blues"`.

**Horizontal bar chart** (great when labels are long):
```python
avg_sorted = df.groupby("city")["marks"].mean().sort_values()
plt.barh(avg_sorted.index, avg_sorted.values, color="steelblue")
plt.title("Average Marks by City (Horizontal)")
plt.show()
```

---

## 2️⃣ Line Chart — "How does this change over time?"

```python
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
study_hours = [4.0, 4.2, 3.8, 5.0, 5.5, 6.0,
               5.8, 6.2, 7.0, 7.5, 8.0, 8.5]
attendance  = [78, 80, 75, 82, 85, 88, 86, 89, 92, 90, 95, 93]

fig, ax1 = plt.subplots(figsize=(10, 4))

# Primary axis — study hours
ax1.plot(months, study_hours, marker="o", color="steelblue",
         linewidth=2, label="Study Hours", markersize=7)
ax1.set_xlabel("Month")
ax1.set_ylabel("Study Hours", color="steelblue")
ax1.fill_between(months, study_hours, alpha=0.1, color="steelblue")

# Secondary axis — attendance
ax2 = ax1.twinx()
ax2.plot(months, attendance, marker="s", color="coral",
         linewidth=2, linestyle="--", label="Attendance %", markersize=7)
ax2.set_ylabel("Attendance (%)", color="coral")

plt.title("Study Hours and Attendance Trends")
fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
plt.tight_layout()
plt.show()
```

---

## 3️⃣ Pie Chart — "What portion of the whole?"

```python
city_counts = df["city"].value_counts()

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Standard Pie
axes[0].pie(city_counts, labels=city_counts.index, autopct="%1.1f%%",
            colors=["#3498db", "#e74c3c", "#2ecc71"], startangle=90,
            explode=[0.05, 0, 0])  # Highlight first slice
axes[0].set_title("Students by City (Pie)")

# Donut Chart (more modern look)
wedges, texts, autotexts = axes[1].pie(
    city_counts, labels=city_counts.index, autopct="%1.1f%%",
    colors=["#3498db", "#e74c3c", "#2ecc71"], startangle=90,
    wedgeprops=dict(width=0.5))  # width<1 → donut!
axes[1].set_title("Students by City (Donut)")

plt.tight_layout()
plt.show()
```

> ⚠️ **Rule:** Use pie/donut only when you have **≤ 6 slices** and the percentages are **meaningfully different**.

---

## 4️⃣ Histogram — "How is this value distributed?"

```python
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

for ax, col, color in zip(axes, ["marks", "study_hours", "attendance"],
                           ["steelblue", "coral", "seagreen"]):
    ax.hist(df[col], bins=5, color=color, edgecolor="black", alpha=0.8)
    ax.axvline(df[col].mean(),   color="red",    linestyle="--", linewidth=2, label="Mean")
    ax.axvline(df[col].median(), color="black",  linestyle=":",  linewidth=2, label="Median")
    ax.set_title(f"Distribution: {col}")
    ax.set_xlabel(col)
    ax.set_ylabel("Frequency")
    ax.legend(fontsize=8)

plt.suptitle("Histograms — How values are spread out", fontweight="bold")
plt.tight_layout()
plt.show()
```

**Seaborn version with KDE (Kernel Density Estimate):**
```python
plt.figure(figsize=(7, 4))
sns.histplot(df["marks"], bins=6, kde=True, color="steelblue")
# kde=True adds a smooth curve showing the distribution shape
plt.title("Marks Distribution with KDE Curve")
plt.show()
```

---

## 5️⃣ Boxplot — "Where are the outliers?"

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Basic boxplot
axes[0].boxplot([df[df["city"]==c]["marks"].values for c in df["city"].unique()],
                labels=df["city"].unique(), patch_artist=True,
                boxprops=dict(facecolor="lightblue"),
                medianprops=dict(color="red", linewidth=2),
                flierprops=dict(marker="o", markerfacecolor="red", markersize=8))
axes[0].set_title("Marks by City (Boxplot)")
axes[0].set_ylabel("Marks")

# Seaborn version (much easier!)
sns.boxplot(data=df, x="city", y="marks", palette="Set2", ax=axes[1])
axes[1].set_title("Marks by City (Seaborn Boxplot)")

plt.tight_layout()
plt.show()
```

---

## 🎨 Matplotlib vs Seaborn — When to Use Which?

| Factor | Matplotlib | Seaborn |
|--------|-----------|---------|
| Control | Full control | Less control |
| Code length | Longer | Shorter |
| Look | Basic by default | Beautiful by default |
| Best for | Custom complex charts | Quick beautiful charts |
| Statistical charts | Manual | Built-in (violin, pairplot...) |

> 💡 **Best practice:** Use **Seaborn for quick exploration**, **Matplotlib for final polish**.

---

## ✅ Key Takeaways

1. **Bar** = Compare groups | **Line** = Show trends over time
2. **Pie** = Part of whole (max 6 slices) | **Histogram** = Distribution shape
3. **Boxplot** = Spot outliers | Both Matplotlib and Seaborn are valuable
4. Always label your axes and add a title!
5. Add value labels on bar charts for clarity

---

*Next Topic → [Visualization Ethics](./03_Visualization_Ethics.md)*
