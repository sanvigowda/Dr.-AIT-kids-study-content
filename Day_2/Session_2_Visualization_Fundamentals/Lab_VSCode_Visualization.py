"""
Day 2 | Session 2 Lab: Data Visualization Fundamentals
======================================================
Course: Data Analytics Complete | Day: 2 | Session: 2

Dataset: students_data.csv + synthetic sales data
Install: pip install pandas matplotlib seaborn

Run from project root:
  python3 Day_2/Session_2_Visualization_Fundamentals/Lab_VSCode_Visualization.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 60)
print("  DAY 2 | SESSION 2 LAB: Visualization Fundamentals")
print("=" * 60)

#  Setup 
df = pd.read_csv("students_data.csv")
df["study_hours"] = df["study_hours"].fillna(df["study_hours"].mean())
df["attendance"]  = df["attendance"].fillna(df["attendance"].mean())
df = df.drop_duplicates().reset_index(drop=True)

# Synthetic monthly data for line/trend charts
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
avg_marks_monthly = [70, 68, 72, 74, 76, 78, 75, 80, 82, 79, 83, 85]
study_monthly     = [4.0, 3.8, 4.5, 5.0, 5.2, 5.5,
                     5.0, 6.0, 6.3, 6.0, 6.5, 7.0]

print("\n Data loaded successfully.")


# 
# CHART 1: BAR CHART  Average Marks by City
# 
print("\n[1] Creating Bar Chart: Avg Marks by City...")

avg_city = df.groupby("city")["marks"].mean().sort_values(ascending=False)

plt.figure(figsize=(7, 4))
bars = plt.bar(avg_city.index, avg_city.values,
               color=["#2ecc71", "#3498db", "#e74c3c"], edgecolor="black", width=0.5)

# Value labels on bars
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f"{bar.get_height():.1f}", ha="center", fontsize=11, fontweight="bold")

plt.title("Average Marks by City", fontsize=13, fontweight="bold")
plt.xlabel("City", fontsize=11)
plt.ylabel("Average Marks", fontsize=11)
plt.ylim(0, 100)  #  ETHICAL: always start at 0!
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("Day_2/chart1_bar_city.png", dpi=120, bbox_inches="tight")
plt.show()
print("     Saved: chart1_bar_city.png")


# 
# CHART 2: GROUPED BAR CHART  Marks AND Study Hours by City
# 
print("[2] Creating Grouped Bar Chart...")

city_stats = df.groupby("city")[["marks", "study_hours"]].mean()
x = np.arange(len(city_stats))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 4))
bars1 = ax.bar(x - width/2, city_stats["marks"],        width, label="Marks",       color="#3498db", edgecolor="black")
bars2 = ax.bar(x + width/2, city_stats["study_hours"]*10, width, label="Study Hrs10", color="#e67e22", edgecolor="black")

ax.set_title("Marks vs Study Hours by City (Grouped Bar)", fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(city_stats.index)
ax.set_ylabel("Value")
ax.legend()
ax.set_ylim(0, 110)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("Day_2/chart2_grouped_bar.png", dpi=120, bbox_inches="tight")
plt.show()
print("     Saved: chart2_grouped_bar.png")


# 
# CHART 3: LINE CHART  Monthly Marks Trend
# 
print("[3] Creating Line Chart: Monthly Trend...")

fig, ax1 = plt.subplots(figsize=(10, 4))

ax1.plot(months, avg_marks_monthly, marker="o", color="#3498db",
         linewidth=2.5, markersize=8, label="Avg Marks")
ax1.fill_between(months, avg_marks_monthly, alpha=0.15, color="#3498db")
ax1.set_xlabel("Month")
ax1.set_ylabel("Average Marks", color="#3498db")
ax1.set_ylim(50, 100)

ax2 = ax1.twinx()
ax2.plot(months, study_monthly, marker="s", color="#e74c3c",
         linewidth=2, linestyle="--", markersize=7, label="Study Hours")
ax2.set_ylabel("Study Hours / Day", color="#e74c3c")

ax1.set_title("Monthly Trend: Marks & Study Hours", fontsize=13, fontweight="bold")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
plt.tight_layout()
plt.savefig("Day_2/chart3_line_trend.png", dpi=120, bbox_inches="tight")
plt.show()
print("     Saved: chart3_line_trend.png")


# 
# CHART 4: PIE + DONUT  City and Gender Distribution
# 
print("[4] Creating Pie and Donut Charts...")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

city_counts   = df["city"].value_counts()
gender_counts = df["gender"].value_counts()

# Pie
axes[0].pie(city_counts, labels=city_counts.index, autopct="%1.1f%%",
            colors=["#3498db", "#2ecc71", "#e74c3c"], startangle=90,
            explode=[0.05, 0, 0])
axes[0].set_title("Students by City (Pie)", fontweight="bold")

# Donut
axes[1].pie(gender_counts, labels=gender_counts.index, autopct="%1.1f%%",
            colors=["#3498db", "#e91e63"], startangle=90,
            wedgeprops=dict(width=0.55))
axes[1].set_title("Students by Gender (Donut)", fontweight="bold")

plt.tight_layout()
plt.savefig("Day_2/chart4_pie_donut.png", dpi=120, bbox_inches="tight")
plt.show()
print("     Saved: chart4_pie_donut.png")


# 
# CHART 5: HISTOGRAM  Distribution of Marks
# 
print("[5] Creating Histogram...")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Matplotlib histogram
axes[0].hist(df["marks"], bins=6, color="#3498db", edgecolor="black", alpha=0.8)
axes[0].axvline(df["marks"].mean(),   color="red",   linestyle="--", linewidth=2,
                label=f"Mean = {df['marks'].mean():.1f}")
axes[0].axvline(df["marks"].median(), color="black", linestyle=":",  linewidth=2,
                label=f"Median = {df['marks'].median():.1f}")
axes[0].set_title("Marks Distribution (Matplotlib)", fontweight="bold")
axes[0].set_xlabel("Marks")
axes[0].set_ylabel("Count")
axes[0].legend()

# Seaborn histogram with KDE
sns.histplot(ax=axes[1], data=df, x="marks", bins=6, kde=True, color="#e74c3c")
axes[1].set_title("Marks Distribution with KDE (Seaborn)", fontweight="bold")
axes[1].set_xlabel("Marks")

plt.tight_layout()
plt.savefig("Day_2/chart5_histogram.png", dpi=120, bbox_inches="tight")
plt.show()
print("     Saved: chart5_histogram.png")


# 
# CHART 6: BOXPLOT  Marks by City and Gender
# 
print("[6] Creating Boxplots...")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Seaborn boxplot by city
sns.boxplot(data=df, x="city", y="marks", palette="Set2", ax=axes[0],
            flierprops=dict(marker="o", markerfacecolor="red", markersize=8))
axes[0].set_title("Marks by City (Boxplot)", fontweight="bold")
axes[0].set_ylabel("Marks")
axes[0].set_ylim(0, 110)

# Seaborn violinplot by gender (more info than boxplot!)
sns.violinplot(data=df, x="gender", y="marks", palette=["#3498db", "#e91e63"],
               inner="box", ax=axes[1])
axes[1].set_title("Marks by Gender (Violin Plot)", fontweight="bold")
axes[1].set_ylabel("Marks")

plt.tight_layout()
plt.savefig("Day_2/chart6_boxplot.png", dpi=120, bbox_inches="tight")
plt.show()
print("     Saved: chart6_boxplot.png")


# 
# ETHICS DEMO: Misleading vs Honest Chart
# 
print("[7] Visualization Ethics Demo...")

avg_city_vals = avg_city.values
avg_city_names = avg_city.index

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.bar(avg_city_names, avg_city_vals, color="#e74c3c", edgecolor="black")
ax1.set_ylim(70, 90)
ax1.set_title(" MISLEADING\n(Y starts at 70  looks like huge gap!)", fontweight="bold")
ax1.set_ylabel("Avg Marks")

ax2.bar(avg_city_names, avg_city_vals, color="#2ecc71", edgecolor="black")
for i, v in enumerate(avg_city_vals):
    ax2.text(i, v + 0.5, f"{v:.1f}", ha="center", fontweight="bold")
ax2.set_ylim(0, 100)
ax2.set_title(" HONEST\n(Y starts at 0  actual difference is small)", fontweight="bold")
ax2.set_ylabel("Avg Marks")

plt.suptitle("Visualization Ethics: Why Y-Axis Matters!", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("Day_2/chart7_ethics_demo.png", dpi=120, bbox_inches="tight")
plt.show()
print("     Saved: chart7_ethics_demo.png")


print("\n" + "=" * 60)
print("    Session 2 Lab Complete! All 7 charts created.")
print("=" * 60)
print("""
KEY LESSONS:
  1. Use bar charts for category comparison
  2. Use line charts for time-series trends
  3. Pie/donut charts only for 6 slices (must add to 100%)
  4. Histograms reveal how data is spread
  5. Boxplots expose outliers instantly
  6. ALWAYS start Y-axis at 0 for bar charts!
  7. Seaborn = quick & beautiful, Matplotlib = full control
""")
