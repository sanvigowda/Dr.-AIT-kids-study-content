#  Basic SQL Queries

> **Learning Goal:** Learn how to extract specific data from a database using SELECT, WHERE, and ORDER BY.

---

## 1 SELECT: Picking Columns

The `SELECT` statement tells the database which columns you want.

```sql
-- Get everything
SELECT * FROM transactions;

-- Get specific columns
SELECT txn_id, amount, category FROM transactions;
```

>  **Analyst Pro-Tip:** Avoid `SELECT *`. It slows down your queries on large datasets. Always pick the columns you need.

---

## 2 WHERE: Filtering Rows

The `WHERE` clause is the "Filter" of SQL.

### Common Operators:
| Operator | Meaning | Example |
|----------|---------|---------|
| `=` | Equal to | `category = 'Food'` |
| `!=` or `<>` | Not equal to | `store != 'Store A'` |
| `>` / `<` | Greater/Less than | `amount > 5000` |
| `BETWEEN` | Range | `amount BETWEEN 1000 AND 2000` |
| `IN` | Match any in list | `category IN ('Electronics', 'Clothing')` |
| `LIKE` | Pattern match | `store LIKE 'Store%'` |

---

## 3 ORDER BY: Sorting Results

Use `ORDER BY` to sort your data. Default is ascending (`ASC`).

```sql
-- Sort by amount (highest first)
SELECT * 
FROM transactions 
ORDER BY amount DESC;
```

---

##  Quick Check Questions

1. How do you select only the `txn_id` and `store` columns?
2. Write a query to find transactions where the `amount` is less than 500.
3. How do you sort transactions by `date` from newest to oldest?
