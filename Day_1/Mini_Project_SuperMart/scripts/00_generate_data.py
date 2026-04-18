"""
SuperMart Sales Intelligence  Data Generator
=============================================
Run this script FIRST to generate the synthetic dataset.
Usage: python 00_generate_data.py
"""

import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(2024)
n = 300

print("Generating SuperMart raw dataset...")

# Stores and cities
stores = ['Store A', 'Store B', 'Store C', 'Store D', 'Store E']
cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad']

# Products
product_catalog = {
    'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smartwatch'],
    'Clothing': ['T-Shirt', 'Jeans', 'Kurti', 'Saree', 'Jacket'],
    'Food & Beverages': ['Coffee', 'Health Bar', 'Juice Pack', 'Snacks', 'Tea'],
    'Books': ['Fiction Novel', 'Programming Book', 'Self-Help', 'Biography', 'Comics'],
    'Sports': ['Yoga Mat', 'Dumbbells', 'Cricket Bat', 'Running Shoes', 'Football'],
}

price_catalog = {
    'Laptop': 55000, 'Smartphone': 28000, 'Tablet': 35000,
    'Headphones': 8500, 'Smartwatch': 15000,
    'T-Shirt': 799, 'Jeans': 1299, 'Kurti': 999, 'Saree': 2499, 'Jacket': 1899,
    'Coffee': 349, 'Health Bar': 199, 'Juice Pack': 149, 'Snacks': 299, 'Tea': 249,
    'Fiction Novel': 399, 'Programming Book': 899, 'Self-Help': 499,
    'Biography': 599, 'Comics': 299,
    'Yoga Mat': 1299, 'Dumbbells': 2499, 'Cricket Bat': 3999,
    'Running Shoes': 4499, 'Football': 999,
}

# Generate base data
categories = np.random.choice(list(product_catalog.keys()), n)
products = [np.random.choice(product_catalog[cat]) for cat in categories]
prices = [price_catalog[p] for p in products]

data = {
    'transaction_id': [f'TXN{i:04d}' for i in range(1, n+1)],
    'store': np.random.choice(stores, n),
    'date': [str(d.date()) for d in pd.date_range('2024-01-01', periods=n, freq='D')[:n]],
    'product': products,
    'category': categories,
    'customer_id': [f'CUST{np.random.randint(100, 999):03d}' for _ in range(n)],
    'customer_type': np.random.choice(['Member', 'Walk-in'], n, p=[0.55, 0.45]),
    'price': [float(p) for p in prices],
    'quantity': np.random.randint(1, 8, n),
    'discount_pct': np.random.choice([0, 5, 10, 15, 20, 25], n, p=[0.25, 0.25, 0.2, 0.15, 0.1, 0.05]),
    'payment_method': np.random.choice(['UPI', 'Credit Card', 'Debit Card', 'Cash', 'EMI'], n,
                                        p=[0.40, 0.20, 0.20, 0.12, 0.08]),
    'city': [cities[stores.index(s)] for s in np.random.choice(stores, n)],
    'rating': np.where(np.random.rand(n) < 0.30, np.nan, np.random.choice([1,2,3,4,5], n, p=[0.03,0.07,0.15,0.40,0.35])),
}

df = pd.DataFrame(data)

#  Introduce intentional data quality issues 
# Issue 1: Duplicate some rows
dup_indices = np.random.choice(n, 12, replace=False)
df_with_dups = pd.concat([df, df.iloc[dup_indices]], ignore_index=True)

# Issue 2: Make some prices negative/zero
bad_price_idx = np.random.choice(len(df_with_dups), 5, replace=False)
df_with_dups.loc[bad_price_idx, 'price'] = np.random.choice([-999, 0, -5000], 5)

# Issue 3: Mixed date formats
mixed_date_idx = np.random.choice(len(df_with_dups), 20, replace=False)
for idx in mixed_date_idx:
    orig_date = pd.to_datetime(df_with_dups.loc[idx, 'date'])
    df_with_dups.loc[idx, 'date'] = orig_date.strftime('%d-%m-%Y')

# Issue 4: Missing values
missing_store_idx = np.random.choice(len(df_with_dups), 8, replace=False)
df_with_dups.loc[missing_store_idx, 'store'] = np.nan
df_with_dups.loc[missing_store_idx, 'city'] = np.nan

missing_customer_type_idx = np.random.choice(len(df_with_dups), 15, replace=False)
df_with_dups.loc[missing_customer_type_idx, 'customer_type'] = np.nan

# Issue 5: Inconsistent text case
inconsistent_idx = np.random.choice(len(df_with_dups), 25, replace=False)
df_with_dups.loc[inconsistent_idx[:12], 'category'] = df_with_dups.loc[inconsistent_idx[:12], 'category'].str.upper()
df_with_dups.loc[inconsistent_idx[12:], 'product'] = df_with_dups.loc[inconsistent_idx[12:], 'product'].str.lower()

# Save
Path('data').mkdir(exist_ok=True)
df_with_dups.to_csv('data/supermart_raw.csv', index=False)

print(f" Dataset generated: {len(df_with_dups)} rows  {len(df_with_dups.columns)} columns")
print(f"   Saved to: data/supermart_raw.csv")
print(f"\n   Data quality issues introduced:")
print(f"   - {12} duplicate rows")
print(f"   - {5} invalid price values")
print(f"   - {20} mixed date formats")
print(f"   - Missing values: store({8}), city({8}), customer_type({15}), rating(~30%)")
print(f"   - {25} inconsistent text case values")
print(f"\nNow run: python supermart_analysis.py")
