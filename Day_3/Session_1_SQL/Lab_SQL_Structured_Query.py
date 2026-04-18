"""
LAB: SQL Structured Querying
This lab uses a simulated database environment within Pandas (SQLAlchemy/pandasql style).
"""
import pandas as pd

# 1. Create a dummy database
students = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Arjun', 'Priha', 'Vikram'],
    'city': ['Bangalore', 'Chennai', 'Hyderabad']
})

marks = pd.DataFrame({
    'student_id': [1, 2, 3],
    'score': [88, 78, 95]
})

# 2. Simulate an INNER JOIN
merged = pd.merge(students, marks, left_on='id', right_on='student_id')
print("Inner Join Result:")
print(merged[['name', 'score']])

# 3. Simulate Aggregation
print("\nAverage Score:")
print(merged['score'].mean())
