#  Handling Missing Values

> **Learning Goal:** Understand why missing values occur, how to detect them, and the right strategies to handle them — without distorting your analysis.

---

##  Why Do Missing Values Exist?

Missing values are one of the most common data quality problems. They arise from:

| Cause | Real-World Example | Type |
|-------|-------------------|------|
| **Not collected** | A survey respondent skipped a question | MCAR |
| **System error** | Server crashed during data write | MCAR |
| **Conditional** | Income field blank for unemployed respondents | MAR |
| **Intentional** | Patients who recovered don't have "death date" | MNAR |

### Three Types of Missing Data
- **MCAR** (Missing Completely at Random) — Randomness, no pattern
- **MAR** (Missing at Random) — Missingness depends on other columns
- **MNAR** (Missing Not at Random) — Data is missing *because of* its actual value

---

##  Step 1: Detect Missing Values

```python
import pandas as pd
import numpy as np

# Create a sample dataset with missing values
data = {
    'customer_id': [101, 102, 103, 104, 105, 106, 107, 108],
    'name': ['Priya', 'Rahul', None, 'Aisha', 'Karan', 'Meera', 'Dev', 'Sana'],
    'age': [25, np.nan, 30, 22, np.nan, 28, 35, np.nan],
    'salary': [45000, 60000, np.nan, 35000, 70000, np.nan, 55000, 40000],
    'city': ['Mumbai', 'Delhi', 'Chennai', None, 'Pune', 'Bangalore', None, 'Hyderabad'],
    'purchase_amount': [1200, np.nan, 850, 2100, 500, np.nan, 1800, 950]
}

df = pd.DataFrame(data)
print("Original DataFrame:")
print(df)

# ─── Method 1: Check for any missing values ────────────────────────────────
print("\nAny missing values?", df.isnull().values.any())  # True

# ─── Method 2: Count missing per column ──────────────────────────────────
print("\nMissing values per column:")
print(df.isnull().sum())

# ─── Method 3: Percentage missing per column ─────────────────────────────
print("\nMissing percentage per column:")
print((df.isnull().sum() / len(df) * 100).round(2))

# ─── Method 4: Visualize missing pattern ─────────────────────────────────
# (Run in Jupyter for the visual)
# import missingno as msno
# msno.matrix(df)
```

### Output Interpretation
```
customer_id       0  → 0.0%
name              1  → 12.5%
age               3  → 37.5%   ← High missing rate — needs attention
salary            2  → 25.0%
city              2  → 25.0%
purchase_amount   2  → 25.0%
```

---

##  Option 1: Drop Missing Values

### When to Drop?
✅ When very few rows have missing data (< 5% of total)  
✅ When the missing column is not important for the analysis  
❌ Don't drop when missing data is informative or you'll lose too many rows

```python
# Drop rows where ANY column has a missing value
df_dropped = df.dropna()
print(f"Original: {len(df)} rows → After drop: {len(df_dropped)} rows")

# Drop rows where SPECIFIC columns have missing values
df_dropped_specific = df.dropna(subset=['salary', 'purchase_amount'])
print(f"After dropping rows with missing salary/purchase: {len(df_dropped_specific)}")

# Drop columns with more than 50% missing values
threshold = len(df) * 0.5
df_dropped_cols = df.dropna(axis=1, thresh=threshold)
print(f"Columns kept after threshold: {df_dropped_cols.columns.tolist()}")

# Drop rows only if ALL values in that row are missing
df_all_missing = df.dropna(how='all')
```

---

## ✏️ Option 2: Imputation (Filling Missing Values)

### 2a. Fill with a Constant

```python
# Fill missing city with 'Unknown'
df['city'] = df['city'].fillna('Unknown')

# Fill missing name with a placeholder
df['name'] = df['name'].fillna('Not Provided')

print(df[['name', 'city']])
```

### 2b. Statistical Imputation — Mean, Median, Mode

```python
# Fill numerical columns with mean (good for normally distributed data)
df['salary'] = df['salary'].fillna(df['salary'].mean())

# Fill numerical columns with median (better when outliers exist)
df['age'] = df['age'].fillna(df['age'].median())

# Fill numerical columns with mode (most frequent value)
df['purchase_amount'] = df['purchase_amount'].fillna(df['purchase_amount'].mode()[0])

print("\nAfter basic imputation:")
print(df.isnull().sum())
```

**Real-Life Example:**
> An e-commerce company has missing "age" for some users. Instead of dropping those customers, they fill age with the **median age** of all customers (e.g., 29). This keeps all purchase data while making a reasonable assumption.

