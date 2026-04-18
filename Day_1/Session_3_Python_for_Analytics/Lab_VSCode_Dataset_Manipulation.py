"""
Day 1 | Session 3 Lab: Python for Data Analytics (VS Code Version)
===================================================================
Course: Data Analytics Complete | Day: 1 | Session: 3

Dataset: Retail Store Performance Dataset  NumPy + Pandas hands-on manipulation

Install dependencies: pip install pandas numpy matplotlib seaborn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

print("=" * 65)
print("DAY 1 | SESSION 3 LAB: Python for Data Analytics")
print("Hands-On Dataset Manipulation: NumPy + Pandas")
print("=" * 65)

# 
# PART A: NumPy in Action
# 
print("\n" + "" * 50)
print("PART A: NumPy  Store Sales Analysis")
print("" * 50)

# Monthly sales for 4 stores over 12 months (2024)
# Rows = stores (A, B, C, D), Columns = months (Jan-Dec)
monthly_sales = np.array([
    [1200, 1350, 1100, 1500, 1800, 1650, 2100, 2300, 2000, 2500, 2900, 3200],  # Store A
    [850,  920,  880,  1050, 1200, 1100, 1400, 1600, 1450, 1800, 2100, 2400],  # Store B
    [1500, 1600, 1400, 1700, 2000, 1900, 2300, 2500, 2200, 2800, 3200, 3600],  # Store C
    [600,  650,  580,  720,  850,  800,  1000, 1100, 950,  1200, 1400, 1600],  # Store D
])

stores = ['Store A', 'Store B', 'Store C', 'Store D']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

print(f"\nArray shape: {monthly_sales.shape}  (stores  months)")
print(f"Data type: {monthly_sales.dtype}")

#  NumPy Operations 
print("\n STORE PERFORMANCE (using NumPy axis operations):")
print("" * 40)

# Annual total per store (sum across columns, axis=1)
annual_totals = monthly_sales.sum(axis=1)
# Monthly average per store (mean across columns, axis=1)
store_avg = monthly_sales.mean(axis=1)
# Best month per store
best_month_idx = monthly_sales.argmax(axis=1)

for i, store in enumerate(stores):
    print(f"  {store}: Annual={annual_totals[i]:,} | "
          f"Avg={store_avg[i]:.0f} | "
          f"Best Month={months[best_month_idx[i]]}")

print("\n MONTHLY PERFORMANCE (across all stores):")
print("" * 40)
monthly_totals = monthly_sales.sum(axis=0)
peak_month_idx = monthly_totals.argmax()
print(f"  Peak Month: {months[peak_month_idx]} (Total: {monthly_totals[peak_month_idx]:,})")
print(f"  Slowest Month: {months[monthly_totals.argmin()]} (Total: {monthly_totals.min():,})")

#  Boolean Indexing 
target = 2000
above_target = monthly_sales > target
print(f"\n Months above {target:,} target per store:")
for i, store in enumerate(stores):
    count = above_target[i].sum()
    print(f"  {store}: {count}/12 months exceeded target")

#  Quarter-wise Analysis using Reshaping 
# Reshape to (stores, quarters, months_per_quarter)
quarterly = monthly_sales.reshape(4, 4, 3)
quarterly_totals = quarterly.sum(axis=2)  # Sum within each quarter

print("\n QUARTERLY TOTALS:")
print(f"{'Store':<12} {'Q1':>8} {'Q2':>8} {'Q3':>8} {'Q4':>8}")
print("" * 50)
for i, store in enumerate(stores):
    q = quarterly_totals[i]
    print(f"{store:<12} {''+str(q[0]):>8} {''+str(q[1]):>8} {''+str(q[2]):>8} {''+str(q[3]):>8}")

#  Growth Rate Calculation 
# Month-over-month growth (percentage change)
mom_growth = np.diff(monthly_sales, axis=1) / monthly_sales[:, :-1] * 100
print("\n Average Month-over-Month Growth:")
for i, store in enumerate(stores):
    avg_growth = mom_growth[i].mean()
    print(f"  {store}: {avg_growth:+.1f}% average monthly growth")

# 
# PART B: Pandas  Deep Analysis
# 
print("\n" + "" * 50)
print("PART B: Pandas  Customer Transaction Analysis")
print("" * 50)

# Convert NumPy to a Pandas DataFrame
sales_df = pd.DataFrame(monthly_sales, index=stores, columns=months)
print("\nSales DataFrame:")
print(sales_df)

#  Create a detailed transactions DataFrame 
np.random.seed(2024)
n = 200

transactions = pd.DataFrame({
    'txn_id':     [f'T{i:04d}' for i in range(1, n+1)],
    'store':      np.random.choice(stores, n),
    'date':       pd.date_range('2024-01-01', periods=n, freq='D')[:n],
    'category':   np.random.choice(['Electronics', 'Clothing', 'Food', 'Books', 'Sports'], n),
    'customer_age': np.random.choice([18, 19, 20, 21, 22, 23, 24, 25, 28, 30, 32, 35, 40, 45, 50], n),
    'amount':     np.round(np.random.lognormal(mean=8.5, sigma=0.8, size=n), 2),
    'items_count': np.random.randint(1, 10, n),
    'payment_method': np.random.choice(['UPI', 'Credit Card', 'Debit Card', 'Cash'], n,
                                        p=[0.45, 0.25, 0.20, 0.10]),
    'member':     np.random.choice([True, False], n, p=[0.6, 0.4]),
})

# Add derived columns
transactions['month'] = transactions['date'].dt.month_name()
transactions['quarter'] = 'Q' + transactions['date'].dt.quarter.astype(str)
transactions['avg_item_value'] = (transactions['amount'] / transactions['items_count']).round(2)
transactions['member_discount'] = np.where(transactions['member'], transactions['amount'] * 0.05, 0)

print(f"\nTransactions Dataset: {transactions.shape}")
print(transactions.head(5).to_string(index=False))

#  Multi-level Analysis 
print("\n" + "" * 40)
print("ANALYSIS 1: Store-Category Performance")
print("" * 40)
store_cat = transactions.groupby(['store', 'category']).agg(
    transactions=('txn_id', 'count'),
    total_revenue=('amount', 'sum'),
    avg_transaction=('amount', 'mean')
).round(2)
print(store_cat.head(10).to_string())

print("\n" + "" * 40)
print("ANALYSIS 2: Payment Method Trends")
print("" * 40)
payment_stats = transactions.groupby('payment_method').agg(
    count=('txn_id', 'count'),
    total_amount=('amount', 'sum'),
    avg_basket=('amount', 'mean'),
    avg_items=('items_count', 'mean')
).round(2).sort_values('total_amount', ascending=False)
print(payment_stats.to_string())

print("\n" + "" * 40)
print("ANALYSIS 3: Member vs Non-Member")
print("" * 40)
member_analysis = transactions.groupby('member').agg(
    count=('txn_id', 'count'),
    avg_spend=('amount', 'mean'),
    total_spend=('amount', 'sum'),
    avg_items=('items_count', 'mean')
).round(2)
member_analysis.index = ['Non-Member', 'Member']
print(member_analysis.to_string())

print("\n" + "" * 40)
print("ANALYSIS 4: Filtering  High Value Transactions")
print("" * 40)
# High-value transactions: > 75th percentile AND member
q75 = transactions['amount'].quantile(0.75)
high_value = transactions[(transactions['amount'] > q75) & (transactions['member'] == True)]
print(f"75th percentile threshold: {q75:.2f}")
print(f"High-value member transactions: {len(high_value)}")
print(f"Their average basket: {high_value['amount'].mean():.2f}")

# Store ranking by revenue  find the best store directly
store_revenue = transactions.groupby('store')['amount'].sum()
best_store = store_revenue.idxmax()
print(f"\n Best performing store: {best_store} ({store_revenue[best_store]:,.0f})")

# 
# PART C: VISUALIZATION DASHBOARD
# 
print("\n" + "" * 50)
print("PART C: Creating Analysis Dashboard")
print("" * 50)

fig = plt.figure(figsize=(16, 12))
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.4, wspace=0.4)
fig.suptitle('Day 1 Session 3 Lab: Retail Analytics Dashboard', fontsize=16, fontweight='bold')

# Chart 1: Monthly sales trend (all stores)
ax1 = fig.add_subplot(gs[0, :])
for store, row in sales_df.iterrows():
    ax1.plot(months, row.values, marker='o', linewidth=2, markersize=5, label=store)
ax1.set_title('Monthly Sales Trend by Store (2024)')
ax1.set_ylabel('Sales ()')
ax1.legend()
ax1.grid(alpha=0.3)

# Chart 2: Annual totals bar
ax2 = fig.add_subplot(gs[1, 0])
colors_bar = ['#2196F3', '#4CAF50', '#FF9800', '#F44336']
ax2.bar(stores, annual_totals, color=colors_bar, alpha=0.8)
ax2.set_title('Annual Total Revenue')
ax2.set_ylabel('Revenue ()')
ax2.grid(axis='y', alpha=0.3)
ax2.tick_params(axis='x', rotation=15)

# Chart 3: Category distribution
ax3 = fig.add_subplot(gs[1, 1])
cat_counts = transactions['category'].value_counts()
ax3.pie(cat_counts, labels=cat_counts.index, autopct='%1.0f%%',
        colors=['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'])
ax3.set_title('Transactions by Category')

# Chart 4: Payment method distribution
ax4 = fig.add_subplot(gs[1, 2])
pay_counts = transactions['payment_method'].value_counts()
ax4.bar(pay_counts.index, pay_counts.values, color='teal', alpha=0.8)
ax4.set_title('Payment Method Usage')
ax4.set_ylabel('Count')
ax4.tick_params(axis='x', rotation=15)
ax4.grid(axis='y', alpha=0.3)

# Chart 5: Amount distribution
ax5 = fig.add_subplot(gs[2, :2])
ax5.hist(transactions['amount'], bins=30, color='steelblue', alpha=0.7, edgecolor='black')
ax5.axvline(transactions['amount'].mean(), color='red', linestyle='--', label=f"Mean: {transactions['amount'].mean():.0f}")
ax5.axvline(transactions['amount'].median(), color='green', linestyle='--', label=f"Median: {transactions['amount'].median():.0f}")
ax5.set_title('Transaction Amount Distribution')
ax5.set_xlabel('Amount ()')
ax5.set_ylabel('Frequency')
ax5.legend()
ax5.grid(alpha=0.3)

# Chart 6: Member vs Non-member
ax6 = fig.add_subplot(gs[2, 2])
member_avg = transactions.groupby('member')['amount'].mean()
ax6.bar(['Non-Member', 'Member'], member_avg.values, color=['#FF6B6B', '#4ECDC4'], alpha=0.8)
ax6.set_title('Avg Spend: Member vs Non-Member')
ax6.set_ylabel('Avg Transaction ()')
ax6.grid(axis='y', alpha=0.3)
for i, v in enumerate(member_avg.values):
    ax6.text(i, v + 50, f'{v:.0f}', ha='center', fontweight='bold')

plt.savefig('session3_lab_dashboard.png', dpi=100, bbox_inches='tight')
plt.show()
print(" Dashboard saved as 'session3_lab_dashboard.png'")

#  Save Final Analysis 
transactions.to_csv('session3_transactions_clean.csv', index=False)
print(" Transaction data saved as 'session3_transactions_clean.csv'")

print("\n" + "=" * 65)
print(" Session 3 Lab Complete!")
print("   You've practiced: NumPy arrays, Pandas DataFrames,")
print("   filtering, groupby, aggregation, and visualization!")
print("=" * 65)
