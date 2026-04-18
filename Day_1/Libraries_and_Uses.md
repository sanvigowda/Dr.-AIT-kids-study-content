#  Python Libraries Used in Day 1 — Data Analytics Complete

> A quick-reference guide to every library used across Day 1 sessions, their purpose, and the key functions you'll use most.

---

## 1.  NumPy (`numpy`)

**What it is:** The core numerical computing library for Python. Provides fast, multi-dimensional arrays and mathematical operations.

**Install:** `pip install numpy`

| Function / Feature | What it Does | Day 1 Usage |
|-------------------|-------------|-------------|
| `np.array()` | Create an array from a list | Store sales matrix (stores × months) |
| `np.zeros()` / `np.ones()` | Create arrays filled with 0s or 1s | Initialize blank grids |
| `np.arange(start, stop, step)` | Create evenly-spaced range of numbers | Generate month indices |
| `np.linspace(start, stop, n)` | Create `n` evenly-spaced points | Axes/interpolation |
| `np.random.rand()` | Generate random floats [0, 1) | Synthetic data generation |
| `np.random.randint()` | Generate random integers | Quantity, age columns |
| `np.random.choice()` | Randomly pick from a list | Sampling categories, stores |
| `np.random.seed()` | Fix random state for reproducibility | All labs use `np.random.seed(42)` |
| `arr.shape` | Get dimensions of array | `(4, 12)` = 4 stores × 12 months |
| `arr.dtype` | Get data type of elements | `float64`, `int64` |
| `arr.sum(axis=1)` | Sum along rows (per store) or columns (per month) | Annual totals per store |
| `arr.mean(axis=0)` | Average down each column (per month) | Monthly average across stores |
| `arr.max()` / `arr.min()` | Highest / lowest value | Peak sales month |
| `arr.argmax()` / `arr.argmin()` | Index of max / min value | Which month was best? |
| `arr.std()` | Standard deviation | Variability in sales |
| `arr.reshape(r, c)` | Change shape without changing data | (12,) → (4, 3) for quarters |
| `arr.flatten()` | Collapse to 1D | Reverse of reshape |
| `arr.T` | Transpose (rows ↔ columns) | Stores ↔ months |
| `np.where(cond, a, b)` | Conditional value assignment | `is_member → True/False` flag |
| `np.select(conds, labels)` | Multiple-condition assignment | Seniority levels |
| `np.concatenate()` | Join arrays end-to-end | Combine Q1 + Q2 sales |
| `np.vstack()` / `np.hstack()` | Stack vertically / horizontally | Add new store row |
| `np.diff(arr, axis=1)` | Difference between consecutive elements | Month-over-month change |
| `np.nan` | Represents a missing numeric value | Missing ratings, prices |
| `np.newaxis` | Add a dimension | Prepare arrays for ML |

---

## 2.  Pandas (`pandas`)

**What it is:** The core data manipulation library. Provides `Series` (1D) and `DataFrame` (2D table) for loading, cleaning, and analyzing structured data.

**Install:** `pip install pandas`

### Loading & Saving Data

| Function | What it Does | Example |
|----------|-------------|---------|
| `pd.read_csv()` | Load a CSV file | `pd.read_csv('sales.csv')` |
| `pd.read_excel()` | Load an Excel file | `pd.read_excel('data.xlsx')` |
| `pd.read_sql_query()` | Load from a database query | `pd.read_sql_query(sql, conn)` |
| `pd.read_json()` | Load JSON data | `pd.read_json('data.json')` |
| `df.to_csv()` | Save DataFrame to CSV | `df.to_csv('out.csv', index=False)` |
| `df.to_excel()` | Save to Excel | `df.to_excel('out.xlsx')` |

### Exploring Data

| Function | What it Does |
|----------|-------------|
| `df.head(n)` | First `n` rows (default 5) |
| `df.tail(n)` | Last `n` rows |
| `df.sample(n)` | Random `n` rows |
| `df.shape` | `(rows, columns)` tuple |
| `df.columns` | List of column names |
| `df.dtypes` | Data type of each column |
| `df.info()` | Full summary: types, non-null counts, memory |
| `df.describe()` | Stats for numeric columns (mean, std, min, max) |
| `df.nunique()` | Unique value count per column |
| `df['col'].value_counts()` | Frequency of each value |

### Selecting & Filtering

