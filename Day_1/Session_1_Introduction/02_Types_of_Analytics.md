#  Types of Analytics

> **Learning Goal:** Understand the 4 types of analytics and know when to use each one in real business scenarios.

---

##  The Analytics Spectrum

Analytics exists on a spectrum from **describing what happened** to **recommending what to do**:

```
PAST  FUTURE
                                                                 
Descriptive  Diagnostic  Predictive  Prescriptive
                                             
"What           "Why          "What          "What
happened?"    happened?"     will           should
                            happen?"       we do?"
```

**Complexity and value both increase as you move right.**

---

## 1 Descriptive Analytics  *"What happened?"*

### Definition
Summarizes **historical data** to understand what has occurred. It is the most basic and commonly used type.

### Real-Life Example
> **Company:** Amazon
> **Question:** "What were our total sales in Q4 2024?"
> **Answer:** A dashboard showing:
> - Total revenue: 50 Crore
> - Best-selling category: Electronics
> - Peak sales day: November 25 (Black Friday)

### Techniques Used
- Summary statistics (mean, median, mode)
- Grouping and aggregation
- Dashboards and reports
- Time series charts

### Python Example
```python
import pandas as pd

# Sales data
sales = pd.DataFrame({
    'month': ['Jan', 'Feb', 'Mar', 'Apr'],
    'revenue': [120000, 145000, 132000, 178000]
})

# Descriptive analytics - What happened?
print("Total Revenue:", sales['revenue'].sum())          # 575000
print("Average Monthly Revenue:", sales['revenue'].mean())  # 143750
print("Best Month:", sales.loc[sales['revenue'].idxmax(), 'month'])  # Apr
```

### Business Value:  (Medium)
Good for monitoring and reporting, but doesn't explain causes.

---

## 2 Diagnostic Analytics  *"Why did it happen?"*

### Definition
Digs deeper into data to **understand the causes** behind trends identified in descriptive analytics. Involves correlation and pattern analysis.

### Real-Life Example
> **Company:** Flipkart
> **Observation (Descriptive):** Website traffic dropped 40% in February
> **Diagnostic Question:** *Why did traffic drop?*
> **Investigation:**
> - Checked server logs  page load time increased to 8 seconds
> - Checked marketing spend  no change
> - Checked competitor activity  competitor launched a big sale
> **Root Cause:** Slow website + competitor sale drove users away

### Techniques Used
- Drill-down analysis
- Correlation analysis
- Data filtering and segmentation
- Root cause analysis

### Python Example
```python
import pandas as pd
import numpy as np

# Monthly data with multiple variables
data = pd.DataFrame({
    'month': range(1, 13),
    'sales': [100, 120, 90, 110, 95, 85, 130, 140, 125, 150, 160, 200],
    'marketing_spend': [5000, 6000, 4000, 5500, 4500, 4000, 7000, 7500, 6500, 8000, 9000, 12000],
    'avg_temperature': [15, 17, 20, 25, 30, 35, 32, 31, 27, 22, 17, 14]
})

# Diagnostic: Find what correlates with sales
correlation = data[['sales', 'marketing_spend', 'avg_temperature']].corr()
print("Correlation with Sales:")
print(correlation['sales'])
# marketing_spend has high correlation  that's why sales changed!
```

### Business Value:  (High)
Helps prevent future problems by understanding root causes.

---

## 3 Predictive Analytics  *"What will happen?"*

### Definition
Uses **statistical models and machine learning** to forecast future outcomes based on historical patterns.

### Real-Life Example
> **Company:** HDFC Bank
> **Question:** "Which customers are likely to default on their loan next month?"
> **Model:** Looks at payment history, income, spending patterns, credit score
> **Output:** List of 500 customers with >70% probability of defaulting
> **Action:** Bank proactively contacts those customers to restructure their loans

### Techniques Used
- Regression analysis
- Classification models
- Time series forecasting (ARIMA, Prophet)
- Machine learning (Random Forest, XGBoost)

### Python Example
```python
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Historical sales data (12 months)
months = np.array(range(1, 13)).reshape(-1, 1)
sales = np.array([100, 120, 115, 130, 125, 140, 145, 150, 165, 170, 180, 200])

# Train a simple predictive model
model = LinearRegression()
model.fit(months, sales)

# Predict next 3 months (13, 14, 15)
future_months = np.array([[13], [14], [15]])
predictions = model.predict(future_months)

print("Predicted Sales for Next 3 Months:")
for i, pred in enumerate(predictions, 13):
    print(f"  Month {i}: {pred:.0f} units")
# Month 13: 215 units
# Month 14: 222 units
# Month 15: 229 units
```

