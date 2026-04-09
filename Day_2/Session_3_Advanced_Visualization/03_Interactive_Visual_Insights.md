# 💡 Interactive Visual Insights

> **Learning Goal:** Go beyond static charts — learn how to add interactivity and create "talking" visualizations that guide the viewer to the insight.

---

## 🤔 What Makes a Visualization "Insightful"?

A chart becomes insightful when the **viewer knows exactly what to do** after seeing it.

| Chart Type | Insight Level |
|-----------|--------------|
| "Here is the data" | ❌ Low |
| "Here is the data + labels" | ✓ Medium |
| "Here is the data + the conclusion drawn" | ✅ High |

---

## 🏷️ Technique 1: Annotate the Key Insight

Add **text annotations** directly on the chart to highlight what matters.

```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("students_data.csv")
df["study_hours"] = df["study_hours"].fillna(df["study_hours"].mean())
df["attendance"]  = df["attendance"].fillna(df["attendance"].mean())
df = df.drop_duplicates()

fig, ax = plt.subplots(figsize=(9, 5))

colors = df["city"].map({"Chennai":"#3498db","Bangalore":"#2ecc71","Hyderabad":"#e74c3c"})
ax.scatter(df["study_hours"], df["marks"], c=colors, s=150, edgecolors="black", zorder=3)

# Name labels for every point
for _, row in df.iterrows():
    ax.annotate(row["name"], (row["study_hours"], row["marks"]),
                textcoords="offset points", xytext=(6, 3), fontsize=8)

# ← The annotation that tells the story
ax.annotate("Vikram: 8 hrs, 98% attend.\n→ Top scorer (95)",
            xy=(8, 95), xytext=(6.2, 88),
            arrowprops=dict(arrowstyle="->", color="black"),
            fontsize=9, color="darkgreen",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", edgecolor="gray"))

ax.annotate("Divya: only 3 hrs\n→ Lowest scorer (60)",
            xy=(3, 60), xytext=(4.2, 63),
            arrowprops=dict(arrowstyle="->", color="black"),
            fontsize=9, color="darkred",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffe0e0", edgecolor="gray"))

# Trend line
import numpy as np
m, b = np.polyfit(df["study_hours"], df["marks"], 1)
x_line = np.linspace(df["study_hours"].min(), df["study_hours"].max(), 100)
ax.plot(x_line, m*x_line + b, "k--", linewidth=1.5, alpha=0.5, label="Trend line")

ax.set_title("Study Hours vs Marks — Insights Annotated", fontsize=13, fontweight="bold")
ax.set_xlabel("Study Hours / Day")
ax.set_ylabel("Marks")
ax.legend()
plt.tight_layout()
plt.show()
```

---

## 🎨 Technique 2: Color to Highlight, Not Decorate

Use color **purposefully** to draw attention.

```python
avg_city = df.groupby("city")["marks"].mean().sort_values(ascending=False)

# Highlight the winner in a different color
bar_colors = ["gold" if c == avg_city.idxmax() else "steelblue"
              for c in avg_city.index]

plt.figure(figsize=(7, 4))
bars = plt.bar(avg_city.index, avg_city.values, color=bar_colors, edgecolor="black")
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f"{bar.get_height():.1f}", ha="center", fontweight="bold")

plt.annotate("🏆 Top City!", xy=(0, avg_city.max()),
             xytext=(0.2, avg_city.max() - 5), fontsize=11, color="goldenrod")

plt.title("Best Performing City Highlighted")
plt.ylim(0, 100)
plt.ylabel("Avg Marks")
plt.tight_layout()
plt.show()
```

---

## 📊 Technique 3: Dashboard Layout with Text Summary

Combine charts + text boxes to create a **story-driven dashboard**.

```python
fig = plt.figure(figsize=(14, 6))
fig.suptitle("Student Performance Dashboard — Key Insights",
             fontsize=15, fontweight="bold")

# Left: Scatter
ax1 = fig.add_subplot(1, 3, 1)
ax1.scatter(df["study_hours"], df["marks"],
            c=df["city"].map({"Chennai":"#3498db","Bangalore":"#2ecc71","Hyderabad":"#e74c3c"}),
            s=120, edgecolors="black")
ax1.set_title("Study Hours vs Marks")
ax1.set_xlabel("Study Hours")
ax1.set_ylabel("Marks")

# Middle: Bar by city
ax2 = fig.add_subplot(1, 3, 2)
avg_city.plot(kind="bar", ax=ax2, color=["gold","steelblue","coral"],
              edgecolor="black", rot=0)
ax2.set_title("Avg Marks by City")
ax2.set_ylim(0, 100)
ax2.set_ylabel("Marks")

# Right: Text insight box
ax3 = fig.add_subplot(1, 3, 3)
ax3.axis("off")   # Turn off axes for text panel
insights = (
    "📌 KEY INSIGHTS\n"
    "─────────────────────────\n"
    f"• Avg Marks:    {df['marks'].mean():.1f}\n"
    f"• Top Student:  Vikram (95)\n"
    f"• Best City:    Bangalore ({avg_city.max():.1f})\n"
    f"• Study ↔ Marks: r = {df['study_hours'].corr(df['marks']):.2f}\n\n"
    "📋 ACTIONS:\n"
    "─────────────────────────\n"
    "• Set min 6 hrs study goal\n"
    "• Alert students < 80% attend"
)
ax3.text(0.05, 0.95, insights, transform=ax3.transAxes,
         verticalalignment="top", fontsize=10,
         bbox=dict(facecolor="#f8f9fa", edgecolor="#dee2e6",
                   boxstyle="round,pad=0.8", linewidth=1.5),
         family="monospace")

plt.tight_layout()
plt.show()
```

---

## 🌐 Technique 4: Simple Plotly Interactive Chart

For truly interactive charts (hover tooltips, zoom, pan), use **Plotly**.

```python
# pip install plotly
import plotly.express as px

fig = px.scatter(
    df,
    x="study_hours",
    y="marks",
    color="city",
    size="attendance",        # Bubble size = attendance
    hover_name="name",        # Hover shows student name
    hover_data=["attendance", "gender"],
    title="Interactive: Hover over each student!",
    labels={"study_hours": "Study Hours", "marks": "Marks"}
)
fig.update_traces(marker=dict(line=dict(width=1, color="black")))
fig.show()  # Opens in browser!
```

> 💡 Plotly charts are **interactive in web browsers** and Jupyter notebooks — great for presentations!

---

## ✅ Key Takeaways

1. **Annotate your charts** — tell the viewer what the insight is, don't make them guess
2. Use **color purposefully** to highlight the main finding
3. A **dashboard = multiple charts + insight text** working together
4. **Plotly** makes interactive charts with hover, zoom, filter
5. The best visualization is one that makes the **action obvious**

---

*Next: Session 3 Lab → [Lab_VSCode_Mini_Dashboard.py](./Lab_VSCode_Mini_Dashboard.py)*
