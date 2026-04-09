
# =============================================================
#   MINI PROJECT: STUDENT PERFORMANCE ANALYSIS
#   Data Analyst | A complete walkthrough
# =============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ─────────────────────────────────────────────────────────────
# SECTION 1: DATA UNDERSTANDING
# ─────────────────────────────────────────────────────────────

print("=" * 55)
print("  SECTION 1: DATA UNDERSTANDING")
print("=" * 55)

# 1. Load the dataset
df = pd.read_csv("students_data.csv")

# 2. First 5 rows
print("\n[1] First 5 rows:")
print(df.head())

# 3. Shape (rows x columns)
print(f"\n[2] Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")

# 4. Column names
print(f"\n[3] Column Names: {list(df.columns)}")

# 5. Identify Numerical and Categorical columns
numerical_cols   = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
print(f"\n[4] Numerical Columns  : {numerical_cols}")
print(f"    Categorical Columns: {categorical_cols}")

# 6. Data types
print("\n[5] Data Types:")
print(df.dtypes)

# 7. Summary statistics
print("\n[6] Summary Statistics:")
print(df.describe())


# ─────────────────────────────────────────────────────────────
# SECTION 2: DATA CLEANING
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("  SECTION 2: DATA CLEANING")
print("=" * 55)

# 8. Check for missing values
print("\n[7] Missing Values per Column:")
print(df.isnull().sum())

# 9. Which columns have missing values?
missing_cols = df.columns[df.isnull().any()].tolist()
print(f"\n[8] Columns with Missing Values: {missing_cols}")

# 10. Handle Missing Values
#   - study_hours  → fill with MEAN  (numerical, small impact)
#   - attendance   → fill with MEAN  (numerical, small impact)
#   Reason: With only ~10 rows, dropping rows would lose too much data.
#           Using the mean keeps the distribution intact.
df["study_hours"] = df["study_hours"].fillna(df["study_hours"].mean())
df["attendance"]  = df["attendance"].fillna(df["attendance"].mean())
print("\n[9] Missing values filled with column MEAN.")
print("    Reason: Dataset is small; dropping rows would lose data.")

# 11. Check for duplicate rows
print(f"\n[10] Duplicate Rows Found: {df.duplicated().sum()}")

# 12. Remove duplicates
df = df.drop_duplicates()
print("     Duplicate rows removed.")

# 13. Verify dataset is clean
print(f"\n[11] After Cleaning → Shape: {df.shape}")
print(f"     Missing Values  : {df.isnull().sum().sum()}")
print(f"     Duplicates      : {df.duplicated().sum()}")
print("\n ✅  Dataset is CLEAN and ready for analysis!\n")

"""
─── Reflection ────────────────────────────────────────────────
WHY IS DATA CLEANING IMPORTANT?

• Dirty data (missing values, duplicates, wrong types) leads
  to WRONG analysis and WRONG decisions.
• Cleaning ensures results are ACCURATE and TRUSTWORTHY.
• "Garbage in → Garbage out" is the #1 rule in data analytics.
───────────────────────────────────────────────────────────────
"""


# ─────────────────────────────────────────────────────────────
# SECTION 3: DATA EXPLORATION (EDA)
# ─────────────────────────────────────────────────────────────

print("=" * 55)
print("  SECTION 3: DATA EXPLORATION (EDA)")
print("=" * 55)

# 14. Average marks
avg_marks = df["marks"].mean()
print(f"\n[12] Average Marks     : {avg_marks:.2f}")

# 15. Min and Max marks
print(f"[13] Minimum Marks     : {df['marks'].min()}")
print(f"     Maximum Marks     : {df['marks'].max()}")

# 16. Average attendance
print(f"[14] Average Attendance: {df['attendance'].mean():.2f}%")

# 17. Student with highest marks
top_student = df.loc[df["marks"].idxmax(), ["name", "marks"]]
print(f"\n[15] Highest Marks → {top_student['name']} ({top_student['marks']})")

# 18. Student with lowest marks
low_student = df.loc[df["marks"].idxmin(), ["name", "marks"]]
print(f"[16] Lowest Marks  → {low_student['name']} ({low_student['marks']})")


