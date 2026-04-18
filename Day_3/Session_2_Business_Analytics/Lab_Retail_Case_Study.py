import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- PREPARATION ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TXN_DATA = os.path.join(ROOT_DIR, "session3_transactions_clean.csv")

# Load Data
df = pd.read_csv(TXN_DATA)
df['date'] = pd.to_datetime(df['date'])

print("Starting SuperMart Business Analytics Lab")
print("----------------------------------\n")

# --- TASK 1: Executive Summary (KPIs) ---
total_revenue = df['amount'].sum()
total_txns = len(df)
aov = total_revenue / total_txns
avg_basket = df['items_count'].mean()

print("EXECUTIVE SUMMARY (ALL STORES)")
print(f"Total Revenue:      Rs.{total_revenue:,.2f}")
print(f"Total Transactions: {total_txns}")
print(f"Average Order Val:  Rs.{aov:,.2f}")
print(f"Avg Items / Order:  {avg_basket:.2f}")
print("\n")

# --- TASK 2: Performance by Category ---
category_perf = df.groupby('category').agg({
    'amount': 'sum',
    'txn_id': 'count'
}).rename(columns={'txn_id': 'order_count', 'amount': 'revenue'})

category_perf['aov'] = category_perf['revenue'] / category_perf['order_count']
print("CATEGORY PERFORMANCE")
print(category_perf.sort_values(by='revenue', ascending=False))
print("\n")

# --- TASK 3: Sales Trend (Monthly) ---
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July']
df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)

monthly_sales = df.groupby('month')['amount'].sum()
print("MONTHLY SALES TREND")
print(monthly_sales)
print("\n")

# --- TASK 4: Customer Insights ---
member_segment = df.groupby('member').agg({
    'amount': 'mean',
    'items_count': 'mean',
    'txn_id': 'count'
}).rename(columns={'amount': 'avg_spend', 'items_count': 'avg_items', 'txn_id': 'order_count'})

print("MEMBER VS NON-MEMBER SEGMENTATION")
print(member_segment)
print("\n")

# --- TASK 5: Visualization for Presentation ---
plt.figure(figsize=(15, 10))

plt.subplot(2, 2, 1)
sns.lineplot(x=monthly_sales.index, y=monthly_sales.values, marker='o', color='purple')
plt.title('Monthly Revenue Trend')
plt.xticks(rotation=45)
plt.ylabel('Revenue (Rs.)')

plt.subplot(2, 2, 2)
sns.barplot(x=category_perf.index, y=category_perf['revenue'], palette='viridis')
plt.title('Revenue by Category')

plt.subplot(2, 2, 3)
df['payment_method'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette('pastel'))
plt.title('Payment Method Distribution')

plt.subplot(2, 2, 4)
sns.boxplot(x='member', y='amount', data=df)
plt.title('Transaction Amount: Member vs Non-Member')

plt.tight_layout()
plt.savefig('retail_case_study_output.png')
print("Dashboard saved as 'retail_case_study_output.png'")

print("\nBusiness Analytics Lab Complete!")
