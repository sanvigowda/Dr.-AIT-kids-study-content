#  Multi-Variable Visualization

> **Learning Goal:** Learn how to visualize relationships between MORE than two variables at once — the most powerful skill in exploratory data analysis.

---

##  Why Multi-Variable Visualization?

With just two variables:
- Study hours vs Marks → Scatter plot ✅

But real questions need more context:
- Study hours vs Marks, **separated by City** → 3 variables!
- Study hours vs Marks vs Attendance → 3+ variables!

> "The goal is to turn data into information, information into insight." — Carly Fiorina

---

##  Key Techniques

### 1. Color (Hue) — Add a 3rd Variable

Use **color** to show a third categorical variable on a 2D scatter plot.

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv("students_data.csv")
df["study_hours"] = df["study_hours"].fillna(df["study_hours"].mean())
df["attendance"]  = df["attendance"].fillna(df["attendance"].mean())
df = df.drop_duplicates()

# 3 variables: study_hours, marks, CITY (color)
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="study_hours", y="marks",
                hue="city",       # ← Adds CITY as color
                palette="Set1",
                s=150, edgecolor="black")

plt.title("Study Hours vs Marks (Colored by City)")
plt.xlabel("Study Hours")
plt.ylabel("Marks")
plt.legend(title="City")
plt.tight_layout()
plt.show()
```

---

### 2. Size — Add a 4th Variable

Use **bubble size** to add a fourth numeric variable.

```python
# 4 variables: study_hours, marks, city (color), attendance (size)
plt.figure(figsize=(9, 5))
scatter = sns.scatterplot(
    data=df,
    x="study_hours",
    y="marks",
    hue="city",           # 3rd variable = color
    size="attendance",    # 4th variable = bubble size
    sizes=(50, 300),      # Min and max bubble size
    palette="Set2",
    edgecolor="black",
    alpha=0.8
)

# Add student name labels
for _, row in df.iterrows():
    plt.annotate(row["name"], (row["study_hours"], row["marks"]),
                 textcoords="offset points", xytext=(5, 3), fontsize=8)

plt.title("Bubble Chart: Study Hrs vs Marks (size=Attendance, color=City)")
plt.legend(bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.show()
```

---

### 3. Facet Grid — Subplots by Category

Split your chart into **multiple panels**, one per category.

```python
# One scatter plot per city
g = sns.FacetGrid(df, col="city", height=4, aspect=0.9)
g.map(sns.scatterplot, "study_hours", "marks", color="steelblue")
g.set_axis_labels("Study Hours", "Marks")
g.set_titles("City: {col_name}")
g.figure.suptitle("Study Hours vs Marks by City", y=1.05)
plt.show()
```

---

### 4. Pair Plot — All Variables at Once

The **pair plot** shows scatter plots for every pair of numerical variables.

```python
# Show all pair-wise relationships in one chart
pair_df = df[["study_hours", "attendance", "marks"]]
g = sns.pairplot(pair_df, diag_kind="kde",
                 plot_kws={"alpha": 0.7, "edgecolor": "black"},
                 diag_kws={"fill": True})
g.figure.suptitle("Pair Plot: All Variable Relationships", y=1.02)
plt.show()
```

**Reading a pair plot:**
- **Diagonal squares** = Distribution of each variable
- **Off-diagonal squares** = Scatter plot of two variables
- Top-right mirrors bottom-left

---

### 5. Color by Category on Any Plot

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Bar by gender and city together
gender_city = df.groupby(["city", "gender"])["marks"].mean().unstack()
gender_city.plot(kind="bar", ax=axes[0], color=["#3498db", "#e91e63"],
                 edgecolor="black", rot=0)
axes[0].set_title("Avg Marks by City × Gender")
axes[0].set_ylabel("Average Marks")
axes[0].set_ylim(0, 100)
axes[0].legend(title="Gender")

# Seaborn bar (easier)
sns.barplot(data=df, x="city", y="marks", hue="gender",
            palette=["#3498db", "#e91e63"], ax=axes[1],
            edgecolor="black", errorbar=None)
axes[1].set_title("Avg Marks by City × Gender (Seaborn)")
axes[1].set_ylim(0, 100)

plt.tight_layout()
plt.show()
```

---

##  Summary: Which Technique for What?

| Extra Variable Type | Technique |
|--------------------|-----------|
| One categorical (3rd var) | **Color / Hue** |
| One numerical (3rd var) | **Bubble size** |
| One categorical (split view) | **Facet Grid** |
| All numerical at once | **Pair Plot** |
| Two categorical | **Grouped Bar** |

---

## ✅ Key Takeaways

1. **Hue (color)** is the easiest way to add a 3rd variable
2. **Bubble charts** encode a 4th dimension using size
3. **FacetGrid** creates one sub-chart per category value
4. **Pair plots** are excellent for understanding all relationships at once
5. Don't add too many dimensions — 4 is usually the max before it gets confusing

---

*Next Topic → [Heatmaps & Distribution Plots](./02_Heatmaps_Distribution_Plots.md)*