| Function | What it Does |
|----------|-------------|
| `df['col']` | Select a single column (returns Series) |
| `df[['a', 'b']]` | Select multiple columns |
| `df.iloc[row, col]` | Select by **integer position** |
| `df.loc[row, col]` | Select by **label / condition** |
| `df[df['col'] > 5]` | Boolean filter (rows where condition is True) |
| `df['col'].isin([...])` | Filter: value is in a list |
| `df['col'].between(a, b)` | Filter: value is in range [a, b] |
| `df['col'].str.contains()` | Filter: text column contains pattern |
| `df.query("col > 5")` | SQL-like readable filtering |

### Cleaning Data

| Function | What it Does |
|----------|-------------|
| `df.isnull()` / `df.isna()` | Returns True where values are missing |
| `df.isnull().sum()` | Count missing values per column |
| `df.dropna()` | Drop rows/cols with missing values |
| `df.fillna(value)` | Fill missing values with a constant |
| `df['col'].fillna(method='ffill')` | Forward fill — use previous value |
| `df['col'].interpolate()` | Estimate missing values between known points |
| `df.drop_duplicates()` | Remove duplicate rows |
| `df.duplicated()` | Returns True for duplicate rows |
| `df.drop(columns=[...])` | Remove columns |
| `df.rename(columns={...})` | Rename columns |
| `df.reset_index(drop=True)` | Reset row numbers after filtering |

### Transforming Data

| Function | What it Does |
|----------|-------------|
| `df['col'].astype()` | Convert data type |
| `pd.to_datetime()` | Parse strings as dates |
| `df['date'].dt.month` | Extract month from datetime column |
| `df['date'].dt.day_name()` | Day of week name |
| `df['col'].str.strip()` | Remove leading/trailing whitespace |
| `df['col'].str.title()` | Convert to Title Case |
| `df['col'].str.lower()` | Convert to lowercase |
| `df['col'].str.replace()` | Find and replace in text |
| `df['col'].map({...})` | Value mapping (e.g. `Yes → True`) |
| `df['col'].apply(func)` | Apply a custom function element-wise |
| `pd.cut()` | Bin continuous data into labeled categories |
| `pd.qcut()` | Bin by quantile (equal-frequency bins) |
| `pd.get_dummies()` | One-hot encode categorical columns |

### Aggregation & Grouping

| Function | What it Does |
|----------|-------------|
| `df.groupby('col')` | Group rows by a column's values |
| `df.groupby('col').agg({...})` | Multiple aggregations at once |
| `df.groupby('col').sum()` | Sum per group |
| `df.groupby('col').mean()` | Average per group |
| `df.groupby('col').transform()` | Add group-level stats back to all rows |
| `df.pivot()` / `df.pivot_table()` | Cross-tabulate two columns |
| `df['col'].rolling(n).mean()` | Rolling (moving) average |
| `df['col'].cumsum()` | Cumulative (running) total |
| `df['col'].rank()` | Rank values within a Series |

### Merging Data

| Function | What it Does |
|----------|-------------|
| `pd.merge(df1, df2, on='key', how='inner')` | SQL-style JOIN (inner/left/right/outer) |
| `pd.concat([df1, df2])` | Stack DataFrames on top of each other |

---

## 3.  Matplotlib (`matplotlib.pyplot`)

**What it is:** The foundational plotting library for Python. Gives precise control over every element of a chart.

**Install:** `pip install matplotlib`

| Function | What it Does | When to Use |
|----------|-------------|-------------|
| `plt.figure(figsize=(w,h))` | Create a figure canvas | Always at the start of a chart |
| `plt.plot(x, y)` | Line chart | Trends over time |
| `plt.bar(x, height)` | Vertical bar chart | Comparing categories |
| `plt.barh(y, width)` | Horizontal bar chart | Long category names |
| `plt.hist(data, bins=n)` | Histogram | Distribution of values |
| `plt.scatter(x, y)` | Scatter plot | Relationship between 2 variables |
| `plt.pie(values, labels=...)` | Pie / donut chart | Proportions |
| `plt.axvline(x)` | Vertical reference line | Mark mean, median |
| `plt.axhline(y)` | Horizontal reference line | Mark a target |
| `plt.title('...')` | Add chart title | — |
| `plt.xlabel('...')` | X-axis label | — |
| `plt.ylabel('...')` | Y-axis label | — |
| `plt.legend()` | Show legend | Multiple series |
| `plt.grid(alpha=0.3)` | Show grid lines | Readability |
| `plt.tight_layout()` | Auto-fix overlapping elements | Before saving |
| `plt.savefig('file.png', dpi=100)` | Save chart to file | Always save in VS Code |
| `plt.show()` | Display chart | — |
| `plt.subplots(rows, cols)` | Create multi-panel figure | Dashboards |
| `gridspec.GridSpec()` | Precise subplot layout | Complex dashboards |

