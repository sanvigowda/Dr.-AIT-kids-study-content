#  Correlation Analysis

> **Learning Goal:** Understand how to find and measure relationships between variables  one of the most powerful tools in a data analyst's toolkit.

---

##  What Is Correlation?

**Correlation** measures how strongly two variables are related and in **which direction**.

### Real-Life Examples:

| Variable A | Variable B | Relationship |
|------------|------------|-------------|
| Study hours | Exam marks |  A   B (Positive) |
| Junk food eaten | Health score |  A   B (Negative) |
| Shoe size | IQ | No relationship (None) |

---

##  The Correlation Coefficient (r)

The **correlation coefficient** is a number between **-1 and +1** that quantifies the relationship.

```

-1.0    -0.7    -0.3    0    +0.3    +0.7    +1.0
                                         
Strong  Moderate Weak  None  Weak  Moderate Strong
Neg.     Neg.   Neg.        Pos.    Pos.    Pos.

```

| r value | Interpretation |
|---------|---------------|
| **+1.0** | Perfect positive  one goes up, other goes up exactly |
| **+0.7 to +1.0** | Strong positive correlation |
| **+0.3 to +0.7** | Moderate positive correlation |
| **0 to +0.3** | Weak positive correlation |
| **0** | No correlation |
| **-0.3 to 0** | Weak negative correlation |
| **-0.7 to -0.3** | Moderate negative correlation |
| **-1.0 to -0.7** | Strong negative correlation |

---

##  Calculating Correlation with Pandas

```python
import pandas as pd

df = pd.read_csv("students_data.csv")

# Correlation between two columns
r = df["study_hours"].corr(df["marks"])
print(f"Study Hours  Marks: {r:.2f}")
# Output: Study Hours  Marks: 0.96   Very strong!

# Full correlation matrix (all numerical columns at once)
corr_matrix = df[["study_hours", "attendance", "marks", "age"]].corr()
print(corr_matrix)
```

**Output:**

```
              study_hours  attendance  marks    age
study_hours      1.00        0.91     0.96   -0.12
attendance       0.91        1.00     0.94   -0.08
marks            0.96        0.94     1.00   -0.10
age             -0.12       -0.08    -0.10    1.00
```

**Reading the matrix:**
- **marks  study_hours = 0.96**  Very strong positive (more study = higher marks)
- **marks  attendance = 0.94**  Very strong positive (attend more = higher marks)
- **marks  age = -0.10**  Almost no relationship (age doesn't affect marks here)

---

##  Visualizing Correlation with a Heatmap

```python
import seaborn as sns
import matplotlib.pyplot as plt

corr_matrix = df[["study_hours", "attendance", "marks"]].corr()

plt.figure(figsize=(6, 4))
sns.heatmap(corr_matrix,
            annot=True,        # Show numbers
            cmap="coolwarm",   # Red = positive, Blue = negative
            fmt=".2f",         # 2 decimal places
            vmin=-1, vmax=1)   # Always fix scale to -1 to 1
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()
```

>  **Color guide for coolwarm:**
> -  Dark red = Strong positive (+1.0)
> -  White = No correlation (0)
> -  Dark blue = Strong negative (-1.0)

---

##  Visualizing with a Scatter Plot Matrix

```python
pd.plotting.scatter_matrix(
    df[["study_hours", "attendance", "marks"]],
    figsize=(8, 6),
    alpha=0.7,
    diagonal="hist"
)
plt.suptitle("Scatter Matrix  Find Relationships Visually")
plt.tight_layout()
plt.show()
```

---

##  IMPORTANT: Correlation  Causation

This is the **most important rule** in data analysis!

> **Just because two things move together doesn't mean one causes the other.**

### Famous Examples:

| Correlation | Real Cause |
|-------------|-----------|
| Ice cream sales  when drowning incidents  | Both caused by **HOT WEATHER** |
| Countries with more TVs have higher life expectancy | Both caused by **WEALTH** |
| Nicolas Cage movies  correlates with pool drownings | Pure **COINCIDENCE** |

### In Our Student Data:
- Study hours and marks are strongly correlated 
- This **makes logical sense**, but we'd still need a **controlled study** to prove causation
- Maybe students who study more also sleep better, eat better, etc. (hidden variables)

>  **The third variable problem:** There's often a hidden "confounding variable" that causes both!

---

##  Real-World Use Cases

| Industry | Correlation Used For |
|----------|---------------------|
| **Retail** | Do promotions drive sales? (promotion  revenue) |
| **Healthcare** | Does smoking cause cancer? (smoking  cancer rate) |
| **Finance** | Do two stocks move together? (portfolio risk) |
| **Education** | Does attendance affect grades? (our example!) |

---

##  Key Takeaways

1. Correlation measures **strength** and **direction** of relationship
2. Ranges from **-1 to +1**  closer to 1 = stronger
3. Use `.corr()` in pandas and `sns.heatmap()` to visualize
4. **NEVER say "causes"** just because two things correlate
5. Always ask: "Is there a **third hidden variable**?"

---

##  Quick Check Questions

1. If `r = -0.85`, what does this mean?
2. In your student dataset, which two variables are most correlated?
3. Someone says "Countries that eat more chocolate win more Nobel prizes." Is this causation?
4. What's the correlation of any variable with itself?

---

*Next Topic  [Outlier Detection](./03_Outlier_Detection.md)*
