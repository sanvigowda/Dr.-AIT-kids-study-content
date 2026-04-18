#  Filtering & Aggregation in Pandas

> **Learning Goal:** Master filtering rows with conditions and summarizing data with groupby and aggregation  the most used operations in real analytics work.

---

## Part 1: Filtering Data

###  Basic Boolean Filtering

```python
import pandas as pd
import numpy as np

# Retail sales dataset
sales = pd.DataFrame({
    'order_id':  range(1001, 1016),
    'customer':  ['Alice', 'Bob', 'Carol', 'Dave', 'Eve', 'Frank',
                  'Grace', 'Hank', 'Iris', 'Jack', 'Kim', 'Leo',
                  'Mia', 'Ned', 'Olivia'],
    'category':  ['Electronics', 'Clothing', 'Electronics', 'Food', 'Electronics',
                  'Clothing', 'Food', 'Electronics', 'Clothing', 'Food',
                  'Electronics', 'Clothing', 'Food', 'Electronics', 'Clothing'],
    'city':      ['Mumbai', 'Delhi', 'Mumbai', 'Chennai', 'Bangalore',
                  'Mumbai', 'Delhi', 'Chennai', 'Bangalore', 'Mumbai',
                  'Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Delhi'],
    'amount':    [4500, 850, 12000, 320, 8500, 1200, 450, 6500,
                  950, 280, 15000, 1800, 560, 7200, 2100],
    'quantity':  [2, 3, 1, 5, 1, 4, 6, 2, 3, 4, 1, 2, 7, 1, 3],
    'returned':  [False, False, True, False, False, True, False,
                  False, True, False, False, False, True, False, False]
})

#  Single condition 
electronics = sales[sales['category'] == 'Electronics']
print(f"Electronics orders: {len(electronics)}")

high_value = sales[sales['amount'] > 5000]
print(f"High value orders (>5000): {len(high_value)}")

#  Multiple conditions (AND) 
# Must use & and put each condition in parentheses
electronics_mumbai = sales[(sales['category'] == 'Electronics') & 
                            (sales['city'] == 'Mumbai')]
print(f"\nElectronics in Mumbai: {len(electronics_mumbai)}")

#  Multiple conditions (OR) 
electronics_or_food = sales[(sales['category'] == 'Electronics') | 
                             (sales['category'] == 'Food')]
print(f"Electronics OR Food: {len(electronics_or_food)}")

#  NOT condition 
not_returned = sales[~sales['returned']]
print(f"Orders not returned: {len(not_returned)}")
```

---

###  Advanced Filtering Methods

```python
#  isin()  filter multiple values 
metro_cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai']
metro_sales = sales[sales['city'].isin(metro_cities)]

# Opposite: NOT in list
non_metro = sales[~sales['city'].isin(['Mumbai', 'Delhi'])]

#  between()  range filter 
mid_range = sales[sales['amount'].between(1000, 8000)]
print(f"\nOrders between 1000-8000: {len(mid_range)}")

#  str.contains()  text search 
# Find customers whose names start with letters A-G
early_alphabet = sales[sales['customer'].str.contains('^[A-G]', regex=True)]

# Find categories containing 'onic' (case insensitive)
matching = sales[sales['category'].str.contains('onic', case=False)]

#  query()  SQL-like syntax (readable for complex filters) 
result = sales.query("amount > 5000 and category == 'Electronics'")
print(f"\nquery() result: {len(result)} rows")

# With variables in query
min_amount = 3000
top_orders = sales.query("amount > @min_amount and returned == False")
```

---

###  Multiple Condition Filtering  Real Scenario

```python
# Business Question: Find high-value orders in electronics that were NOT returned
# to understand our best performing sales

top_electronics = sales[
    (sales['category'] == 'Electronics') &
    (sales['amount'] >= 5000) &
    (sales['returned'] == False)
].sort_values('amount', ascending=False)

print("Top Electronics Orders (not returned):")
print(top_electronics[['customer', 'city', 'amount']].to_string(index=False))
```

---

## Part 2: Aggregation with GroupBy

###  Basic GroupBy

Think of GroupBy like Excel's PivotTable  split the data into groups, apply a function, and combine the results.

```python
# Total sales by category
by_category = sales.groupby('category')['amount'].sum()
print("Total Sales by Category:")
print(by_category)

# Average order value by city
avg_by_city = sales.groupby('city')['amount'].mean().round(2)
print("\nAverage Order Value by City:")
print(avg_by_city.sort_values(ascending=False))

# Count of orders per category
order_count = sales.groupby('category')['order_id'].count()
print("\nOrder Count by Category:")
print(order_count)
```

---

###  Multiple Aggregations with agg()

