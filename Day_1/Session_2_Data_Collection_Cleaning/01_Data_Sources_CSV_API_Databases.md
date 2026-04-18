#  Data Sources — CSV, APIs, and Databases

> **Learning Goal:** Learn how to collect data from the three most common sources: CSV files, APIs, and databases — with hands-on Python examples.

---

##  Where Does Data Come From?

In the real world, data lives in many places. As a data analyst, you need to know how to **access data from multiple sources** and bring it into Python for analysis.

```
Data Sources
├── Files → CSV, Excel, JSON, XML, Parquet
├── APIs → REST APIs (weather, finance, social media)
├── Databases → SQL (MySQL, PostgreSQL), NoSQL (MongoDB)
├── Web Scraping → HTML, tables from websites
└── Streaming → IoT sensors, real-time feeds
```

---

## 1️⃣ CSV Files — The Most Common Starting Point

### What is CSV?
**CSV (Comma-Separated Values)** is a plain text format where each row is a record and fields are separated by commas.

```
student_id,name,score,grade
101,Priya,85,A
102,Rahul,72,B
103,Aisha,91,A+
```

### Real-Life Example
> Government portals in India (data.gov.in) publish datasets as CSV files — population census, crop production statistics, highway traffic data.

### Reading CSV with Pandas

```python
import pandas as pd

# Read from local file
df = pd.read_csv('students.csv')

# Read from a URL directly
url = "https://raw.githubusercontent.com/datasets/covid-19/main/data/worldwide-aggregated.csv"
df = pd.read_csv(url)

# Read with options
df = pd.read_csv(
    'sales_data.csv',
    sep=',',              # delimiter
    header=0,            # row number for column names
    index_col='order_id', # set as index
    parse_dates=['date'], # convert to datetime
    encoding='utf-8'     # handle special characters
)

print(df.head())       # First 5 rows
print(df.shape)        # (rows, columns)
print(df.dtypes)       # Data types of each column
print(df.info())       # Complete summary
```

### Writing CSV

```python
# Save DataFrame to CSV
df.to_csv('cleaned_data.csv', index=False)  # index=False avoids writing row numbers

# Save only specific columns
df[['name', 'score']].to_csv('scores_only.csv', index=False)
```

### Other File Formats

```python
# Excel
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')
df.to_excel('output.xlsx', index=False)

# JSON
df = pd.read_json('data.json')
df.to_json('output.json', orient='records')

# Parquet (faster for large datasets)
df = pd.read_parquet('data.parquet')
df.to_parquet('output.parquet')
```

---

## 2️⃣ APIs — Getting Live Data

### What is an API?
An **API (Application Programming Interface)** is a way for programs to talk to each other. A **REST API** lets you request data over the internet using HTTP.

Think of it like ordering at a restaurant:
- You (the analyst) → are the customer
- The menu (API docs) → tells you what you can order
- The API endpoint → is the kitchen that prepares your request
- The response (JSON) → is the food delivered to you

### Real-Life Example
> **OpenWeatherMap API** lets you get real-time weather for any city. A delivery company uses this to predict whether bad weather will delay deliveries.

### Making API Requests with Python

```python
import requests
import pandas as pd

# Example: Get weather data for Mumbai (free API)
API_KEY = "your_api_key_here"  # Sign up at openweathermap.org for free
city = "Mumbai"

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

# Make the request
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    data = response.json()
    print(f"City: {data['name']}")
    print(f"Temperature: {data['main']['temp']}°C")
    print(f"Weather: {data['weather'][0]['description']}")
    print(f"Humidity: {data['main']['humidity']}%")
else:
    print(f"Error: {response.status_code}")
```

### Working with JSON API Response

```python
import requests
import pandas as pd

# Free API: Get currency exchange rates
url = "https://api.frankfurter.app/latest?from=USD&to=INR,EUR,GBP"
response = requests.get(url)
data = response.json()

# data looks like:
# {"base": "USD", "rates": {"INR": 83.2, "EUR": 0.92, "GBP": 0.79}}

# Convert to DataFrame
rates_df = pd.DataFrame(list(data['rates'].items()), columns=['Currency', 'Rate'])
rates_df['Base'] = data['base']
rates_df['Date'] = data['date']
print(rates_df)
```

