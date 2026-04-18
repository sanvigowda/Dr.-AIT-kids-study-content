import sqlite3
import pandas as pd
import os

# --- PREPARATION: Load data into SQL ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TXN_DATA = os.path.join(ROOT_DIR, "session3_transactions_clean.csv")
STORES_DATA = os.path.join(ROOT_DIR, "Day_3", "data", "stores_lookup.csv")

# Create data directory if missing
os.makedirs(os.path.dirname(STORES_DATA), exist_ok=True)

# Create stores_lookup.csv if missing
if not os.path.exists(STORES_DATA):
    pd.DataFrame({
        'store': ['Store A', 'Store B', 'Store C', 'Store D', 'Store E'],
        'location': ['Mumbai', 'Bangalore', 'Chennai', 'Delhi', 'Hyderabad'],
        'manager': ['Rajesh', 'Anjali', 'Karthik', 'Sonia', 'Vikram']
    }).to_csv(STORES_DATA, index=False)

# Connect to SQLite
conn = sqlite3.connect("retail_analytics.db")

# Load CSVs to SQL
df_txns = pd.read_csv(TXN_DATA)
df_txns.to_sql("transactions", conn, if_exists="replace", index=False)

df_stores = pd.read_csv(STORES_DATA)
df_stores.to_sql("stores", conn, if_exists="replace", index=False)

print(" SQL Environment Ready: Databases 'transactions' and 'stores' loaded.\n")

# --- LAB TASKS ---

def run_query(title, query):
    print(f"--- {title} ---")
    print(f"SQL: {query}")
    result = pd.read_sql(query, conn)
    print(result)
    print("\n")

# Task 1: Basic Selection
run_query("Task 1: Store A Sample", 
          "SELECT txn_id, amount, date FROM transactions WHERE store = 'Store A' LIMIT 5")

# Task 2: Aggregation
run_query("Task 2: Category Performance", 
          "SELECT category, SUM(amount) as revenue, AVG(items_count) as avg_items FROM transactions GROUP BY category")

# Task 3: Sorting & Filtering
run_query("Task 3: High Value Electronics", 
          "SELECT txn_id, amount, date FROM transactions WHERE category = 'Electronics' ORDER BY amount DESC LIMIT 3")

# Task 4: Joins
run_query("Task 4: Sales with Location", 
          """
          SELECT t.txn_id, t.amount, s.location 
          FROM transactions t
          JOIN stores s ON t.store = s.store
          LIMIT 5
          """)

# Task 5: Business Challenge
run_query("Task 5: City Revenue Leaderboard", 
          """
          SELECT s.location, SUM(t.amount) AS total_revenue
          FROM stores s
          JOIN transactions t ON s.store = t.store
          GROUP BY s.location
          ORDER BY total_revenue DESC
          """)

# Close connection
conn.close()
print(" Lab Complete!")