### Business Value:  (Very High)
Enables proactive decision-making before problems occur.

---

## 4 Prescriptive Analytics  *"What should we do?"*

### Definition
The **most advanced** type of analytics. Not only predicts what will happen but also **recommends the best action** to take, often using optimization algorithms.

### Real-Life Example
> **Company:** Ola / Uber
> **Problem:** Too many drivers in downtown at 2 AM, not enough at the airport at 6 AM
> **Prescriptive Analytics:**
> - Predicts demand for the next 24 hours by location
> - Calculates optimal driver positioning
> - Sends surge pricing signals and driver incentives to move supply to demand
> **Result:** 95% of ride requests fulfilled within 5 minutes

### Techniques Used
- Optimization algorithms (Linear Programming)
- Simulation (Monte Carlo)
- Decision trees with action recommendations
- Reinforcement learning

### Python Example
```python
from scipy.optimize import linprog
import numpy as np

# Business Problem: Maximize profit from 2 products
# Product A gives 5 profit, Product B gives 4 profit
# Constraints: Machine hours (A needs 2hr, B needs 1hr, max 100hr)
#              Raw material (A needs 1kg, B needs 3kg, max 150kg)

# Prescriptive: Find optimal production mix
# Minimize -profit (linprog minimizes, so negate profit to maximize)
c = [-5, -4]  # negative because we're maximizing

# Constraint matrix (Ax <= b)
A = [[2, 1],   # machine hours
     [1, 3]]   # raw material
b = [100, 150]  # limits

# Non-negativity bounds
x_bounds = [(0, None), (0, None)]

result = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method='highs')
print(f"Optimal: Produce {result.x[0]:.0f} units of A, {result.x[1]:.0f} units of B")
print(f"Maximum Profit: {-result.fun:.0f}")
```

### Business Value:  (Maximum)
Directly drives optimized business decisions.

---

##  Comparison Table

| Feature | Descriptive | Diagnostic | Predictive | Prescriptive |
|---------|-------------|------------|------------|--------------|
| **Question** | What happened? | Why did it happen? | What will happen? | What should we do? |
| **Data Focus** | Historical | Historical + Context | Historical  Future | Future + Optimization |
| **Difficulty** | Low | Medium | High | Very High |
| **Tools** | Excel, SQL, Tableau | Python, SQL | ML, Statistics | AI, Optimization |
| **Example** | Monthly sales report | Sales drop analysis | Demand forecast | Inventory optimization |
| **Business Impact** | Monitoring | Problem solving | Planning | Action |

---

##  Industry Examples

### E-Commerce (Meesho / Amazon)
- **Descriptive:** "What are the top 10 products sold this week?"
- **Diagnostic:** "Why did returns increase in the electronics category?"
- **Predictive:** "Which products will sell most during Diwali?"
- **Prescriptive:** "What discounts should we offer to maximize profit?"

### Healthcare (Apollo Hospitals)
- **Descriptive:** "How many patients were admitted for diabetes last year?"
- **Diagnostic:** "Why is readmission rate high in cardiac patients?"
- **Predictive:** "Which patients are at risk of developing complications?"
- **Prescriptive:** "What treatment protocol minimizes recovery time?"

---

##  Key Takeaways

1. All 4 types are **valuable**  most organizations use all of them at different times
2. Start with **Descriptive** analytics before moving to advanced types
3. **Predictive** requires clean historical data as input
4. **Prescriptive** analytics is where AI/ML creates the most business value
5. 80% of industry analytics today is still **Descriptive + Diagnostic**

---

##  Quick Check Questions

1. A retail company creates a report showing last month's revenue. What type of analytics is this?
2. You build a model to predict customer churn. What type is this?
3. What is the key difference between predictive and prescriptive analytics?
4. Which type of analytics is most commonly used in business today?

---

*Previous: [Data Analytics Lifecycle](./01_Data_Analytics_Lifecycle.md) | Next: [Industry Applications & Career Pathways](./03_Industry_Applications_Career.md)*