# ─────────────────────────────────────────────────────────────
# SECTION 4: ANALYSIS & AGGREGATION
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("  SECTION 4: ANALYSIS & AGGREGATION")
print("=" * 55)

# 19. Average marks by city
avg_marks_city = df.groupby("city")["marks"].mean().sort_values(ascending=False).round(2)
print("\n[17] Average Marks by City:")
print(avg_marks_city)

# 20. Average marks by gender
avg_marks_gender = df.groupby("gender")["marks"].mean().round(2)
print("\n[18] Average Marks by Gender:")
print(avg_marks_gender)

# 21. Average study hours by city
avg_study_city = df.groupby("city")["study_hours"].mean().round(2)
print("\n[19] Average Study Hours by City:")
print(avg_study_city)

# 22. Highest performing city
best_city = avg_marks_city.idxmax()
print(f"\n[20] Highest Performing City: {best_city} ({avg_marks_city[best_city]:.2f} avg marks)")

# 23. Male vs Female performance
print("\n[21] Male vs Female Performance:")
print(df.groupby("gender")[["marks", "study_hours", "attendance"]].mean().round(2))

"""
─── Thinking Question ─────────────────────────────────────────
STUDY HOURS vs ATTENDANCE — Which matters more?

Looking at the data:
• Vikram (8 hrs study, 98% attendance) → 95 marks  ← BEST
• Divya  (3 hrs study, 70% attendance) → 60 marks  ← WORST

Both seem important, but ATTENDANCE tends to correlate
more consistently because regular presence = regular learning.
Study hours alone without attending class is less effective.
───────────────────────────────────────────────────────────────
"""


# ─────────────────────────────────────────────────────────────
# SECTION 5: VISUALIZATION
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("  SECTION 5: VISUALIZATION")
print("=" * 55)

fig, axes = plt.subplots(2, 2, figsize=(12, 9))
fig.suptitle("Student Performance Analysis", fontsize=16, fontweight="bold")

# 24. Bar chart – Average Marks by City
avg_marks_city.plot(kind="bar", ax=axes[0, 0], color=["steelblue", "coral", "seagreen"],
                    edgecolor="black")
axes[0, 0].set_title("Average Marks by City")
axes[0, 0].set_xlabel("City")
axes[0, 0].set_ylabel("Average Marks")
axes[0, 0].tick_params(axis="x", rotation=0)
for bar in axes[0, 0].patches:
    axes[0, 0].text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.5,
                    f"{bar.get_height():.1f}", ha="center", fontsize=9)

# 25. Bar chart – Average Marks by Gender``
avg_marks_gender.plot(kind="bar", ax=axes[0, 1], color=["dodgerblue", "hotpink"],
                      edgecolor="black", width=0.4)
axes[0, 1].set_title("Average Marks by Gender")
axes[0, 1].set_xlabel("Gender")
axes[0, 1].set_ylabel("Average Marks")
axes[0, 1].tick_params(axis="x", rotation=0)
for bar in axes[0, 1].patches:
    axes[0, 1].text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.5,
                    f"{bar.get_height():.1f}", ha="center", fontsize=9)

# 26. Scatter plot – Study Hours vs Marks
axes[1, 0].scatter(df["study_hours"], df["marks"], color="darkorange",
                   edgecolors="black", s=100)
axes[1, 0].set_title("Study Hours vs Marks")
axes[1, 0].set_xlabel("Study Hours")
axes[1, 0].set_ylabel("Marks")
for _, row in df.iterrows():
    axes[1, 0].annotate(row["name"],
                        (row["study_hours"], row["marks"]),
                        textcoords="offset points", xytext=(5, 3), fontsize=7)

# 27. Scatter plot – Attendance vs Marks (Optional)
axes[1, 1].scatter(df["attendance"], df["marks"], color="mediumseagreen",
                   edgecolors="black", s=100)
axes[1, 1].set_title("Attendance vs Marks")
axes[1, 1].set_xlabel("Attendance (%)")
axes[1, 1].set_ylabel("Marks")
for _, row in df.iterrows():
    axes[1, 1].annotate(row["name"],
                        (row["attendance"], row["marks"]),
                        textcoords="offset points", xytext=(5, 3), fontsize=7)

