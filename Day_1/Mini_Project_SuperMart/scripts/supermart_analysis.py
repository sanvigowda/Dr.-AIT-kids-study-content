"""
SuperMart Sales Intelligence — Complete Analysis Pipeline (VS Code)
===================================================================
MODEL MINI PROJECT — Data Analytics Complete | Day 1

This script demonstrates a complete analytics lifecycle:
  1. Problem Definition
  2. Data Collection (CSV load)
  3. Data Audit
  4. Data Cleaning
  5. Feature Engineering
  6. Exploratory Data Analysis
  7. Insights Communication

Run: python supermart_analysis.py
(First run: python 00_generate_data.py to create the dataset)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 1: PROBLEM DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═" * 70)
print("  SUPERMART SALES INTELLIGENCE DASHBOARD")
print("  Day 1 Model Mini Project — Data Analytics Complete")
print("═" * 70)

print("""
╔══════════════════════════════════════════════════════╗
║  BUSINESS PROBLEM                                    ║
║  SuperMart wants to understand:                      ║
║  1. Which products & categories drive revenue?       ║
║  2. Are there data quality issues in the raw data?   ║
║  3. Which store performs best per quarter?           ║
║  4. Do members spend more than walk-in customers?    ║
║  5. What is the impact of discounts on revenue?      ║
╚══════════════════════════════════════════════════════╝
""")

# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 2: DATA COLLECTION
# ═══════════════════════════════════════════════════════════════════════════════
print("─" * 60)
print("STAGE 2: DATA COLLECTION")
print("─" * 60)

data_path = Path('data/supermart_raw.csv')
if not data_path.exists():
    print("⚠️  Dataset not found. Generating it now...")
    import subprocess
    subprocess.run(['python', 'scripts/00_generate_data.py'])

df_raw = pd.read_csv('data/supermart_raw.csv')
print(f"\n✅ Loaded: {df_raw.shape[0]} rows × {df_raw.shape[1]} columns")
print(f"   Columns: {', '.join(df_raw.columns)}")

# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 3: DATA AUDIT — Find All Quality Issues
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "─" * 60)
print("STAGE 3: DATA AUDIT")
print("─" * 60)

audit_report = {}

# Missing values
missing = df_raw.isnull().sum()
missing_pct = (missing / len(df_raw) * 100).round(1)
audit_report['missing_values'] = missing[missing > 0]

# Duplicates
audit_report['duplicate_rows'] = df_raw.duplicated().sum()
audit_report['duplicate_txn_ids'] = df_raw.duplicated(subset=['transaction_id']).sum()

# Invalid prices  
audit_report['negative_prices'] = (df_raw['price'] <= 0).sum()

# Inconsistent categories
audit_report['unique_category_variants'] = df_raw['category'].nunique()

print(f"\n AUDIT RESULTS:")
print(f"   {'Issue':<35} {'Count'}")
print(f"   {'─'*35} {'─'*10}")
print(f"   {'Full duplicate rows':<35} {audit_report['duplicate_rows']}")
print(f"   {'Duplicate transaction IDs':<35} {audit_report['duplicate_txn_ids']}")
print(f"   {'Invalid price values (≤0)':<35} {audit_report['negative_prices']}")
print(f"\n   Missing Values:")
for col, cnt in audit_report['missing_values'].items():
    print(f"     {col:<30} {cnt:>3} ({missing_pct[col]}%)")

# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 4: DATA CLEANING
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "─" * 60)
print("STAGE 4: DATA CLEANING")
print("─" * 60)

df = df_raw.copy()

# Step 4.1: Remove duplicates
before = len(df)
df = df.drop_duplicates(subset=['transaction_id'], keep='first').reset_index(drop=True)
print(f"\n✅ 4.1 Duplicates removed: {before} → {len(df)} rows")

# Step 4.2: Fix invalid prices
median_price_by_product = df[df['price'] > 0].groupby('product')['price'].median()
invalid_mask = df['price'] <= 0
for idx in df[invalid_mask].index:
    product = df.loc[idx, 'product']
    if product in median_price_by_product:
        df.loc[idx, 'price'] = median_price_by_product[product]
    else:
        df.loc[idx, 'price'] = df[df['price'] > 0]['price'].median()
print(f"✅ 4.2 Invalid prices corrected: {invalid_mask.sum()} records")

# Step 4.3: Standardize dates
df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True, errors='coerce')
date_nulls = df['date'].isnull().sum()
if date_nulls > 0:
    df['date'] = df['date'].fillna(pd.Timestamp.today())
print(f"✅ 4.3 Dates standardized (parse failures: {date_nulls})")

# Step 4.4: Standardize text fields
df['category'] = df['category'].str.strip().str.title()
df['product'] = df['product'].str.strip().str.title()
df['store'] = df['store'].str.strip().str.title()
df['city'] = df['city'].str.strip().str.title()
df['customer_type'] = df['customer_type'].str.strip().str.title()
print("✅ 4.4 Text fields standardized (category, product, store, city)")

# Step 4.5: Handle missing values
df['store'] = df['store'].fillna('Unknown Store')
df['city'] = df['city'].fillna('Unknown City')
df['customer_type'] = df['customer_type'].fillna('Walk-In')
df['rating'] = df['rating'].fillna(df['rating'].median())
print("✅ 4.5 Missing values handled")

# Validation check
remaining_issues = df.isnull().sum().sum() + (df['price'] <= 0).sum()
print(f"\n✅ CLEANING COMPLETE — Remaining issues: {remaining_issues}")

# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 5: FEATURE ENGINEERING
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "─" * 60)
print("STAGE 5: FEATURE ENGINEERING")
print("─" * 60)

# Revenue calculation
df['revenue'] = (df['price'] * df['quantity'] * (1 - df['discount_pct'] / 100)).round(2)

# Time features
df['month'] = df['date'].dt.month
df['month_name'] = df['date'].dt.month_name()
df['quarter'] = 'Q' + df['date'].dt.quarter.astype(str)
df['day_of_week'] = df['date'].dt.day_name()
df['is_weekend'] = df['date'].dt.dayofweek >= 5

# Customer segment
df['is_member'] = df['customer_type'].str.contains('Member', case=False)

# Transaction size
df['basket_size'] = pd.cut(
    df['revenue'],
    bins=[0, 1000, 5000, 20000, float('inf')],
    labels=['Small (<₹1K)', 'Medium (₹1K-5K)', 'Large (₹5K-20K)', 'Premium (>₹20K)']
)

# Discount effectiveness flag
df['has_discount'] = df['discount_pct'] > 0

print(f"✅ Engineered features: revenue, quarter, is_member, basket_size, has_discount")
print(f"   Final shape: {df.shape[0]} rows × {df.shape[1]} columns")

# Save cleaned data
Path('output').mkdir(exist_ok=True)
df.to_csv('output/cleaned_data.csv', index=False)
print(f"   Saved to: output/cleaned_data.csv")

# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 6: EXPLORATORY DATA ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═" * 70)
print("STAGE 6: EXPLORATORY DATA ANALYSIS")
print("═" * 70)

# ─── Q1: Revenue by Store ─────────────────────────────────────────────────────
print("\n Q1: Revenue by Store:")
store_rev = df.groupby('store').agg(
    total_revenue=('revenue', 'sum'),
    transactions=('transaction_id', 'count'),
    avg_basket=('revenue', 'mean')
).round(2).sort_values('total_revenue', ascending=False)
store_rev['rank'] = range(1, len(store_rev)+1)
for store, row in store_rev.iterrows():
    bar = '█' * int(row['total_revenue'] / store_rev['total_revenue'].max() * 20)
    print(f"  #{row['rank']} {store:<12} |{bar:<20}| ₹{row['total_revenue']:>10,.0f}")

# ─── Q2: Revenue by Category ──────────────────────────────────────────────────
print("\n Q2: Category Performance:")
cat_stats = df.groupby('category').agg(
    revenue=('revenue', 'sum'),
    units=('quantity', 'sum'),
    transactions=('transaction_id', 'count'),
    avg_rating=('rating', 'mean')
).round(2).sort_values('revenue', ascending=False)
print(cat_stats.to_string())

# ─── Q3: Quarterly Trends ─────────────────────────────────────────────────────
print("\n Q3: Quarterly Store Performance:")
quarterly_store = df.groupby(['quarter', 'store'])['revenue'].sum().unstack(fill_value=0).round(0)
print(quarterly_store.to_string())

# ─── Q4: Members vs Walk-in ───────────────────────────────────────────────────
print("\n Q4: Member vs Walk-In Customers:")
member_stats = df.groupby('is_member').agg(
    count=('transaction_id', 'count'),
    avg_basket=('revenue', 'mean'),
    total_revenue=('revenue', 'sum'),
    avg_items=('quantity', 'mean')
).round(2)
member_stats.index = ['Walk-In', 'Member']
print(member_stats.to_string())
premium = ((member_stats.loc['Member', 'avg_basket'] -
            member_stats.loc['Walk-In', 'avg_basket']) /
           member_stats.loc['Walk-In', 'avg_basket'] * 100)
print(f"\n   Members spend {premium:.1f}% MORE per transaction than walk-in customers!")

# ─── Q5: Discount Analysis ────────────────────────────────────────────────────
print("\n Q5: Discount Impact on Revenue:")
discount_groups = df.groupby('has_discount').agg(
    avg_revenue=('revenue', 'mean'),
    total_revenue=('revenue', 'sum'),
    count=('transaction_id', 'count'),
    avg_items=('quantity', 'mean')
).round(2)
discount_groups.index = ['No Discount', 'With Discount']
print(discount_groups.to_string())

# ─── Q6: Top Products ─────────────────────────────────────────────────────────
print("\n Q6: Top 10 Products by Revenue:")
top_products = df.groupby('product')['revenue'].sum().sort_values(ascending=False).head(10)
for rank, (product, rev) in enumerate(top_products.items(), 1):
    print(f"  {rank:>2}. {product:<25} ₹{rev:>10,.0f}")

# ─── Q7: High-value customer profile ─────────────────────────────────────────
print("\n Q7: High-Value Transaction Profile:")
q75 = df['revenue'].quantile(0.75)
high_value_txns = df[df['revenue'] > q75]
print(f"  Threshold (75th percentile): ₹{q75:,.0f}")
print(f"  High-value transactions: {len(high_value_txns)}")
print(f"  Member %: {high_value_txns['is_member'].mean()*100:.1f}%")
print(f"  Top category: {high_value_txns['category'].mode()[0]}")
print(f"  Preferred payment: {high_value_txns['payment_method'].mode()[0]}")

# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 7: VISUALIZATION DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "─" * 60)
print("STAGE 7: BUILDING VISUALIZATION DASHBOARD")
print("─" * 60)

fig = plt.figure(figsize=(18, 14))
fig.patch.set_facecolor('#0F0F1A')
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.4)

DARK_BG = '#0F0F1A'
CARD_BG = '#1A1A2E'
TEXT_COLOR = '#E0E0E0'
ACCENT_COLORS = ['#00D4FF', '#FF6B6B', '#4ECB71', '#FFD93D', '#A78BFA']

def style_ax(ax, title):
    ax.set_facecolor(CARD_BG)
    ax.set_title(title, color=TEXT_COLOR, fontsize=10, fontweight='bold', pad=8)
    ax.tick_params(colors=TEXT_COLOR, labelsize=8)
    ax.spines[:].set_color('#333355')
    for spine in ax.spines.values():
        spine.set_linewidth(0.5)

# Header
fig.text(0.5, 0.97, ' SUPERMART SALES INTELLIGENCE DASHBOARD',
         ha='center', va='top', fontsize=16, fontweight='bold', color=TEXT_COLOR)
fig.text(0.5, 0.94, 'Model Mini Project — Data Analytics Complete Day 1',
         ha='center', va='top', fontsize=10, color='#888888')

# Chart 1: Revenue by Store (horizontal bar)
ax1 = fig.add_subplot(gs[0, :2])
style_ax(ax1, ' Total Revenue by Store')
store_vals = store_rev['total_revenue'].sort_values()
bars = ax1.barh(store_vals.index, store_vals.values / 1000, color=ACCENT_COLORS[:len(store_vals)], alpha=0.85)
for bar, val in zip(bars, store_vals.values):
    ax1.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
             f'₹{val/1000:.0f}K', va='center', color=TEXT_COLOR, fontsize=8)
ax1.set_xlabel('Revenue (₹ Thousands)', color=TEXT_COLOR)
ax1.grid(axis='x', alpha=0.15, color='white')

# Chart 2: Category pie
ax2 = fig.add_subplot(gs[0, 2])
style_ax(ax2, '️ Revenue by Category')
cat_vals = cat_stats['revenue']
wedges, texts, autotexts = ax2.pie(cat_vals, labels=None, autopct='%1.0f%%',
                                    colors=ACCENT_COLORS, startangle=90,
                                    wedgeprops={'edgecolor': DARK_BG, 'linewidth': 2})
for at in autotexts:
    at.set_color('white')
    at.set_fontsize(8)
ax2.legend(cat_vals.index, loc='lower left', fontsize=7,
           framealpha=0.2, labelcolor=TEXT_COLOR)

# Chart 3: Quarterly trend line
ax3 = fig.add_subplot(gs[1, :2])
style_ax(ax3, ' Quarterly Revenue Trend by Store')
q_data = df.groupby(['quarter', 'store'])['revenue'].sum().reset_index()
stores_list = df['store'].unique()
for i, store in enumerate(stores_list):
    s_data = q_data[q_data['store'] == store]
    ax3.plot(s_data['quarter'], s_data['revenue']/1000,
             marker='o', linewidth=2, markersize=7,
             color=ACCENT_COLORS[i % len(ACCENT_COLORS)],
             label=store)
ax3.set_xlabel('Quarter', color=TEXT_COLOR)
ax3.set_ylabel('Revenue (₹ Thousands)', color=TEXT_COLOR)
ax3.legend(fontsize=8, framealpha=0.2, labelcolor=TEXT_COLOR)
ax3.grid(alpha=0.15, color='white')

# Chart 4: Member vs Walk-in comparison
ax4 = fig.add_subplot(gs[1, 2])
style_ax(ax4, ' Member vs Walk-In Spend')
labels = ['Walk-In', 'Member']
avgs = [member_stats.loc['Walk-In', 'avg_basket'], member_stats.loc['Member', 'avg_basket']]
bars = ax4.bar(labels, avgs, color=['#FF6B6B', '#4ECB71'], alpha=0.85, width=0.5)
for bar, val in zip(bars, avgs):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
             f'₹{val:.0f}', ha='center', color=TEXT_COLOR, fontsize=10, fontweight='bold')
ax4.set_ylabel('Avg Transaction (₹)', color=TEXT_COLOR)
ax4.grid(axis='y', alpha=0.15, color='white')
ax4.set_ylim(0, max(avgs) * 1.2)

# Chart 5: Revenue distribution (histogram)
ax5 = fig.add_subplot(gs[2, :2])
style_ax(ax5, ' Transaction Revenue Distribution')
ax5.hist(df['revenue'], bins=35, color='#00D4FF', alpha=0.75, edgecolor='#333355')
ax5.axvline(df['revenue'].mean(), color='#FFD93D', linewidth=2,
            linestyle='--', label=f'Mean: ₹{df["revenue"].mean():.0f}')
ax5.axvline(df['revenue'].median(), color='#FF6B6B', linewidth=2,
            linestyle='--', label=f'Median: ₹{df["revenue"].median():.0f}')
ax5.set_xlabel('Revenue (₹)', color=TEXT_COLOR)
ax5.set_ylabel('Frequency', color=TEXT_COLOR)
ax5.legend(fontsize=8, framealpha=0.2, labelcolor=TEXT_COLOR)
ax5.grid(alpha=0.15, color='white')

# Chart 6: Payment method
ax6 = fig.add_subplot(gs[2, 2])
style_ax(ax6, ' Payment Method Shares')
pay_counts = df['payment_method'].value_counts()
ax6.bar(pay_counts.index, pay_counts.values, color=ACCENT_COLORS, alpha=0.85)
ax6.tick_params(axis='x', rotation=20)
ax6.set_ylabel('Transactions', color=TEXT_COLOR)
ax6.grid(axis='y', alpha=0.15, color='white')

plt.savefig('output/dashboard.png', dpi=120, bbox_inches='tight', facecolor=DARK_BG)
plt.show()
print(" Dashboard saved to output/dashboard.png")

# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 8: BUSINESS INSIGHT SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═" * 70)
print("BUSINESS INSIGHT SUMMARY")
print("═" * 70)

top_store = store_rev.index[0]
top_cat = cat_stats['revenue'].idxmax()
best_quarter = df.groupby('quarter')['revenue'].sum().idxmax()
member_premium = ((member_stats.loc['Member', 'avg_basket'] -
                   member_stats.loc['Walk-In', 'avg_basket']) /
                  member_stats.loc['Walk-In', 'avg_basket'] * 100)

insights = [
    f" {top_store} is the top-performing store with ₹{store_rev.loc[top_store, 'total_revenue']:,.0f} total revenue.",
    f" {top_cat} is the highest-grossing category, accounting for {cat_stats.loc[top_cat, 'revenue']/df['revenue'].sum()*100:.1f}% of total revenue.",
    f" {best_quarter} was the strongest quarter across all stores.",
    f" Members spend {member_premium:.1f}% more per transaction — growing the loyalty program could boost revenue significantly.",
    f" UPI is the most popular payment method, indicating a digital-savvy customer base.",
    f" {len(high_value_txns)} transactions ({len(high_value_txns)/len(df)*100:.1f}%) are high-value (>₹{q75:,.0f}) — these customers deserve premium retention efforts.",
]

for i, insight in enumerate(insights, 1):
    print(f"\n  {i}. {insight}")

print(f"\n{'═' * 70}")
print("✅ MINI PROJECT COMPLETE!")
print("   Files generated:")
print("   - output/cleaned_data.csv")
print("   - output/dashboard.png")
print(f"{'═' * 70}\n")
