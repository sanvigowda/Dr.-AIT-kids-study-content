"""
Day 2 | Session 1 Lab: Exploratory Data Analysis (EDA)
======================================================
Course: Data Analytics Complete | Day: 2 | Session: 1

Dataset: students_data.csv (from Day 1 mini project)
Install: pip install pandas numpy matplotlib seaborn scipy

Run this file from the project root folder:
  python3 Day_2/Session_1_EDA/Lab_VSCode_EDA.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 60)
print("  DAY 2 | SESSION 1 LAB: Exploratory Data Analysis")
print("=" * 60)

# 
# STEP 0: Load and prepare data
# 

df = pd.read_csv("students_data.csv")

# Quick clean (from Day 1)
df["study_hours"] = df["study_hours"].fillna(df["study_hours"].mean())
df["attendance"]  = df["attendance"].fillna(df["attendance"].mean())
df = df.drop_duplicates().reset_index(drop=True)

print(f"\n Dataset loaded: {df.shape[0]} students, {df.shape[1]} columns")
print(df.to_string(index=False))


# 
# SECTION 1: STATISTICAL SUMMARIES
# 

print("\n" + "=" * 60)
print("  SECTION 1: STATISTICAL SUMMARIES")
print("=" * 60)

# 1a. Full summary statistics
print("\n[1] Summary Statistics (describe):")
print(df[["study_hours", "attendance", "marks"]].describe().round(2))

# 1b. Individual stats for marks
marks = df["marks"]
print(f"\n[2] Marks  Detailed Stats:")
print(f"    Mean    : {marks.mean():.2f}")
print(f"    Median  : {marks.median():.2f}")
print(f"    Std Dev : {marks.std():.2f}")
print(f"    Variance: {marks.var():.2f}")
print(f"    Range   : {marks.max() - marks.min()}")

Q1 = marks.quantile(0.25)
Q3 = marks.quantile(0.75)
IQR = Q3 - Q1
print(f"    Q1      : {Q1}")
print(f"    Q3      : {Q3}")
print(f"    IQR     : {IQR}")

# 1c. Frequency distribution
print("\n[3] Marks  Grade Distribution:")
grade_bins = pd.cut(df["marks"], bins=[0, 60, 70, 80, 90, 100],
                    labels=["F (<60)", "C (60-70)", "B (70-80)", "A (80-90)", "A+ (90+)"])
print(grade_bins.value_counts().sort_index())

# 1d. Categorical summary
print("\n[4] City Distribution:")
print(df["city"].value_counts())
print("\n[5] Gender Distribution:")
print(df["gender"].value_counts())


# 
# SECTION 2: CORRELATION ANALYSIS
# 

print("\n" + "=" * 60)
print("  SECTION 2: CORRELATION ANALYSIS")
print("=" * 60)

# 2a. Pairwise correlations
print("\n[6] Pairwise Correlations with Marks:")
num_cols = ["study_hours", "attendance", "marks"]
corr_matrix = df[num_cols].corr()
print(corr_matrix.round(2))

# Highlight strongest correlations
print("\n[7] What the correlations tell us:")
sh_r  = df["study_hours"].corr(df["marks"])
att_r = df["attendance"].corr(df["marks"])
age_r = df["age"].corr(df["marks"])
print(f"    study_hours  marks : r = {sh_r:.2f}   {'Strong ' if abs(sh_r) > 0.7 else 'Moderate'} positive")
print(f"    attendance   marks : r = {att_r:.2f}   {'Strong ' if abs(att_r) > 0.7 else 'Moderate'} positive")
age_label = "Weak (age doesn't matter here)" if abs(age_r) < 0.3 else "Moderate"
print(f"    age          marks : r = {age_r:.2f}   {age_label}")


# 
# SECTION 3: OUTLIER DETECTION
# 

print("\n" + "=" * 60)
print("  SECTION 3: OUTLIER DETECTION")
print("=" * 60)

# 3a. IQR Method
print("\n[8] Outlier Detection  IQR Method:")
for col in ["marks", "study_hours", "attendance"]:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    print(f"    {col:15s}  fence: [{lower:.1f}, {upper:.1f}]  | Outliers: {len(outliers)}")

# 3b. Z-Score Method (using numpy  no scipy needed)
print("\n[9] Outlier Detection  Z-Score Method (|z| > 2):")
for col in ["marks", "study_hours"]:
    col_data = df[col]
    z_scores = np.abs((col_data - col_data.mean()) / col_data.std())
    outlier_mask = z_scores > 2
    if outlier_mask.any():
        print(f"    {col}: {df[outlier_mask]['name'].tolist()} are potential outliers")
    else:
        print(f"    {col}: No outliers found (|z| > 2)")


# 
# SECTION 4: FEATURE ANALYSIS
# 

print("\n" + "=" * 60)
print("  SECTION 4: FEATURE ANALYSIS")
print("=" * 60)

print("\n[10] Performance by City:")
city_stats = df.groupby("city")[["marks", "study_hours", "attendance"]].agg(["mean", "min", "max"]).round(1)
print(city_stats)

print("\n[11] Performance by Gender:")
gender_stats = df.groupby("gender")[["marks", "study_hours", "attendance"]].mean().round(2)
print(gender_stats)

print("\n[12] Top 3 Students:")
print(df.nlargest(3, "marks")[["name", "city", "study_hours", "attendance", "marks"]].to_string(index=False))

print("\n[13] Students Needing Attention (marks < 70):")
print(df[df["marks"] < 70][["name", "city", "study_hours", "attendance", "marks"]].to_string(index=False))


# 
# SECTION 5: VISUALIZATIONS  EDA Dashboard
# 

print("\n" + "=" * 60)
print("  SECTION 5: EDA VISUALIZATIONS")
print("=" * 60)

fig, axes = plt.subplots(2, 3, figsize=(15, 9))
fig.suptitle("Day 2 | Session 1 Lab: EDA Dashboard  Student Performance",
             fontsize=14, fontweight="bold", y=1.01)

# Plot 1: Distribution of Marks (Histogram)
axes[0, 0].hist(df["marks"], bins=6, color="steelblue", edgecolor="black", alpha=0.8)
axes[0, 0].axvline(df["marks"].mean(),   color="red",    linestyle="--", label=f"Mean={df['marks'].mean():.1f}")
axes[0, 0].axvline(df["marks"].median(), color="orange", linestyle="--", label=f"Median={df['marks'].median():.1f}")
axes[0, 0].set_title("Distribution of Marks")
axes[0, 0].set_xlabel("Marks")
axes[0, 0].set_ylabel("Count")
axes[0, 0].legend(fontsize=8)

# Plot 2: Boxplot  All Numerical Columns
data_to_plot = [df["marks"], df["study_hours"] * 10, df["attendance"]]
bp = axes[0, 1].boxplot(data_to_plot, patch_artist=True,
                         labels=["Marks", "Study Hrs10", "Attendance"],
                         boxprops=dict(facecolor="lightblue"),
                         medianprops=dict(color="red", linewidth=2))
axes[0, 1].set_title("Boxplots (Outlier Detection)")
axes[0, 1].set_ylabel("Value")
axes[0, 1].grid(axis="y", alpha=0.3)

# Plot 3: Correlation Heatmap
corr = df[["study_hours", "attendance", "marks"]].corr()
im = axes[0, 2].imshow(corr, cmap="coolwarm", vmin=-1, vmax=1, aspect="auto")
axes[0, 2].set_xticks(range(3))
axes[0, 2].set_yticks(range(3))
axes[0, 2].set_xticklabels(["Study Hrs", "Attend.", "Marks"], fontsize=8)
axes[0, 2].set_yticklabels(["Study Hrs", "Attend.", "Marks"], fontsize=8)
for i in range(3):
    for j in range(3):
        axes[0, 2].text(j, i, f"{corr.iloc[i, j]:.2f}",
                        ha="center", va="center", fontsize=11, fontweight="bold")
axes[0, 2].set_title("Correlation Heatmap")
plt.colorbar(im, ax=axes[0, 2], shrink=0.8)

# Plot 4: Scatter  Study Hours vs Marks
colors = {"Chennai": "steelblue", "Bangalore": "coral", "Hyderabad": "seagreen"}
for city, group in df.groupby("city"):
    axes[1, 0].scatter(group["study_hours"], group["marks"],
                       label=city, color=colors[city], s=100, edgecolors="black")
axes[1, 0].set_title(f"Study Hours vs Marks  (r={sh_r:.2f})")
axes[1, 0].set_xlabel("Study Hours")
axes[1, 0].set_ylabel("Marks")
axes[1, 0].legend(fontsize=8)
# Add names
for _, row in df.iterrows():
    axes[1, 0].annotate(row["name"], (row["study_hours"], row["marks"]),
                        textcoords="offset points", xytext=(4, 3), fontsize=7)

# Plot 5: Scatter  Attendance vs Marks
for city, group in df.groupby("city"):
    axes[1, 1].scatter(group["attendance"], group["marks"],
                       label=city, color=colors[city], s=100, edgecolors="black")
axes[1, 1].set_title(f"Attendance vs Marks  (r={att_r:.2f})")
axes[1, 1].set_xlabel("Attendance (%)")
axes[1, 1].set_ylabel("Marks")
axes[1, 1].legend(fontsize=8)

# Plot 6: Grade Distribution Pie Chart
grade_counts = grade_bins.value_counts().sort_index()
colors_pie = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#27ae60"]
axes[1, 2].pie(grade_counts, labels=grade_counts.index, autopct="%1.0f%%",
               colors=colors_pie, startangle=90)
axes[1, 2].set_title("Grade Distribution")

plt.tight_layout()
plt.savefig("Day_2/session_1_eda_dashboard.png", dpi=130, bbox_inches="tight")
plt.show()
print("\n EDA Dashboard saved as 'Day_2/session_1_eda_dashboard.png'")

print("\n" + "=" * 60)
print("    Session 1 Lab Complete!")
print("=" * 60)
print("""
KEY TAKEAWAYS FROM THIS LAB:
   describe() gives a complete statistical snapshot in one call
   Correlation matrix shows all relationships at once
   IQR fence method is the industry standard for outlier detection
   Visual exploration (boxplots, heatmaps) reveals patterns instantly
""")
