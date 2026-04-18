#  Pandas & DataFrame Operations

> **Learning Goal:** Master the Pandas library  the most important tool for data analysis in Python.

---

##  Getting Started with Pandas

Before we dive into the code, it's essential to understand that **Pandas** is the industry standard for data manipulation in Python. It's built on top of NumPy and offers high-performance, easy-to-use data structures.

###  Let's Dive Deep!
To complement this session and gain an official credential, we highly recommend completing the:
[ **Kaggle Pandas Certification**](https://www.kaggle.com/learn/pandas)

This will help you master the fundamentals and prepare you for real-world data challenges.

---

##  What is Pandas?

**Pandas** is a Python library that provides two primary data structures:
- **Series**  1D labeled array (like a single column)
- **DataFrame**  2D labeled table (like an Excel spreadsheet or SQL table)

**Real-World Analogy:**
> Think of a DataFrame as an Excel spreadsheet that you can program with Python to automatically process millions of rows in seconds.

---

##  Creating DataFrames

```python
import pandas as pd
import numpy as np

#  Method 1: From a dictionary 
employee_data = {
    'emp_id':     [101, 102, 103, 104, 105],
    'name':       ['Priya', 'Rahul', 'Aisha', 'Karan', 'Meera'],
    'department': ['Engineering', 'Marketing', 'Engineering', 'HR', 'Marketing'],
    'salary':     [85000, 62000, 92000, 55000, 70000],
    'experience': [5, 3, 7, 2, 4],
    'join_date':  pd.to_datetime(['2019-03-15', '2021-07-01', '2017-11-20',
                                   '2022-02-10', '2020-09-05'])
}
df = pd.DataFrame(employee_data)
print(df)
print("\nShape:", df.shape)  # (5, 6)

#  Method 2: From CSV 
# df = pd.read_csv('employees.csv')

#  Method 3: From URL 
# df = pd.read_csv('https://example.com/data.csv')
```

---

##  Exploring a DataFrame

```python
# First look at the data
print(df.head(3))          # First 3 rows
print(df.tail(2))          # Last 2 rows
print(df.sample(2))        # 2 random rows

# Structure information
print(df.shape)            # (rows, columns)
print(df.columns.tolist()) # Column names
print(df.dtypes)           # Data types
print(df.info())           # Complete summary (memory, nulls, dtypes)

# Statistical summary
print(df.describe())       # Stats for numerical columns
print(df.describe(include='object'))  # Stats for text columns
print(df.nunique())        # Number of unique values per column
print(df['department'].value_counts())  # Frequency of each category
```

---

##  Selecting Data: Columns and Rows

```python
#  Select Columns 
# Single column  returns a Series
names = df['name']
print(type(names))  # pandas.core.series.Series

# Multiple columns  returns a DataFrame
subset = df[['name', 'salary', 'department']]
print(type(subset))  # pandas.core.frame.DataFrame

#  Select Rows by Position (iloc) 
# iloc = integer location
first_row = df.iloc[0]        # First row
last_two = df.iloc[-2:]       # Last 2 rows
block = df.iloc[1:4, 0:3]     # Rows 1-3, Columns 0-2
scalar = df.iloc[2, 3]        # Row 2, Column 3 (value: 92000)

#  Select Rows by Label (loc) 
# loc = label-based location (uses index values and column names)
df.set_index('emp_id', inplace=True)  # Set emp_id as index
emp_102 = df.loc[102]                  # Get employee 102
emp_subset = df.loc[[101, 103], ['name', 'salary']]  # Specific rows and columns
df.reset_index(inplace=True)          # Reset to default integer index

#  Select Rows by Condition (Boolean Indexing) 
engineers = df[df['department'] == 'Engineering']
senior = df[df['experience'] >= 5]
high_earners = df[df['salary'] > 75000]
```

---

##  Adding, Updating, Deleting Columns

```python
#  Add new columns 
# Computed column
df['annual_bonus'] = df['salary'] * 0.10  # 10% of salary

# Conditional column
df['seniority'] = np.where(df['experience'] >= 5, 'Senior', 'Junior')

# Multiple conditions
conditions = [
    df['experience'] < 2,
    (df['experience'] >= 2) & (df['experience'] < 5),
    df['experience'] >= 5
]
labels = ['Junior', 'Mid-level', 'Senior']
df['level'] = np.select(conditions, labels)

# Apply a custom function
def categorize_salary(salary):
    if salary < 60000:
        return 'Below Average'
    elif salary < 80000:
        return 'Average'
    else:
        return 'Above Average'

df['salary_category'] = df['salary'].apply(categorize_salary)

#  Update existing values 
df.loc[df['emp_id'] == 104, 'salary'] = 58000  # Update specific row

#  Delete columns 
df_clean = df.drop(columns=['annual_bonus'])  # Drop one column
df_clean = df.drop(columns=['level', 'salary_category'])  # Drop multiple

print(df.head())
```

---

##  Sorting Data

```python
# Sort by salary (descending = highest first)
df_sorted = df.sort_values('salary', ascending=False)
print("Top earners:\n", df_sorted[['name', 'salary']].head(3))

# Sort by multiple columns
df_sorted2 = df.sort_values(['department', 'salary'], ascending=[True, False])
print("\nBy Dept and Salary:\n", df_sorted2[['department', 'name', 'salary']])

# Sort by index
df_sorted_idx = df.sort_index()
```

---

##  Joining DataFrames (Like SQL JOIN)

```python
import pandas as pd

# Employee basic info
employees = pd.DataFrame({
    'emp_id': [101, 102, 103, 104, 105],
    'name':   ['Priya', 'Rahul', 'Aisha', 'Karan', 'Meera'],
    'dept_id': [10, 20, 10, 30, 20]
})

# Department info
departments = pd.DataFrame({
    'dept_id':   [10, 20, 30],
    'dept_name': ['Engineering', 'Marketing', 'HR'],
    'location':  ['Bangalore', 'Mumbai', 'Delhi']
})

# Performance ratings (not all employees have ratings)
ratings = pd.DataFrame({
    'emp_id': [101, 102, 103],
    'rating': ['A', 'B', 'A+']
})

# INNER JOIN  only matching records
inner = pd.merge(employees, departments, on='dept_id', how='inner')
print("Inner join:\n", inner)

# LEFT JOIN  all employees, even without department info
left = pd.merge(employees, departments, on='dept_id', how='left')

# With ratings (some employees missing)
with_ratings = pd.merge(inner, ratings, on='emp_id', how='left')
with_ratings['rating'] = with_ratings['rating'].fillna('Not Rated')
print("\nWith Ratings:\n", with_ratings[['name', 'dept_name', 'rating']])
```

---

##  Key Takeaways

1. **DataFrame = Excel table** in Python  rows and columns with labels
2. Use `.head()`, `.info()`, `.describe()` to explore data first
3. **`iloc`** selects by position (integers), **`loc`** selects by label
4. **Boolean indexing** is the most powerful way to filter rows
5. Use `merge()` to join multiple DataFrames like SQL JOINs
6. `apply()` lets you run custom functions on any column

---

*Previous: [NumPy Introduction](./01_NumPy_Introduction.md) | Next: [Filtering & Aggregation](./03_Filtering_Aggregation.md)*