### Free APIs to Practice With

| API | What It Provides | URL |
|-----|-----------------|-----|
| JSONPlaceholder | Fake REST API for testing | jsonplaceholder.typicode.com |
| Open-Meteo | Weather forecasts (no key needed) | open-meteo.com |
| CoinGecko | Cryptocurrency prices | api.coingecko.com |
| REST Countries | Country information | restcountries.com |
| NASA | Space data and images | api.nasa.gov |

### Pagination — When Data Is in Pages

```python
import requests
import pandas as pd

all_posts = []
page = 1

# Some APIs return data in pages (like search results)
while page <= 5:  # Get first 5 pages
    response = requests.get(f"https://jsonplaceholder.typicode.com/posts?_page={page}&_limit=10")
    data = response.json()
    
    if not data:  # No more data
        break
    
    all_posts.extend(data)
    page += 1

df = pd.DataFrame(all_posts)
print(f"Total posts collected: {len(df)}")
```

---

## 3️⃣ Databases — Structured Data at Scale

### What is a Database?
A **database** stores structured data in organized tables that can be queried efficiently. Unlike CSV files, databases handle millions of records efficiently.

### Real-Life Example
> **IRCTC** (Indian Railways) stores hundreds of millions of booking records in databases. They use SQL to generate daily reports of train occupancy, revenue, and cancellations.

### Connecting to SQLite (No Setup Required)

```python
import sqlite3
import pandas as pd

# Create a database and table (SQLite works locally, no server needed)
conn = sqlite3.connect('analytics_demo.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        product TEXT,
        quantity INTEGER,
        price REAL,
        sale_date TEXT,
        region TEXT
    )
''')

# Insert sample data
sample_data = [
    (1, 'Laptop', 5, 45000, '2024-01-15', 'Mumbai'),
    (2, 'Phone', 12, 25000, '2024-01-16', 'Delhi'),
    (3, 'Tablet', 8, 35000, '2024-01-17', 'Chennai'),
    (4, 'Laptop', 3, 45000, '2024-01-18', 'Bangalore'),
    (5, 'Phone', 20, 25000, '2024-01-19', 'Mumbai'),
]
cursor.executemany('INSERT OR IGNORE INTO sales VALUES (?,?,?,?,?,?)', sample_data)
conn.commit()

# Read directly into DataFrame using SQL
query = """
    SELECT region, 
           product, 
           SUM(quantity) as total_units,
           SUM(quantity * price) as total_revenue
    FROM sales
    GROUP BY region, product
    ORDER BY total_revenue DESC
"""
df = pd.read_sql_query(query, conn)
print(df)
conn.close()
```

### Connecting to MySQL (Production Database)

```python
# pip install mysql-connector-python
import mysql.connector
import pandas as pd

config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'ecommerce_db'
}

conn = mysql.connector.connect(**config)

# Read into DataFrame
df = pd.read_sql("SELECT * FROM orders WHERE status = 'shipped'", conn)
conn.close()
```

### Combining Multiple Sources

```python
import pandas as pd
import requests
import sqlite3

# Step 1: Get product catalog from CSV
products_df = pd.read_csv('products.csv')

# Step 2: Get real-time prices from API
response = requests.get("https://api.example.com/prices")
prices_df = pd.DataFrame(response.json())

# Step 3: Get order history from database
conn = sqlite3.connect('orders.db')
orders_df = pd.read_sql("SELECT * FROM orders", conn)
conn.close()

# Step 4: Merge all sources
full_df = orders_df.merge(products_df, on='product_id').merge(prices_df, on='product_id')
print(f"Combined dataset shape: {full_df.shape}")
```

---

## ✅ Key Takeaways

1. **CSV files** are the easiest starting point — use `pd.read_csv()`
2. **APIs** give you live, real-time data — always check `response.status_code == 200`
3. **Databases** handle large, structured data — use `pd.read_sql_query()` to bring data into Pandas
4. Real projects often combine **multiple sources**
5. Always check **data types** and **shape** after loading

---

*Previous: [Session 1](../Session_1_Introduction/) | Next: [Handling Missing Values](./02_Handling_Missing_Values.md)*
