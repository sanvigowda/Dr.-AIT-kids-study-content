import pandas as pd
import sqlite3
import os

# --- 1. SETUP ---
# Connect to the database created in Session 1
DATABASE = "../../retail_analytics.db"
if not os.path.exists(DATABASE):
    print("Error: Database not found. Please run Session 1 Lab first!")
    exit()

conn = sqlite3.connect(DATABASE)

print("SuperMart Business Intelligence Analysis")
print("---------------------------------------\n")

# --- 2. PHASE 1: SQL EXTRACTION ---
# TODO: Write a SQL query to get: location, total revenue, and order count per city
query = """
SELECT 
    -- Add columns here
    'REPLACE_ME' as placeholder
FROM transactions t
JOIN stores s ON t.store = s.store
GROUP BY s.location
"""

city_performance = pd.read_sql(query, conn)
print("City Performance Report:")
print(city_performance)
print("\n")

# --- 3. PHASE 2: PANDAS ANALYSIS ---
# Load and clean date
df = pd.read_sql("SELECT * FROM transactions", conn)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# TODO: Calculate a 7-day rolling average of 'amount'
# df['rolling_avg'] = ...

# TODO: Find "Dormant Champions"
# Definition: member == 1 AND date < (latest_date - 30 days)
latest_date = df['date'].max()
# dormant_members = ...

print("Analysis Complete. Ready for Recommendations.")

# Close connection
conn.close()
