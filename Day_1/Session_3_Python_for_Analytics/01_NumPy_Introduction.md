#  Introduction to NumPy

> **Learning Goal:** Understand NumPy arrays and core operations  the foundation for all data science in Python.

---

##  Why NumPy?

Before NumPy, Python lists handled data. But Python lists are **slow** for large datasets.

```python
# Python list  slow for large data
prices = [100, 200, 150, 300, 250]
# To add 10% tax: you need a loop
tax_prices = [p * 1.1 for p in prices]  # Loop required

# NumPy array  fast for large data
import numpy as np
prices = np.array([100, 200, 150, 300, 250])
tax_prices = prices * 1.1  # No loop needed! Works on entire array
```

**Speed Test:**
> For 1 million numbers, NumPy is **100-300x faster** than Python lists.

---

##  Creating NumPy Arrays

```python
import numpy as np

# From Python lists
arr1d = np.array([10, 20, 30, 40, 50])             # 1D array
arr2d = np.array([[1, 2, 3], [4, 5, 6]])            # 2D array (matrix)
arr3d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])  # 3D array

print(f"1D shape: {arr1d.shape}")   # (5,)
print(f"2D shape: {arr2d.shape}")   # (2, 3)
print(f"3D shape: {arr3d.shape}")   # (2, 2, 2)

# Useful creation functions
zeros = np.zeros((3, 4))          # 3x4 matrix of zeros
ones = np.ones((2, 3))            # 2x3 matrix of ones
identity = np.eye(4)              # 4x4 identity matrix
range_arr = np.arange(0, 20, 2)   # [0, 2, 4, ..., 18]
linspace = np.linspace(0, 1, 10)  # 10 evenly spaced points from 0 to 1
random_arr = np.random.rand(3, 3) # 3x3 matrix of random numbers [0,1]

# Data types
prices = np.array([100.5, 200.3, 150.7], dtype=np.float32)
ids = np.array([101, 102, 103], dtype=np.int64)
print(prices.dtype, ids.dtype)
```

---

##  Array Indexing & Slicing

```python
import numpy as np

# Monthly sales data (12 months)
monthly_sales = np.array([1200, 1500, 1100, 1800, 2100, 1950,
                           2300, 2500, 2200, 2800, 3100, 3500])

# Basic indexing
print("January sales:", monthly_sales[0])      # 1200
print("December sales:", monthly_sales[-1])    # 3500
print("Last 3 months:", monthly_sales[-3:])    # [2800, 3100, 3500]
print("Q1 (months 1-3):", monthly_sales[0:3]) # [1200, 1500, 1100]
print("Q2 (months 4-6):", monthly_sales[3:6]) # [1800, 2100, 1950]

# 2D array indexing  e.g., store sales matrix (stores  months)
store_sales = np.array([
    [1200, 1500, 1800, 2000],  # Store A: Jan, Feb, Mar, Apr
    [800,  1100, 1300, 1600],  # Store B
    [1500, 1700, 2000, 2200],  # Store C
])

print("\nStore B, March:", store_sales[1, 2])    # 1300
print("All stores, January:", store_sales[:, 0])  # [1200, 800, 1500]
print("Store A all months:", store_sales[0, :])   # [1200, 1500, 1800, 2000]
print("Top-right 2x2 block:", store_sales[:2, 2:])  # [[1800, 2000], [1300, 1600]]

# Boolean indexing  very powerful
high_sales = monthly_sales[monthly_sales > 2000]
print("\nMonths with sales > 2000:", high_sales)

# Find WHICH months had high sales
high_months = np.where(monthly_sales > 2000)[0] + 1  # +1 for 1-indexed month numbers
print("Month numbers with sales > 2000:", high_months)
```

---

##  NumPy Mathematical Operations

```python
import numpy as np

# Stock prices for 5 days
stock_a = np.array([450.0, 455.0, 448.0, 460.0, 475.0])
stock_b = np.array([280.0, 285.0, 282.0, 291.0, 295.0])

# Arithmetic (element-wise)
print("Stock A + Stock B (portfolio):", stock_a + stock_b)
print("Stock A price change:", stock_a - stock_a[0])
print("Normalized (divide by first price):", stock_a / stock_a[0])
print("10% bonded return:", stock_a * 1.10)

# Statistical operations
print("\n--- Statistics for Stock A ---")
print(f"Mean price: {stock_a.mean():.2f}")
print(f"Max price: {stock_a.max():.2f}")
print(f"Min price: {stock_a.min():.2f}")
print(f"Standard Deviation: {stock_a.std():.2f}")
print(f"Total return: {((stock_a[-1] - stock_a[0]) / stock_a[0]) * 100:.2f}%")
```

