# SQL Joins and Aggregations

## 1. Group By & Aggregations
Combining rows and calculating statistics.
- `COUNT()`: Number of rows
- `SUM()`: Total sum
- `AVG()`: Average value
- `MIN()` / `MAX()`

```sql
SELECT city, AVG(marks) as avg_marks
FROM students
GROUP BY city;
```

## 2. Joins
Combining data from multiple tables.
- **INNER JOIN**: Returns records with matching values in both tables.
- **LEFT JOIN**: Returns all records from the left table, and matched records from the right.

```sql
SELECT students.name, courses.course_name
FROM students
INNER JOIN enrollments ON students.id = enrollments.student_id;
```
