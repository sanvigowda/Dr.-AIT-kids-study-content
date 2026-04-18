"""
Day 1 | Session 1 Lab: Dataset Exploration (VS Code Version)
=============================================================
Course: Data Analytics Complete | Day: 1 | Session: 1

Run this file in VS Code with Python extension installed.
Install dependencies:
    pip install pandas numpy matplotlib seaborn

Dataset: Country-level Happiness & Economic Data (World Happiness Report inspired)
"""

#  Imports 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:.2f}'.format)

#  1. CREATE DATASET 
print("=" * 60)
print("DAY 1 | SESSION 1 LAB: Dataset Exploration")
print("=" * 60)

data = {
    'country': ['Finland', 'Denmark', 'Iceland', 'Israel', 'Netherlands',
                 'Sweden', 'Norway', 'Switzerland', 'Australia', 'New Zealand',
                 'Canada', 'USA', 'UK', 'Germany', 'France',
                 'Japan', 'South Korea', 'Brazil', 'India', 'China',
                 'Mexico', 'Russia', 'Nigeria', 'Kenya', 'Ethiopia'],
    'region': ['Europe', 'Europe', 'Europe', 'Middle East', 'Europe',
                'Europe', 'Europe', 'Europe', 'Oceania', 'Oceania',
                'North America', 'North America', 'Europe', 'Europe', 'Europe',
                'Asia', 'Asia', 'South America', 'Asia', 'Asia',
                'North America', 'Europe', 'Africa', 'Africa', 'Africa'],
    'happiness_score': [7.74, 7.58, 7.53, 7.47, 7.43,
                         7.40, 7.32, 7.24, 7.10, 7.03,
                         6.90, 6.89, 6.80, 6.75, 6.69,
                         6.11, 5.95, 6.00, 4.04, 5.82,
                         6.33, 5.66, 4.48, 4.52, 3.56],
    'gdp_per_capita': [49000, 62000, 55000, 45000, 57000,
                        54000, 82000, 78000, 53000, 47000,
                        52000, 65000, 45000, 50000, 43000,
                        40000, 31000, 9000, 2400, 12000,
                        10000, 12000, 2200, 1900, 950],
    'social_support': [0.95, 0.96, 0.97, 0.91, 0.94,
                        0.93, 0.95, 0.94, 0.93, 0.94,
                        0.92, 0.90, 0.90, 0.90, 0.88,
                        0.88, 0.83, 0.82, 0.69, 0.83,
                        0.82, 0.81, 0.73, 0.72, 0.66],
    'life_expectancy': [72, 72, 73, 73, 72,
                         72, 73, 74, 73, 73,
                         72, 68, 72, 72, 73,
                         74, 73, 65, 60, 68,
                         66, 63, 54, 58, 52],
}

df = pd.DataFrame(data)
print(f"\n Dataset loaded: {df.shape[0]} countries  {df.shape[1]} variables")

#  2. EXPLORE THE DATA 
print("\n" + "" * 40)
print("FIRST 5 ROWS:")
print("" * 40)
print(df.head().to_string())

print("\n" + "" * 40)
print("DATA TYPES:")
print("" * 40)
print(df.dtypes)

print("\n" + "" * 40)
print("DESCRIPTIVE STATISTICS:")
print("" * 40)
print(df.describe().round(2).to_string())

print("\n" + "" * 40)
print("REGION DISTRIBUTION:")
print("" * 40)
print(df['region'].value_counts())

#  3. DESCRIPTIVE ANALYTICS 
print("\n" + "" * 40)
print("HAPPINESS BY REGION:")
print("" * 40)
regional_stats = df.groupby('region').agg(
    avg_happiness=('happiness_score', 'mean'),
    avg_gdp=('gdp_per_capita', 'mean'),
    country_count=('country', 'count')
).round(2).sort_values('avg_happiness', ascending=False)
print(regional_stats.to_string())

#  4. DIAGNOSTIC ANALYTICS: Correlation 
print("\n" + "" * 40)
print("CORRELATION WITH HAPPINESS SCORE:")
print("" * 40)
numeric_cols = ['gdp_per_capita', 'social_support', 'life_expectancy']
correlations = df[numeric_cols + ['happiness_score']].corr()['happiness_score'].drop('happiness_score')
for factor, corr in correlations.items():
    direction = " Positive" if corr > 0 else " Negative"
    print(f"  {factor:30s}: {corr:+.3f}  {direction}")

#  5. VISUALIZATION 
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Happiness by Region (bar chart)
regional_avg = df.groupby('region')['happiness_score'].mean().sort_values(ascending=True)
axes[0].barh(regional_avg.index, regional_avg.values, color='steelblue', alpha=0.8)
axes[0].set_xlabel('Average Happiness Score')
axes[0].set_title('Average Happiness Score by Region')
axes[0].axvline(df['happiness_score'].mean(), color='red', linestyle='--', label='Global Avg')
axes[0].legend()
axes[0].grid(axis='x', alpha=0.3)

# Plot 2: GDP vs Happiness scatter
regions = df['region'].unique()
colors = plt.cm.Set2(range(len(regions)))
for region, color in zip(regions, colors):
    mask = df['region'] == region
    axes[1].scatter(df[mask]['gdp_per_capita']/1000,
                    df[mask]['happiness_score'],
                    label=region, s=80, alpha=0.8, color=color)

axes[1].set_xlabel('GDP per Capita ($000s)')
axes[1].set_ylabel('Happiness Score')
axes[1].set_title('GDP vs Happiness Score')
axes[1].legend(fontsize=8)
axes[1].grid(alpha=0.3)

plt.suptitle('Day 1 Lab: World Happiness Analysis', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('session1_lab_output.png', dpi=100, bbox_inches='tight')
plt.show()
print("\n Chart saved as 'session1_lab_output.png'")

#  6. KEY FINDINGS 
print("\n" + "=" * 60)
print("KEY FINDINGS:")
print("=" * 60)
happiest = df.loc[df['happiness_score'].idxmax()]
unhappiest = df.loc[df['happiness_score'].idxmin()]
print(f"   Happiest: {happiest['country']} (Score: {happiest['happiness_score']})")
print(f"   Unhappiest: {unhappiest['country']} (Score: {unhappiest['happiness_score']})")
print(f"   Global average: {df['happiness_score'].mean():.2f}")
print(f"   GDP correlation: {correlations['gdp_per_capita']:+.3f}")
print("\n Lab complete! Explore the exercises in the Colab notebook.")