plt.tight_layout()
plt.savefig("student_analysis_charts.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n[22] Charts saved as 'student_analysis_charts.png'")

"""
─── Observation ───────────────────────────────────────────────
PATTERNS FROM THE GRAPHS:
1. Bangalore students score the highest on average.
2. Study hours and marks show a clear UPWARD trend —
   more study → higher marks.
3. Attendance and marks also rise together — students
   with 90%+ attendance consistently score 80+.
4. Students below 75% attendance tend to score below 70.
───────────────────────────────────────────────────────────────
"""


# ─────────────────────────────────────────────────────────────
# SECTION 6: CORRELATION ANALYSIS
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("  SECTION 6: CORRELATION ANALYSIS")
print("=" * 55)

# 28. Correlation matrix
corr = df[["study_hours", "attendance", "marks", "age"]].corr().round(2)
print("\n[23] Correlation Matrix:")
print(corr)

# 29. Strongest correlations with marks
print("\n[24] Correlation with MARKS:")
print(corr["marks"].drop("marks").sort_values(ascending=False))

# 30. Specific relationships
sh_marks  = df["study_hours"].corr(df["marks"]).round(2)
att_marks = df["attendance"].corr(df["marks"]).round(2)
print(f"\n[25] Study Hours  ↔ Marks : {sh_marks}  (Strong Positive)")
print(f"     Attendance  ↔ Marks : {att_marks}  (Strong Positive)")

"""
─── Important ─────────────────────────────────────────────────
DOES CORRELATION MEAN CAUSATION?

NO. Correlation only tells us two variables MOVE TOGETHER.
It does NOT prove one CAUSES the other.

Example:
  Ice cream sales and drowning incidents are correlated
  (both rise in summer). But ice cream doesn't cause drowning!
  The hidden cause is HOT WEATHER.

In our data → more study hours correlate with higher marks.
This MAKES SENSE logically, but we still need experiments
(controlled studies) to truly prove causation.
───────────────────────────────────────────────────────────────
"""


# ─────────────────────────────────────────────────────────────
# SECTION 7: INSIGHTS & CONCLUSION
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("  SECTION 7: INSIGHTS & CONCLUSION")
print("=" * 55)

print("""
KEY INSIGHTS:
─────────────────────────────────────────────────────
1. Study Hours matter the most.
   Students who study 6+ hours/day consistently score 85+.
   Students with <4 hours score below 70.

2. Attendance is strongly linked to marks.
   All students with 90%+ attendance scored above 80.
   Vikram (8 hrs, 98% attendance) → scored highest (95).

3. Bangalore students outperform other cities.
   Bangalore avg = highest, possibly due to more study hours.

SUGGESTED ACTIONS:
─────────────────────────────────────────────────────
1. Encourage low-performing students (Divya, Sneha) to
   increase study hours from 3–4 hrs to at least 6 hrs/day.

2. Implement an attendance alert system — notify students
   when their attendance drops below 80% so they can
   take corrective action before exams.
─────────────────────────────────────────────────────
""")


# ─────────────────────────────────────────────────────────────
# SECTION 8: PRESENTATION (Simple Summary)
# ─────────────────────────────────────────────────────────────

print("=" * 55)
print("  SECTION 8: PRESENTATION SUMMARY")
print("=" * 55)
print("""
WHAT DID WE LEARN?
  • Students who study more and attend regularly score better.
  • Bangalore is the top performing city in this dataset.
  • Female and Male students performed almost equally on average.

WHAT SURPRISED US?
  • Even with just 10 students, the data told a CLEAR story!
  • Attendance had a very strong correlation with marks —
    just showing up to class makes a huge difference.

BONUS — WHO WILL SCORE HIGHEST NEXT TIME?
  • Based on current trends: Vikram (8 hrs study, 98% attendance)
    is predicted to maintain top performance.
  • Improvement candidates: Divya and Sneha — if they increase
    study hours, they have the highest potential to improve.
""")

print("=" * 55)
print("  ✅  Analysis Complete!")
print("=" * 55)