```python
# Multiple stats at once for each category
category_stats = sales.groupby('category').agg(
    total_revenue  = ('amount', 'sum'),
    avg_order      = ('amount', 'mean'),
    max_order      = ('amount', 'max'),
    min_order      = ('amount', 'min'),
    order_count    = ('order_id', 'count'),
    total_units    = ('quantity', 'sum'),
    return_rate    = ('returned', 'mean')  # mean of boolean = proportion
).round(2)

category_stats['return_rate'] = (category_stats['return_rate'] * 100).round(1)
category_stats = category_stats.rename(columns={'return_rate': 'return_rate_%'})

print("Category Performance Summary:")
print(category_stats)
```

---

###  Multi-Level GroupBy

```python
# Group by TWO columns: category  city
city_category = sales.groupby(['city', 'category']).agg(
    revenue = ('amount', 'sum'),
    orders  = ('order_id', 'count')
).reset_index()

print("City-Category Revenue:")
print(city_category.sort_values('revenue', ascending=False))

# Pivot table format (easier to read)
pivot = city_category.pivot(index='city', columns='category', values='revenue').fillna(0)
print("\nPivot Table:")
print(pivot)
```

---

###  transform()  Add Aggregated Values Back to Original

```python
# Add a column with category total revenue WHILE keeping all rows
sales['category_total'] = sales.groupby('category')['amount'].transform('sum')

# Calculate each order's % contribution to its category total
sales['pct_of_category'] = (sales['amount'] / sales['category_total'] * 100).round(1)

# Rank within each category
sales['rank_in_category'] = sales.groupby('category')['amount'].rank(ascending=False)

print(sales[['customer', 'category', 'amount', 'pct_of_category', 'rank_in_category']]
      .sort_values(['category', 'rank_in_category']))
```

---

###  Real-World Example: E-Commerce Sales Analysis

```python
import pandas as pd
import numpy as np

# Create a realistic monthly sales dataset
np.random.seed(42)
dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
n = len(dates)

monthly_data = pd.DataFrame({
    'date':     np.random.choice(dates, 500),
    'category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books'], 500),
    'region':   np.random.choice(['North', 'South', 'East', 'West'], 500),
    'revenue':  np.random.randint(500, 50000, 500),
    'units':    np.random.randint(1, 20, 500)
})

monthly_data['month'] = monthly_data['date'].dt.month_name()
monthly_data['quarter'] = 'Q' + monthly_data['date'].dt.quarter.astype(str)

# Q1: Which category generates the most revenue per quarter?
quarterly_category = monthly_data.groupby(['quarter', 'category'])['revenue'].sum().reset_index()
best_per_quarter = quarterly_category.loc[quarterly_category.groupby('quarter')['revenue'].idxmax()]
print("Best Category per Quarter:")
print(best_per_quarter.to_string(index=False))

# Q2: Which region has highest average order value?
region_avg = monthly_data.groupby('region').agg(
    avg_revenue = ('revenue', 'mean'),
    total_orders = ('revenue', 'count')
).round(2)
print("\nRegion Performance:")
print(region_avg)
```

---

###  Window Functions with rolling() & expanding()

```python
import pandas as pd

# Daily sales data
daily_sales = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=30),
    'revenue': [4500, 5200, 4800, 6100, 5500, 4700, 6800, 7200, 6500,
                5900, 7500, 8100, 7800, 6900, 8500, 9200, 8800, 7600,
                9500, 10100, 9800, 8900, 10500, 11200, 10800, 9900,
                11500, 12100, 11800, 10900]
})

# 7-day rolling average (smooths out day-to-day noise)
daily_sales['7d_avg'] = daily_sales['revenue'].rolling(window=7).mean().round(0)

# 7-day rolling max
daily_sales['7d_max'] = daily_sales['revenue'].rolling(window=7).max()

# Cumulative (running) total
daily_sales['cumulative_revenue'] = daily_sales['revenue'].cumsum()

# Month-to-date running average
daily_sales['running_avg'] = daily_sales['revenue'].expanding().mean().round(0)

print(daily_sales.head(15).to_string(index=False))
```

---

##  Key Takeaways

1. **Boolean filtering** with `&`, `|`, `~` is how we select rows by condition
2. Use `isin()` for multiple values, `between()` for ranges, `str.contains()` for text
3. **`groupby()`** is the most powerful aggregation tool  works like SQL's GROUP BY
4. Use **`agg()`** with named aggregations for clean, readable multi-stat summaries
5. **`transform()`** adds group-level stats back to the original DataFrame
6. **Rolling windows** smooth time-series data and show trends

---

*Previous: [Pandas & DataFrame Operations](./02_Pandas_DataFrame_Operations.md)*
