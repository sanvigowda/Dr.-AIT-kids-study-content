#  SQL for Data Analytics

> **Learning Goal:** Understand why SQL is the backbone of data analytics and how it compares to Pandas.

---

##  What is SQL?

**SQL (Structured Query Language)** is the standard language for interacting with **Relational Databases** (RDMS). 

While Pandas is great for data on your local machine, SQL is where "Big Data" lives. Most companies store their transaction records, customer details, and logs in databases like PostgreSQL, MySQL, or BigQuery.

###  Pandas vs. SQL

| Feature | Pandas | SQL |
|---------|--------|-----|
| **Data Source** | CSV, Excel, Local Files | Centralized Databases |
| **Scale** | Limited by RAM (typically < 10GB) | Can handle Terabytes/Petabytes |
| **Logic** | Procedural (Step-by-step) | Declarative ("What" you want, not "How") |
| **Persistence** | Temporary (in-memory) | Permanent Storage |

---

##  The Core Concepts

SQL works on **Tables** (similar to DataFrames).

- **Rows**: Individual records (e.g., one sale).
- **Columns**: Attributes (e.g., price, date, product name).
- **Primary Key**: A unique ID for every row (e.g., `txn_id`).
- **Foreign Key**: An ID that links to another table (e.g., `customer_id` links to the Customers table).

---

##  SQL in Python (SQLite)

In this session, we will use **SQLite**. Its a lightweight database that doesn't require a server. Its built directly into Python!

```python
import sqlite3
import pandas as pd

# 1. Connect to a database (creates it if it doesn't exist)
conn = sqlite3.connect("retail_data.db")

# 2. Load a CSV into SQL
df = pd.read_csv("session3_transactions_clean.csv")
df.to_sql("transactions", conn, if_exists="replace", index=False)

# 3. Run a SQL query
query = "SELECT * FROM transactions LIMIT 5"
result = pd.read_sql(query, conn)
print(result)
```

---

##  Why Data Analysts Love SQL?

1. **Efficiency**: Databases are optimized to filter millions of rows in milliseconds.
2. **Filtering at Source**: Instead of downloading 1GB of data and filtering in Python, you can ask SQL to only send you the 10MB you actually need.
3. **Universality**: Every data tool (Tableau, PowerBI, Python) speaks SQL.

---

##  Quick Check Questions

1. When should you use SQL instead of Pandas?
2. What is the difference between a Row and a Column?
3. What does "Declarative Language" mean in the context of SQL?

---

*Next Topic  [Basic Queries: SELECT & WHERE](./02_Basic_Queries.md)*
