"""
MINI PROJECT: RETAIL ANALYTICS
Analyze sales data to identify trends and segments.
"""
import pandas as pd

# 1. Load sample dataset
data = {
    'date': pd.to_date_range('2023-01-01', periods=10, freq='M'),
    'sales': [1000, 1200, 1500, 1100, 1300, 1600, 1800, 1400, 1700, 1900],
    'customers': [50, 55, 60, 45, 50, 65, 70, 55, 60, 75]
}
df = pd.DataFrame(data)

# 2. Calculate AOV (Average Order Value)
df['AOV'] = df['sales'] / df['customers']
print("Monthly Performance Metrics:")
print(df[['date', 'sales', 'AOV']])

# 3. Identify Peak Month
peak_month = df.loc[df['sales'].idxmax(), 'date']
print(f"\nPeak Sales Month: {peak_month}")