### 2c. Group-Based (Smart) Imputation

```python
import pandas as pd
import numpy as np

# Sales dataset where salary varies by city
df = pd.DataFrame({
    'city': ['Mumbai', 'Mumbai', 'Delhi', 'Delhi', 'Mumbai', 'Delhi'],
    'salary': [80000, np.nan, 55000, np.nan, 75000, 60000]
})

# Smart approach: Fill missing salary with the median salary FOR THAT CITY
df['salary'] = df.groupby('city')['salary'].transform(
    lambda x: x.fillna(x.median())
)
print(df)
# Mumbai employees get Mumbai's median salary
# Delhi employees get Delhi's median salary
# Much more accurate than global median!
```

### 2d. Forward Fill & Backward Fill (Time Series)

```python
import pandas as pd
import numpy as np

# Stock price data with missing values on weekends/holidays
stock_data = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=7),
    'price': [450.0, 455.0, np.nan, np.nan, 460.0, np.nan, 475.0]
})

# Forward fill — carry last known value forward
stock_data['price_ffill'] = stock_data['price'].fillna(method='ffill')

# Backward fill — use next known value to fill backward  
stock_data['price_bfill'] = stock_data['price'].fillna(method='bfill')

# Interpolate — estimate values between known points (best for continuous data)
stock_data['price_interpolated'] = stock_data['price'].interpolate(method='linear')

print(stock_data)
```

**Real-Life Example:**
> A weather station occasionally goes offline. For temperature readings, **linear interpolation** is used to estimate the missing hours, because temperature changes gradually.

### 2e. ML-Based Imputation (Advanced)

```python
from sklearn.impute import KNNImputer
import pandas as pd
import numpy as np

# KNN Imputer: uses K-nearest neighbor records to estimate missing values
df = pd.DataFrame({
    'age': [25, np.nan, 30, 22, np.nan, 28],
    'salary': [45000, 60000, np.nan, 35000, 70000, np.nan],
    'experience': [2, 5, 7, 1, 8, 4]
})

imputer = KNNImputer(n_neighbors=2)
df_imputed = pd.DataFrame(
    imputer.fit_transform(df),
    columns=df.columns
)
print("KNN Imputed DataFrame:")
print(df_imputed.round(2))
```

---

##  Decision Framework: Which Strategy to Use?

```
Is the column important for analysis?
├── No → DROP the column entirely
└── Yes → How much data is missing?
    ├── < 5% → DROP those rows safely
    ├── 5-30% → IMPUTE with mean/median/mode
    │   ├── Numerical + no outliers → Mean
    │   ├── Numerical + outliers exist → Median
    │   ├── Categorical → Mode or 'Unknown'
    │   └── Time series → Forward/Backward fill or Interpolation
    └── > 30% → Consider the business context
        ├── Is missing value itself meaningful? → Create a "is_missing" flag column
        └── Else → Use advanced ML imputation or collect more data
```

---

##  Creating Missing Indicator Columns

Sometimes the fact that something is missing IS important information!

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'phone_number': ['+91-9999', np.nan, '+91-8888', np.nan, '+91-7777'],
    'purchase': [500, 1200, np.nan, 800, np.nan]
})

# Create indicator: 1 if phone number was provided, else 0
df['has_phone'] = df['phone_number'].notna().astype(int)

# Create indicator: 1 if purchase is missing
df['purchase_missing'] = df['purchase'].isna().astype(int)

# Now fill the missing values normally
df['purchase'] = df['purchase'].fillna(df['purchase'].median())

print(df)
# Insight: Customers without phone numbers → different purchase behavior?
```

---

## ✅ Key Takeaways

1. Always **detect and quantify** missing values before any analysis
2. **Never drop** blindly — understand *why* data is missing first
3. Use **median** for skewed numerical data, **mean** for normally distributed
4. For time series, **forward fill** or **interpolation** works best
5. Sometimes missing data IS the signal — create **indicator columns**
6. Document every imputation decision for reproducibility

---

##  Quick Check Questions

1. When would you use `median` instead of `mean` for imputation?
2. What is forward fill and when is it appropriate?
3. A customer survey has 40% missing "income" values. What should you do?
4. What does MCAR stand for?

---

*Previous: [Data Sources](./01_Data_Sources_CSV_API_Databases.md) | Next: [Removing Duplicates & Transformation](./03_Duplicates_Transformation.md)*
