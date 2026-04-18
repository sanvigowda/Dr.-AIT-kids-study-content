"""
Day 1 | Session 2 Lab: Cleaning Real-World Dataset (VS Code Version)
====================================================================
Course: Data Analytics Complete | Day: 1 | Session: 2

Dataset: E-Commerce Sales Dataset with intentional data quality issues

Install dependencies: pip install pandas numpy matplotlib
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 65)
print("DAY 1 | SESSION 2 LAB: Data Cleaning Pipeline")
print("=" * 65)

# 
# SECTION 1: CREATE RAW (DIRTY) DATASET
# Real e-commerce data has all sorts of issues  let's simulate them
# 

np.random.seed(42)

raw_data = {
    'order_id':        ['ORD001', 'ORD002', 'ORD003', 'ORD004', 'ORD005',
                         'ORD006', 'ORD007', 'ORD008', 'ORD009', 'ORD010',
                         'ORD002',  # DUPLICATE
                         'ORD011', 'ORD012', 'ORD013', 'ORD014', 'ORD015'],
    'customer_name':   ['Priya Sharma', '  rahul KUMAR  ', 'Aisha Khan', None,
                         'Karan Patel', 'meera SINGH', 'Dev Malhotra', 'Sana Rao',
                         'Arjun Nair', 'Pooja Mehta',
                         '  rahul KUMAR  ',  # DUPLICATE row
                         'Ravi Gupta', None, 'Ananya Roy', 'Mohit Jain', 'Deepa Krishnan'],
    'email':           ['priya@gmail.com', 'Rahul@OUTLOOK.com', 'aisha@yahoo.in', None,
                         'karan@gmail.com', None, 'dev@hotmail.com', 'sana@gmail.com',
                         'arjun@yahoo.in', 'pooja@gmail.com',
                         'Rahul@OUTLOOK.com',  # DUPLICATE
                         'ravi@gmail.com', None, 'ananya@yahoo.in', 'mohit@gmail.com', 'deepa@gmail.com'],
    'product':         ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Laptop',
                         'Smartwatch', 'Smartphone', 'Laptop', 'Headphones', 'Tablet',
                         'Smartphone',   # DUPLICATE
                         'Camera', 'Laptop', 'Smartwatch', 'Headphones', 'Tablet'],
    'category':        ['Electronics', 'Electronics', 'Electronics', 'Audio', 'Electronics',
                         'Wearables', 'Electronics', 'Electronics', 'Audio', 'Electronics',
                         'Electronics',  # DUPLICATE
                         'Photography', 'ELECTRONICS',  # inconsistent case
                         'Wearables', 'audio',   # inconsistent case
                         'Electronics'],
    'price':           [45000, 25000, 35000, 8500, 55000,
                         12000, 28000, 42000, -9500,  # NEGATIVE PRICE (error!)
                         32000,
                         25000,  # DUPLICATE
                         65000, 49000, 15000, 7500, 28000],
    'quantity':        [1, 2, 1, 3, 1, 2, 1, 1, 2, 1,
                         2,  # DUPLICATE
                         1, 1, 2, 4, 1],
    'discount_pct':    [10, 5, 15, 0, 20, 8, 5, 12, 0, 10,
                         5,  # DUPLICATE
                         0, 15, 8, 5, 10],
    'order_date':      ['15-01-2024', '2024-01-16', 'Jan 17 2024', '2024-01-18', '19/01/2024',
                         '2024-01-20', '2024-01-21', '22-01-2024', '2024-01-23', '2024-01-24',
                         '2024-01-16',  # DUPLICATE
                         '2024-01-25', '2024-01-26', '2024-01-27', '2024-01-28', '2024-01-29'],
    'city':            ['Mumbai', 'Delhi', 'Chennai', None, 'Bangalore',
                         'Pune', 'Mumbai', 'hyderabad',  # lowercase
                         'Kolkata', 'Bangalore',
                         'Delhi',  # DUPLICATE
                         'Jaipur', 'mumbai',  # lowercase
                         'Delhi', 'Chennai', 'Bangalore'],
    'rating':          [5, 4, None, 3, 5, 4, None, 4, 3, 5,
                         4,  # DUPLICATE
                         5, 4, 3, None, 5],
}

df_raw = pd.DataFrame(raw_data)
print(f"\n Raw dataset: {df_raw.shape[0]} rows  {df_raw.shape[1]} columns")
print(df_raw.to_string())

# 
# SECTION 2: AUDIT THE DATA  Find All Quality Issues
# 
print("\n" + "=" * 65)
print("STEP 1: DATA AUDIT")
print("=" * 65)

print("\n ISSUE 1  MISSING VALUES:")
missing_report = pd.DataFrame({
    'Missing Count': df_raw.isnull().sum(),
    'Missing %': (df_raw.isnull().sum() / len(df_raw) * 100).round(1)
})
print(missing_report[missing_report['Missing Count'] > 0])

print("\n ISSUE 2  DUPLICATES:")
print(f"  Full duplicate rows: {df_raw.duplicated().sum()}")
print(f"  Duplicate order_ids: {df_raw.duplicated(subset=['order_id']).sum()}")

print("\n ISSUE 3  INVALID VALUES:")
print(f"  Negative prices: {(df_raw['price'] < 0).sum()} rows")
print(f"  Prices = 0: {(df_raw['price'] == 0).sum()} rows")

print("\n ISSUE 4  INCONSISTENT TEXT:")
print(f"  Unique categories: {df_raw['category'].str.lower().unique()}")
print(f"  Cities (sample): {df_raw['city'].dropna().str.lower().unique()[:5]}")

# 
# SECTION 3: CLEAN THE DATA  Step by Step
# 
print("\n" + "=" * 65)
print("STEP 2: CLEANING PIPELINE")
print("=" * 65)

df = df_raw.copy()  # Always work on a copy!

#  Fix 1: Remove Duplicates 
before = len(df)
df = df.drop_duplicates(subset=['order_id'], keep='first')
df = df.reset_index(drop=True)
print(f"\n Fix 1  Duplicates removed: {before}  {len(df)} rows")

#  Fix 2: Standardize Text Fields 
# Clean customer names
df['customer_name'] = df['customer_name'].str.strip().str.title()

# Standardize email
df['email'] = df['email'].str.lower().str.strip()

# Standardize category
df['category'] = df['category'].str.strip().str.title()

# Standardize city
df['city'] = df['city'].str.strip().str.title()

print(" Fix 2  Text fields standardized (names, emails, categories, cities)")

#  Fix 3: Fix Invalid Price Values 
invalid_price_mask = df['price'] <= 0
invalid_count = invalid_price_mask.sum()
# Replace with median price
df.loc[invalid_price_mask, 'price'] = df['price'][df['price'] > 0].median()
print(f" Fix 3  Invalid prices corrected: {invalid_count} records")

#  Fix 4: Standardize Dates 
df['order_date'] = pd.to_datetime(df['order_date'], infer_datetime_format=True, errors='coerce')
failed_dates = df['order_date'].isnull().sum()
print(f" Fix 4  Dates standardized (failed to parse: {failed_dates})")

#  Fix 5: Handle Missing Values 
# Missing city  fill with 'Unknown'
df['city'] = df['city'].fillna('Unknown')

# Missing rating  fill with median rating
df['rating'] = df['rating'].fillna(df['rating'].median())

# Missing customer names  mark as 'Anonymous'
df['customer_name'] = df['customer_name'].fillna('Anonymous')

# Missing email  mark as 'not_provided'
df['email'] = df['email'].fillna('not_provided')

print(" Fix 5  Missing values handled")

#  Fix 6: Engineer New Features 
# Calculate actual revenue after discount
df['revenue'] = (df['price'] * df['quantity'] * (1 - df['discount_pct']/100)).round(2)

# Extract date components
df['order_month'] = df['order_date'].dt.month_name()
df['order_weekday'] = df['order_date'].dt.day_name()

# Customer tier based on revenue
df['customer_tier'] = pd.cut(
    df['revenue'],
    bins=[0, 10000, 30000, 60000, float('inf')],
    labels=['Bronze', 'Silver', 'Gold', 'Platinum']
)

print(" Fix 6  New features engineered: revenue, order_month, customer_tier")

# 
# SECTION 4: VALIDATION  Verify the cleaned data
# 
print("\n" + "=" * 65)
print("STEP 3: VALIDATION")
print("=" * 65)

print(f"\n Final shape: {df.shape[0]} rows  {df.shape[1]} columns")
print(f"   Missing values remaining: {df.isnull().sum().sum()}")
print(f"   Duplicate rows: {df.duplicated().sum()}")
print(f"   Negative prices: {(df['price'] < 0).sum()}")

print("\n Cleaned DataFrame (first 5 rows):")
print(df[['order_id', 'customer_name', 'product', 'category',
          'price', 'quantity', 'revenue', 'city', 'rating']].head().to_string(index=False))

# 
# SECTION 5: ANALYSIS ON CLEAN DATA
# 
print("\n" + "=" * 65)
print("STEP 4: ANALYSIS (Now We Can Trust the Data!)")
print("=" * 65)

# Revenue by category
print("\n Revenue by Category:")
print(df.groupby('category')['revenue'].sum().sort_values(ascending=False).apply(lambda x: f"{x:,.0f}"))

# Top cities
print("\n Top Cities by Revenue:")
print(df.groupby('city')['revenue'].sum().sort_values(ascending=False).head(5).apply(lambda x: f"{x:,.0f}"))

# Customer tiers
print("\n Customer Tier Distribution:")
print(df['customer_tier'].value_counts())

#  Visualization 
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 1 Session 2 Lab: E-Commerce Data Cleaning Results', fontsize=14, fontweight='bold')

# 1. Revenue by Category
cat_rev = df.groupby('category')['revenue'].sum().sort_values(ascending=True)
axes[0, 0].barh(cat_rev.index, cat_rev.values/1000, color='steelblue', alpha=0.8)
axes[0, 0].set_xlabel('Revenue ( Thousands)')
axes[0, 0].set_title('Revenue by Category')
axes[0, 0].grid(axis='x', alpha=0.3)

# 2. Customer Tier Distribution
tier_counts = df['customer_tier'].value_counts()
axes[0, 1].pie(tier_counts, labels=tier_counts.index, autopct='%1.1f%%',
               colors=['#CD7F32', '#C0C0C0', '#FFD700', '#E5E4E2'])
axes[0, 1].set_title('Customer Tier Distribution')

# 3. Rating Distribution
axes[1, 0].hist(df['rating'], bins=5, color='coral', alpha=0.8, edgecolor='black')
axes[1, 0].set_xlabel('Rating')
axes[1, 0].set_ylabel('Count')
axes[1, 0].set_title('Rating Distribution')

# 4. Revenue by City
city_rev = df.groupby('city')['revenue'].sum().sort_values(ascending=False).head(6)
axes[1, 1].bar(city_rev.index, city_rev.values/1000, color='teal', alpha=0.8)
axes[1, 1].set_xlabel('City')
axes[1, 1].set_ylabel('Revenue ( Thousands)')
axes[1, 1].set_title('Top Cities by Revenue')
axes[1, 1].tick_params(axis='x', rotation=30)
axes[1, 1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('session2_lab_output.png', dpi=100, bbox_inches='tight')
plt.show()
print("\n Charts saved as 'session2_lab_output.png'")

#  Save cleaned data 
df.to_csv('cleaned_ecommerce_data.csv', index=False)
print(" Cleaned data saved as 'cleaned_ecommerce_data.csv'")
print("\n Session 2 Lab Complete!")
