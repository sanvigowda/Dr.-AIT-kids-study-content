#  Removing Duplicates & Data Transformation

> **Learning Goal:** Learn to find and remove duplicate data, and apply transformations to shape data for analysis.

---

## Part 1: Removing Duplicates

### Why Do Duplicates Occur?

| Cause | Example |
|-------|---------|
| Data entry errors | Same order submitted twice |
| System merges | Two databases merged with overlapping records |
| API polling | Same record fetched multiple times |
| Manual data | Staff entered same customer twice |

**Real-Life Damage:** A hospital billed a patient twice for the same procedure because of duplicate records  1.2 lakh extra charge that caused a lawsuit.

---

###  Detecting Duplicates

```python
import pandas as pd

# E-commerce orders dataset with duplicates
orders = pd.DataFrame({
    'order_id':    [101, 102, 103, 101, 104, 103, 105],
    'customer':    ['Priya', 'Rahul', 'Aisha', 'Priya', 'Karan', 'Aisha', 'Meera'],
    'product':     ['Laptop', 'Phone', 'Tablet', 'Laptop', 'Watch', 'Tablet', 'Camera'],
    'amount':      [45000, 25000, 35000, 45000, 12000, 35000, 28000],
    'date':        ['2024-01-10', '2024-01-11', '2024-01-12',
                    '2024-01-10', '2024-01-13', '2024-01-12', '2024-01-14']
})

print("Total rows:", len(orders))  # 7

# Check for completely duplicate rows (all columns match)
print("\nFully duplicate rows:")
print(orders.duplicated().sum())

# Check for duplicates based on specific columns
print("\nDuplicate order IDs:")
print(orders.duplicated(subset=['order_id']).sum())  # 2 duplicates

# Show which rows ARE duplicates (keep='first' marks duplicates after first)
print("\nThe duplicate rows:")
print(orders[orders.duplicated(subset=['order_id'], keep='first')])
```

---

###  Removing Duplicates

```python
# Remove fully duplicate rows (keep first occurrence)
df_clean = orders.drop_duplicates()
print("After removing full duplicates:", len(df_clean))

# Remove duplicates based on specific columns
df_unique_orders = orders.drop_duplicates(subset=['order_id'], keep='first')
print("After removing duplicate order IDs:", len(df_unique_orders))

# Keep LAST occurrence instead of first (useful for time-series updates)
df_latest = orders.drop_duplicates(subset=['order_id'], keep='last')

# Drop ALL occurrences of duplicate records (not just the extras)
df_no_dups_at_all = orders.drop_duplicates(subset=['order_id'], keep=False)
print("Rows with unique order IDs only:", len(df_no_dups_at_all))

# Reset index after dropping
df_clean = df_unique_orders.reset_index(drop=True)
```

---

###  Real-World Example: Banking Duplicate Transactions

```python
import pandas as pd

transactions = pd.DataFrame({
    'txn_id': ['T001', 'T002', 'T003', 'T001', 'T004'],
    'account': ['ACC001', 'ACC002', 'ACC001', 'ACC001', 'ACC003'],
    'amount':  [5000, 12000, 8000, 5000, 3000],
    'timestamp': ['2024-01-15 10:00', '2024-01-15 10:05',
                  '2024-01-15 10:10', '2024-01-15 10:00', '2024-01-15 10:15']
})

# Find exact duplicates (same txn_id AND same timestamp = true duplicate)
true_duplicates = transactions.duplicated(subset=['txn_id', 'timestamp'])
print(f"Found {true_duplicates.sum()} duplicate transaction(s)")
print(transactions[true_duplicates])

# Remove them
clean_transactions = transactions.drop_duplicates(subset=['txn_id', 'timestamp'])
print(f"\nClean transactions: {len(clean_transactions)}")
```

---

## Part 2: Data Transformation Techniques

Transformation reshapes data into a format suitable for analysis.

---

###  1. Data Type Conversion

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'price': ['45,000', '25,000', '1,20,000'],  # String with special chars
    'quantity': ['10', '25', '5'],                    # Numbers stored as strings
    'date': ['15-01-2024', '16-01-2024', '17-01-2024'],  # Date as string
    'in_stock': ['Yes', 'No', 'Yes'],                 # Boolean as text
    'rating': [4.5, np.nan, 3.8]
})

# Remove  and commas, convert to float
df['price'] = df['price'].str.replace('', '').str.replace(',', '').astype(float)

# Convert string to integer
df['quantity'] = df['quantity'].astype(int)

# Parse dates
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

# Convert Yes/No to boolean
df['in_stock'] = df['in_stock'].map({'Yes': True, 'No': False})

print(df.dtypes)
print(df)
```

---

###  2. String Transformations

```python
import pandas as pd

