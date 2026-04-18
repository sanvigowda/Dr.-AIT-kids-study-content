"""
Day 2 | Session 3 Lab: Mini Dashboard — Advanced Visualization
==============================================================
Course: Data Analytics Complete | Day: 2 | Session: 3

This is the CAPSTONE lab for Day 2.
You will build a complete, professional-quality analytics dashboard
covering: multi-variable charts, heatmaps, distribution plots,
annotations, and insight panels.

Dataset: students_data.csv
Install: pip install pandas numpy matplotlib seaborn

Run from project root:
  python3 Day_2/Session_3_Advanced_Visualization/Lab_VSCode_Mini_Dashboard.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

print("=" * 65)
print("  DAY 2 | SESSION 3 LAB: Advanced Visualization Mini Dashboard")
print("=" * 65)

# ─────────────────────────────────────────────────────────────
# DATA PREPARATION
# ─────────────────────────────────────────────────────────────

df = pd.read_csv("students_data.csv")
df["study_hours"] = df["study_hours"].fillna(df["study_hours"].mean())
df["attendance"]  = df["attendance"].fillna(df["attendance"].mean())
df = df.drop_duplicates().reset_index(drop=True)

# Derived columns
df["grade"] = pd.cut(df["marks"],
                     bins=[0, 60, 70, 80, 90, 100],
                     labels=["F", "C", "B", "A", "A+"])
df["performance_label"] = df["marks"].apply(
    lambda x: "High" if x >= 80 else ("Mid" if x >= 70 else "Low"))

# Pre-compute stats
avg_marks     = df["marks"].mean()
avg_attend    = df["attendance"].mean()
avg_study     = df["study_hours"].mean()
top_student   = df.loc[df["marks"].idxmax(), "name"]
low_student   = df.loc[df["marks"].idxmin(), "name"]
best_city     = df.groupby("city")["marks"].mean().idxmax()
corr_sh_marks = df["study_hours"].corr(df["marks"])
corr_at_marks = df["attendance"].corr(df["marks"])

print(f"\n✅ Dataset ready  →  {df.shape[0]} students | {df.shape[1]} columns")
print(f"\nQuick Stats:")
print(f"  Avg Marks     : {avg_marks:.1f}")
print(f"  Avg Attendance: {avg_attend:.1f}%")
print(f"  Avg Study Hrs : {avg_study:.1f} hrs/day")
print(f"  Top Student   : {top_student}")
print(f"  Best City     : {best_city}")
print(f"  Corr (study↔marks): {corr_sh_marks:.2f}")
print(f"  Corr (attend↔marks): {corr_at_marks:.2f}")


# ─────────────────────────────────────────────────────────────
# PART 1: MULTI-VARIABLE SCATTER — Study Hours vs Marks
#          (Color = City, Size = Attendance)
# ─────────────────────────────────────────────────────────────
print("\n[1] Multi-variable Scatter Plot...")

fig1, ax = plt.subplots(figsize=(10, 6))

city_colors = {"Chennai": "#3498db", "Bangalore": "#2ecc71", "Hyderabad": "#e74c3c"}
for city, group in df.groupby("city"):
    ax.scatter(group["study_hours"], group["marks"],
               c=city_colors[city], s=group["attendance"] * 3,
               label=city, edgecolors="black", linewidth=0.8, alpha=0.9)

# Trend line
m, b = np.polyfit(df["study_hours"], df["marks"], 1)
x_line = np.linspace(df["study_hours"].min(), df["study_hours"].max(), 100)
ax.plot(x_line, m * x_line + b, "k--", linewidth=1.5, alpha=0.5, label="Trend line")

# Name labels
for _, row in df.iterrows():
    ax.annotate(row["name"], (row["study_hours"], row["marks"]),
                textcoords="offset points", xytext=(5, 3), fontsize=8)

# Highlight top & bottom students
top = df.loc[df["marks"].idxmax()]
low = df.loc[df["marks"].idxmin()]
ax.annotate(f"⭐ {top['name']} (Top scorer: {top['marks']})",
            xy=(top["study_hours"], top["marks"]),
            xytext=(top["study_hours"] - 2.5, top["marks"] - 6),
            arrowprops=dict(arrowstyle="->", color="darkgreen"),
            fontsize=9, color="darkgreen",
            bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow", ec="gray"))
ax.annotate(f" {low['name']} (Needs help: {low['marks']})",
            xy=(low["study_hours"], low["marks"]),
            xytext=(low["study_hours"] + 0.5, low["marks"] + 8),
            arrowprops=dict(arrowstyle="->", color="darkred"),
            fontsize=9, color="darkred",
            bbox=dict(boxstyle="round,pad=0.3", fc="#ffe0e0", ec="gray"))

ax.set_title("Study Hours vs Marks\n(Color = City | Bubble size = Attendance %)",
             fontsize=12, fontweight="bold")
ax.set_xlabel("Study Hours / Day", fontsize=11)
ax.set_ylabel("Marks", fontsize=11)
ax.legend(title="City")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("Day_2/part1_multivariable_scatter.png", dpi=130, bbox_inches="tight")
plt.show()
print("   ✅ Saved: Day_2/part1_multivariable_scatter.png")


# ─────────────────────────────────────────────────────────────
# PART 2: HEATMAP — Correlation Matrix (styled)
# ─────────────────────────────────────────────────────────────
print("[2] Correlation Heatmap...")

corr_data = df[["study_hours", "attendance", "marks", "age"]].corr()

fig2, ax = plt.subplots(figsize=(7, 5))
sns.heatmap(corr_data, annot=True, fmt=".2f", cmap="coolwarm",
            vmin=-1, vmax=1, linewidths=1, linecolor="white",
            square=True, annot_kws={"size": 13, "weight": "bold"},
            ax=ax)
ax.set_title("Correlation Heatmap\n(Darker red = stronger positive link)",
             fontsize=12, fontweight="bold")
ax.set_xticklabels(["Study Hrs", "Attendance", "Marks", "Age"], rotation=15)
ax.set_yticklabels(["Study Hrs", "Attendance", "Marks", "Age"], rotation=0)
plt.tight_layout()
plt.savefig("Day_2/part2_heatmap.png", dpi=130, bbox_inches="tight")
plt.show()
print("   ✅ Saved: Day_2/part2_heatmap.png")


# ─────────────────────────────────────────────────────────────
# PART 3: DISTRIBUTION PLOTS — KDE + Violin + Strip
# ─────────────────────────────────────────────────────────────
print("[3] Distribution Plots...")

fig3, axes = plt.subplots(1, 3, figsize=(15, 5))
fig3.suptitle("Distribution Analysis — Marks", fontsize=13, fontweight="bold")

# KDE by city
for city in df["city"].unique():
    subset = df[df["city"] == city]["marks"]
    axes[0].fill_between(np.linspace(subset.min()-5, subset.max()+5, 100),
                         0, 0, alpha=0)  # dummy for spacing
    sns.kdeplot(subset, ax=axes[0], label=city, fill=True, alpha=0.4, linewidth=2)
axes[0].set_title("KDE: Marks Distribution by City")
axes[0].set_xlabel("Marks")
axes[0].legend()

# Violin by city
sns.violinplot(data=df, x="city", y="marks", palette="Set2",
               inner="box", ax=axes[1])
axes[1].set_title("Violin: Marks Shape by City")
axes[1].set_ylabel("Marks")

# Swarm by gender — shows every student
sns.swarmplot(data=df, x="gender", y="marks",
              palette=["#3498db", "#e91e63"],
              size=12, edgecolor="black", linewidth=1, ax=axes[2])
axes[2].set_title("Swarm: Every Student Shown by Gender")
axes[2].set_ylabel("Marks")

plt.tight_layout()
plt.savefig("Day_2/part3_distributions.png", dpi=130, bbox_inches="tight")
plt.show()
print("   ✅ Saved: Day_2/part3_distributions.png")


# ─────────────────────────────────────────────────────────────
# PART 4: THE FULL MINI DASHBOARD (6-panel)
# ─────────────────────────────────────────────────────────────
print("[4] Building the Full Mini Dashboard...")

fig4 = plt.figure(figsize=(18, 11))
fig4.suptitle(" Student Performance Analytics Dashboard — Day 2 Capstone",
              fontsize=16, fontweight="bold", y=1.01)

gs = gridspec.GridSpec(2, 4, figure=fig4, hspace=0.45, wspace=0.4)

avg_city   = df.groupby("city")["marks"].mean().sort_values(ascending=False)
avg_gender = df.groupby("gender")["marks"].mean()

# ── Panel 1: Bar — City Comparison ──────────────────────────
ax1 = fig4.add_subplot(gs[0, 0])
bar_colors = ["gold" if c == best_city else "steelblue" for c in avg_city.index]
bars = ax1.bar(avg_city.index, avg_city.values, color=bar_colors, edgecolor="black", width=0.5)
for bar in bars:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f"{bar.get_height():.1f}", ha="center", fontsize=9, fontweight="bold")
ax1.set_title("Avg Marks by City\n( Gold = Best)", fontweight="bold", fontsize=9)
ax1.set_ylim(0, 100)
ax1.set_ylabel("Marks")

# ── Panel 2: Violin — Gender ─────────────────────────────────
ax2 = fig4.add_subplot(gs[0, 1])
sns.violinplot(data=df, x="gender", y="marks",
               palette=["#3498db", "#e91e63"], inner="quartile", ax=ax2)
ax2.set_title("Marks by Gender\n(Violin)", fontweight="bold", fontsize=9)
ax2.set_ylabel("Marks")

# ── Panel 3: Heatmap ─────────────────────────────────────────
ax3 = fig4.add_subplot(gs[0, 2])
mini_corr = df[["study_hours","attendance","marks"]].corr()
sns.heatmap(mini_corr, annot=True, fmt=".2f", cmap="coolwarm",
            vmin=-1, vmax=1, square=True,
            annot_kws={"size": 10, "weight": "bold"},
            linewidths=1, linecolor="white", ax=ax3)
ax3.set_xticklabels(["Study", "Attend.", "Marks"], fontsize=8, rotation=15)
ax3.set_yticklabels(["Study", "Attend.", "Marks"], fontsize=8, rotation=0)
ax3.set_title("Correlation Heatmap", fontweight="bold", fontsize=9)

# ── Panel 4: KPI Text Box ─────────────────────────────────────
ax4 = fig4.add_subplot(gs[0, 3])
ax4.axis("off")
kpi_text = (
    " KPIs\n"
    "─────────────────────\n"
    f"  Avg Marks:   {avg_marks:.1f}\n"
    f"  Avg Attend:  {avg_attend:.1f}%\n"
    f"  Avg Study:   {avg_study:.1f} hrs\n\n"
    " RANKINGS\n"
    "─────────────────────\n"
    f"  Top:  {top_student} (95)\n"
    f"  Low:  {low_student} (60)\n"
    f"  City: {best_city} \n\n"
    " CORRELATIONS\n"
    "─────────────────────\n"
    f"  Study↔Marks:  {corr_sh_marks:.2f}\n"
    f"  Attend↔Marks: {corr_at_marks:.2f}"
)
ax4.text(0.05, 0.97, kpi_text, transform=ax4.transAxes,
         va="top", fontsize=9, family="monospace",
         bbox=dict(facecolor="#f8f9fa", edgecolor="#adb5bd",
                   boxstyle="round,pad=0.6", linewidth=1.5))
ax4.set_title("Key Metrics", fontweight="bold", fontsize=9)

# ── Panel 5: Scatter — Study Hours vs Marks ──────────────────
ax5 = fig4.add_subplot(gs[1, 0:2])
for city, group in df.groupby("city"):
    ax5.scatter(group["study_hours"], group["marks"],
                c=city_colors[city], s=100, label=city,
                edgecolors="black", linewidth=0.7)
ax5.plot(x_line, m * x_line + b, "k--", linewidth=1.5, alpha=0.5, label="Trend")
for _, row in df.iterrows():
    ax5.annotate(row["name"], (row["study_hours"], row["marks"]),
                 textcoords="offset points", xytext=(4, 2), fontsize=7)
ax5.set_title("Study Hours vs Marks (Color = City)", fontweight="bold", fontsize=9)
ax5.set_xlabel("Study Hours")
ax5.set_ylabel("Marks")
ax5.legend(fontsize=8)
ax5.grid(alpha=0.25)

# ── Panel 6: Grade Distribution ──────────────────────────────
ax6 = fig4.add_subplot(gs[1, 2])
grade_counts = df["grade"].value_counts().sort_index()
grade_colors = ["#e74c3c","#e67e22","#f1c40f","#2ecc71","#27ae60"]
ax6.bar(grade_counts.index.astype(str), grade_counts.values,
        color=grade_colors[:len(grade_counts)], edgecolor="black")
for i, (g, v) in enumerate(zip(grade_counts.index, grade_counts.values)):
    ax6.text(i, v + 0.05, str(v), ha="center", fontweight="bold", fontsize=10)
ax6.set_title("Grade Distribution", fontweight="bold", fontsize=9)
ax6.set_ylabel("Number of Students")
ax6.set_xlabel("Grade")

# ── Panel 7: Action Summary ──────────────────────────────────
ax7 = fig4.add_subplot(gs[1, 3])
ax7.axis("off")
actions = (
    " INSIGHTS\n"
    "─────────────────────\n"
    "1. More study hours =\n"
    "   higher marks (r=0.96)\n\n"
    "2. Attendance matters:\n"
    "   90%+ → score 80+\n\n"
    "3. Bangalore leads\n"
    "   (avg 86.7 marks)\n\n"
    " ACTIONS\n"
    "─────────────────────\n"
    "▸ Set 6-hr study goal\n"
    "▸ Alert <80% attendance\n"
    "▸ Mentor Divya & Sneha"
)
ax7.text(0.05, 0.97, actions, transform=ax7.transAxes,
         va="top", fontsize=9, family="monospace",
         bbox=dict(facecolor="#fff3cd", edgecolor="#ffc107",
                   boxstyle="round,pad=0.6", linewidth=1.5))
ax7.set_title("Insights & Actions", fontweight="bold", fontsize=9)

plt.savefig("Day_2/session3_mini_dashboard.png", dpi=140, bbox_inches="tight")
plt.show()
print("   ✅ Dashboard saved: Day_2/session3_mini_dashboard.png")


# ─────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("  ✅  Session 3 Lab Complete! Day 2 Capstone Done.")
print("=" * 65)
print("""
CHARTS CREATED:
  Part 1: Multi-variable bubble scatter (bubble=attendance, color=city)
  Part 2: Styled correlation heatmap with coolwarm palette
  Part 3: KDE + Violin + Swarm distribution analysis
  Part 4: 6-panel full analytics dashboard with KPIs + actions

ADVANCED TECHNIQUES APPLIED:
  ✔ Color encoding for 3rd variable
  ✔ Size encoding for 4th variable
  ✔ Arrow annotations pointing to key findings
  ✔ Trend line (linear regression) on scatter
  ✔  KPI text panel alongside charts
  ✔ Highlight the "winner" in gold
  ✔ gridspec for precise dashboard layout
""")
