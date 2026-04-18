#  SQL Joins

> **Learning Goal:** Learn how to combine data from multiple tables to build a complete view of your business.

---

## 1 The Common Join Types

| Join Type | Description |
|-----------|-------------|
| **INNER JOIN** | Returns records that have matching values in both tables. |
| **LEFT JOIN** | Returns all records from the left table, and matched records from the right. (Most common!) |

---

## 2 How to Write a JOIN

```sql
SELECT 
    t.txn_id, 
    t.amount, 
    s.location, 
    s.manager
FROM transactions t        -- 't' is an alias
JOIN stores s              -- 's' is an alias
ON t.store = s.store;      -- The common link
```

---

## 3 Left Join vs Inner Join

Analysts usually prefer **LEFT JOIN** to ensure they don't accidentally lose data from the primary table.

---

##  Real-World Example: Manager Performance

```sql
SELECT 
    s.manager, 
    SUM(t.amount) as total_managed_sales
FROM stores s
LEFT JOIN transactions t ON s.store = t.store
GROUP BY s.manager
ORDER BY total_managed_sales DESC;
```

---

##  Quick Check Questions

1. Which join would you use if you want all transactions, even if the store info is missing?
2. What happens if there is no match in an INNER JOIN?
3. What is an alias, and why is it useful?