---

## 4.  Seaborn (`seaborn`)

**What it is:** Built on top of Matplotlib. Creates beautiful statistical charts with less code.

**Install:** `pip install seaborn`

| Function | What it Does | When to Use |
|----------|-------------|-------------|
| `sns.heatmap(df.corr())` | Correlation heatmap | See relationships between all columns |
| `sns.boxplot(x, y, data=df)` | Box & whisker plot | Spot outliers per group |
| `sns.histplot(df['col'])` | Enhanced histogram with KDE curve | Distribution |
| `sns.scatterplot(x, y, hue='col')` | Scatter with color encoding | Two vars + a category |
| `sns.barplot(x, y, data=df)` | Bar chart with confidence intervals | Group comparison |
| `sns.lineplot(x, y, data=df)` | Line chart with shaded confidence band | Time trends |
| `sns.pairplot(df)` | Grid of scatter plots for all column pairs | EDA overview |
| `sns.set_style('darkgrid')` | Set chart theme | Visual consistency |
| `sns.countplot(x='col', data=df)` | Bar chart of value frequencies | Categorical distribution |

---

## 5.  Requests (`requests`)

**What it is:** The standard library for making HTTP requests to APIs. Lets you fetch live data from the internet.

**Install:** `pip install requests`

| Function | What it Does |
|----------|-------------|
| `requests.get(url)` | Make a GET request to a URL or API |
| `response.status_code` | Check if request succeeded (`200` = OK, `404` = not found) |
| `response.json()` | Parse the response as a Python dictionary |
| `response.text` | Get raw text content of the response |
| `requests.get(url, params={...})` | Send query parameters with the request |
| `requests.get(url, headers={...})` | Send authentication headers (API keys) |

---

## 6. ️ SQLite3 (`sqlite3`)

**What it is:** Python's built-in module for working with SQLite databases — no server needed.

**Install:** Built-in (no install needed)

| Function | What it Does |
|----------|-------------|
| `sqlite3.connect('file.db')` | Create or open a database file |
| `conn.cursor()` | Create a cursor to run SQL statements |
| `cursor.execute(sql)` | Run a single SQL statement |
| `cursor.executemany(sql, data)` | Insert many rows at once |
| `conn.commit()` | Save changes to the database |
| `pd.read_sql_query(sql, conn)` | Load SQL results directly into a DataFrame |
| `conn.close()` | Close the database connection |

---

## 7.  scikit-learn (`sklearn`)

**What it is:** The most popular machine learning library. Day 1 uses only its preprocessing utilities.

**Install:** `pip install scikit-learn`

| Function | What it Does | Day 1 Usage |
|----------|-------------|-------------|
| `MinMaxScaler()` | Scale values to range [0, 1] | Normalization of salary, age |
| `StandardScaler()` | Scale to mean=0, std=1 | Standardization for ML models |
| `KNNImputer(n_neighbors=k)` | Fill missing values using K nearest neighbors | Advanced missing value imputation |
| `scaler.fit_transform(df)` | Fit scaler and transform in one step | — |
| `LinearRegression()` | Train a simple linear regression model | Predictive analytics demo |

---

## 8. ️ Pathlib (`pathlib`)

**What it is:** Python's built-in module for file system path handling. Cleaner than `os.path`.

**Install:** Built-in

| Function | What it Does |
|----------|-------------|
| `Path('folder/file.csv')` | Create a path object |
| `path.exists()` | Check if file or folder exists |
| `Path('folder').mkdir(exist_ok=True)` | Create directory if it doesn't exist |

---

## ️ Which Library for Which Task?

| Task | Use This |
|------|----------|
| Load a CSV file | `pandas` |
| Math on large number arrays | `numpy` |
| Fetch data from an API | `requests` |
| Query a database | `sqlite3` + `pandas` |
| Clean & transform data | `pandas` |
| Create charts | `matplotlib` or `seaborn` |
| Statistical visualizations | `seaborn` |
| Scale/normalize features | `sklearn.preprocessing` |
| Fill missing values smartly | `sklearn.impute.KNNImputer` |

---

##  Install Everything at Once

```bash
pip install pandas numpy matplotlib seaborn requests scikit-learn
```

Or for Jupyter / Google Colab (run inside a cell):
```python
!pip install pandas numpy matplotlib seaborn requests scikit-learn -q
```

---

*Part of the Data Analytics Complete Course — Day 1*