---

##  Array Reshaping  Critical for Data Science

```python
import numpy as np

# Raw sensor data collected as 1D array
sensor_data = np.arange(1, 25)  # 24 readings
print("Original shape:", sensor_data.shape)  # (24,)

# Reshape to 6 time periods  4 sensors
reshaped = sensor_data.reshape(6, 4)
print("Reshaped to 6x4:")
print(reshaped)

# Flatten back to 1D
flat = reshaped.flatten()
print("Flattened back:", flat[:5], "...")

# Transpose (rows become columns)
transposed = reshaped.T  # Now 4 sensors  6 time periods
print("Transposed shape:", transposed.shape)  # (4, 6)

# Add a dimension (needed for ML models)
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
arr_3d = arr_2d[:, :, np.newaxis]  # (2, 3)  (2, 3, 1)
print("Extended shape:", arr_3d.shape)
```

---

##  Array Concatenation & Stacking

```python
import numpy as np

# Q1 and Q2 sales data
q1_sales = np.array([1200, 1500, 1100])  # Jan, Feb, Mar
q2_sales = np.array([1800, 2100, 1950])  # Apr, May, Jun

# Combine into one array
h1_sales = np.concatenate([q1_sales, q2_sales])
print("H1 Sales:", h1_sales)

# Stack arrays (vertical stacking = adding rows)
store_data = np.array([[100, 200, 300],    # Store A monthly sales
                        [150, 180, 220]])   # Store B monthly sales

new_store = np.array([[120, 160, 200]])    # Store C joins

all_stores = np.vstack([store_data, new_store])  # vertical stack
print("All stores:")
print(all_stores)

# Horizontal stack (adding columns)
monthly_cost = np.array([[80, 150, 250],    # Store A costs
                          [100, 130, 180],  # Store B costs
                          [90, 120, 170]])  # Store C costs

combined = np.hstack([all_stores, monthly_cost])  # 36
print("Sales + Cost combined shape:", combined.shape)
```

---

##  Real-World Example: Student Grade Analysis

```python
import numpy as np

# 5 students, 4 subjects (Math, Science, English, Hindi)
grades = np.array([
    [85, 92, 78, 88],   # Student 1
    [72, 68, 80, 75],   # Student 2
    [95, 97, 89, 93],   # Student 3
    [60, 55, 70, 65],   # Student 4
    [78, 82, 85, 80],   # Student 5
])

subjects = ['Math', 'Science', 'English', 'Hindi']
students = ['Alice', 'Bob', 'Carol', 'Dave', 'Eve']

# Per-student average
student_avg = grades.mean(axis=1)  # axis=1 = across columns (per row)
print("Student Averages:")
for name, avg in zip(students, student_avg):
    print(f"  {name}: {avg:.1f}")

# Per-subject average
subject_avg = grades.mean(axis=0)  # axis=0 = down rows (per column)
print("\nSubject Averages:")
for subject, avg in zip(subjects, subject_avg):
    print(f"  {subject}: {avg:.1f}")

# Find top student
top_student_idx = student_avg.argmax()
print(f"\nTop Student: {students[top_student_idx]} with {student_avg[top_student_idx]:.1f}")

# Students who failed (< 60 in any subject)
failed_mask = np.any(grades < 60, axis=1)
print(f"\nStudents with at least one failing grade:")
print([students[i] for i in np.where(failed_mask)[0]])
```

---

##  Key Takeaways

1. NumPy arrays are **faster** and more memory-efficient than Python lists
2. Arrays support **vectorized operations**  no loops needed
3. **shape** tells you the dimensions of your array
4. **axis=0** operates down rows (per column), **axis=1** operates across columns (per row)
5. Boolean indexing is **powerful for filtering**
6. `reshape()`, `flatten()`, and `transpose()` are essential for ML data preparation

---

*Previous: [Session 2](../Session_2_Data_Collection_Cleaning/) | Next: [Pandas & DataFrame Operations](./02_Pandas_DataFrame_Operations.md)*
