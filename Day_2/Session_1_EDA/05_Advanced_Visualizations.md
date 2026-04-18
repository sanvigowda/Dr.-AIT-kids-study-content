#  Advanced Data Visualization

> **Learning Goal:** Learn how to create dense, information-rich visualizations that summarize complex, multi-variable relationships in a single chart.

---

##  The Limits of Basic Charts

A bar chart or a scatter plot is excellent for looking at one or two columns. But what if you have a dataset with 20 columns? 

Plotting 20 separate scatter plots is incredibly tedious and makes it impossible to see the "big picture".

**Advanced visualizations** exist to condense massive amounts of information into a single, digestible view.

---

##  1. The Correlation Heatmap

A correlation heatmap takes a correlation matrix (which is just a grid of numbers between -1 and 1) and color-codes it. This allows your brain to instantly identify strong positive (often dark red/blue) and strong negative relationships without reading a single number.

###  Code Example:
```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("students_data.csv")

# 1. Calculate the correlation matrix
corr_matrix = df[["study_hours", "attendance", "marks"]].corr()

# 2. Plot the heatmap!
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, 
            annot=True,         # Show the actual numbers inside the squares
            cmap="coolwarm",    # Use a red/blue color palette
            vmin=-1, vmax=1,    # Set the scale to correctly match correlation math
            linewidths=0.5)     # Add grid lines between squares

plt.title("Correlation Heatmap: Student Metrics")
plt.show()
```

---

##  2. The Pairplot

If you want to visually check *every* combination of numerical columns simultaneously, the `pairplot` is your best friend.

A Pairplot creates a grid where:
- The **diagonal** reveals the distribution (histogram/KDE) of a single variable.
- The **non-diagonal** spaces show scatterplots of every variable against every other variable.

###  Code Example:
```python
# Pass the dataframe to pairplot, and color points based on the 'city' column
sns.pairplot(df, hue="city", palette="Dark2")
plt.show()
```

> **Warning:** Pairplots are computationally expensive. Running a pairplot on a dataset with 50 columns and 1 million rows will crash your computer. It is best used on fewer than 10 critical columns.

---

##  3. Subplots (Dashboards)

Often, you want to present multiple different charts side-by-side as a "dashboard". Matplotlib's `subplots` let you divide your canvas into a grid and put a different chart in each slot.

###  Code Example:
```python
# Create a 1x3 grid of empty charts
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

# Plot 1: Histogram in the first slot (axes[0])
sns.histplot(df["marks"], ax=axes[0], color="blue")
axes[0].set_title("Distribution of Marks")

# Plot 2: Boxplot in the second slot (axes[1])
sns.boxplot(y=df["marks"], x=df["city"], ax=axes[1])
axes[1].set_title("Marks by City")

# Plot 3: Scatterplot in the third slot (axes[2])
sns.scatterplot(x=df["attendance"], y=df["marks"], ax=axes[2], color="green")
axes[2].set_title("Attendance vs. Marks")

# Ensure charts don't overlap
plt.tight_layout()
plt.show()
```

---

##  Saving Your Masterpieces

Once you've built the perfect chart, you need to save it so you can drop it into a presentation or send it to your team in an email.

Do this *before* calling `plt.show()`!

```python
plt.savefig("my_amazing_dashboard.png", dpi=300, bbox_inches="tight")
```
- `dpi=300`: Ensures the image is high-resolution (good for presentations/printing).
- `bbox_inches="tight"`: Ensures that titles and axis labels don't get accidentally cut off from the saved image.

---

##  Real-World Example: Fraud Detection

> A bank is trying to map out credit card fraud. They have a dataset with 30 columns reflecting user behaviour (login times, transaction amounts, location changes).
> 
> A Data Analyst generates a **Correlation Heatmap**. 
> Instantly, a bright red square emerges between `transaction_distance_from_home` and `is_fraud`. They focus their analysis on this relationship instead of individually checking the other 29 columns.

---

##  Key Takeaways

1. Use a **Heatmap** to visualize a correlation matrix instantly.
2. Use a **Pairplot** to generate scatterplots for every combination of numerical columns.
3. Use **Subplots** (`plt.subplots`) to combine multiple charts into a single cohesive dashboard layout.
4. Save your figures using **`plt.savefig()`** as a high-resolution `.png` file.

---

##  Quick Check Questions

1. Why shouldn't you run a `pairplot` on a dataset with 100 columns?
2. In a Seaborn heatmap, what does `annot=True` do?
3. What is the parameter in `plt.savefig()` that makes the image high resolution?

---

 **Congratulations! You've completed the Day 2 Data Analytics Curriculum.** You now know how to generate raw statistics, map correlations, hunt outliers, and visualize data beautifully!