customers = pd.DataFrame({
    'name':  ['  priya sharma ', 'RAHUL KUMAR', 'aisha   khan'],
    'email': ['Priya@Gmail.COM', 'rahul.kumar@OUTLOOK.com', 'aisha@yahoo.in'],
    'phone': ['98-764-32100', '(91)876-543210', '+91 9876 543210']
})

# Standardize text
customers['name'] = customers['name'].str.strip().str.title()     # Remove spaces, Title Case
customers['email'] = customers['email'].str.lower().str.strip()   # Lowercase emails

# Extract digits only from phone numbers
customers['phone_clean'] = customers['phone'].str.replace(r'[^0-9]', '', regex=True)

# Get last 10 digits (Indian mobile number)
customers['phone_10d'] = customers['phone_clean'].str[-10:]

print(customers)
```

---

###  3. Date & Time Transformations

```python
import pandas as pd

# Transaction data
df = pd.DataFrame({
    'transaction_date': pd.date_range('2024-01-01', periods=10, freq='3D'),
    'amount': [1000, 2500, 800, 3200, 1500, 4100, 900, 2800, 1200, 3500]
})

# Extract components
df['year'] = df['transaction_date'].dt.year
df['month'] = df['transaction_date'].dt.month
df['month_name'] = df['transaction_date'].dt.month_name()
df['day_of_week'] = df['transaction_date'].dt.day_name()
df['quarter'] = df['transaction_date'].dt.quarter
df['week_number'] = df['transaction_date'].dt.isocalendar().week

# Is it a weekend?
df['is_weekend'] = df['transaction_date'].dt.dayofweek >= 5

# Days since transaction
df['days_ago'] = (pd.Timestamp.today() - df['transaction_date']).dt.days

print(df.head())
```

---

###  4. Binning / Discretization (Grouping continuous into categories)

```python
import pandas as pd

employees = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Carol', 'Dave', 'Eve', 'Frank', 'Grace'],
    'salary': [28000, 45000, 72000, 95000, 120000, 55000, 38000]
})

# Create salary bands (Equal-width bins)
employees['salary_band'] = pd.cut(
    employees['salary'],
    bins=[0, 35000, 60000, 90000, 150000],
    labels=['Entry', 'Mid', 'Senior', 'Lead']
)

# Create age groups using quantiles (Equal-frequency bins)
employees['salary_quartile'] = pd.qcut(
    employees['salary'],
    q=4,
    labels=['Q1 (Bottom 25%)', 'Q2', 'Q3', 'Q4 (Top 25%)']
)

print(employees)
```

**Real-Life Example:**
> Banks categorize customers into credit score brackets (Poor: 300-579, Fair: 580-669, Good: 670-739, Excellent: 740-850) to determine loan eligibility  this is binning!

---

###  5. Encoding Categorical Variables

```python
import pandas as pd

df = pd.DataFrame({
    'city': ['Mumbai', 'Delhi', 'Mumbai', 'Chennai', 'Delhi'],
    'product_tier': ['Budget', 'Premium', 'Mid', 'Premium', 'Budget'],
    'feedback': ['Positive', 'Negative', 'Positive', 'Neutral', 'Negative']
})

# Label Encoding (Ordinal categories with order)
tier_mapping = {'Budget': 1, 'Mid': 2, 'Premium': 3}
df['tier_encoded'] = df['product_tier'].map(tier_mapping)

# One-Hot Encoding (Nominal categories without order)
df_encoded = pd.get_dummies(df, columns=['city'], prefix='city', dtype=int)

print(df_encoded)
# Creates: city_Chennai, city_Delhi, city_Mumbai columns
```

---

###  6. Normalization & Standardization

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

df = pd.DataFrame({
    'age':    [25, 30, 22, 35, 28],
    'salary': [35000, 60000, 28000, 80000, 50000]
})

# Min-Max Normalization: scales to range [0, 1]
scaler = MinMaxScaler()
df[['age_norm', 'salary_norm']] = scaler.fit_transform(df[['age', 'salary']])

# Z-Score Standardization: mean=0, std=1 (better for ML)
std_scaler = StandardScaler()
df[['age_std', 'salary_std']] = std_scaler.fit_transform(df[['age', 'salary']])

print(df.round(3))
```

**When to use which?**
- **Normalization [0,1]**  When algorithm needs values in bounded range (Neural Networks)
- **Standardization (Z-score)**  When algorithm assumes normal distribution (Linear Regression, SVM)

---

##  Key Takeaways

1. **Duplicates** corrupt analysis  always check both full and partial key duplicates
2. **Data types** must be correct before any computation
3. **Strings** are messy  standardize case, strip whitespace, clean special characters
4. **Dates** should be datetime type, not strings
5. **Binning** converts continuous data into meaningful categories
6. **Encoding** converts categories into numbers for ML models
7. **Normalize/Standardize** numerical features before machine learning

---

*Previous: [Handling Missing Values](./02_Handling_Missing_Values.md)*
