#  Visualization Ethics

> **Learning Goal:** Learn the responsibility that comes with creating charts  a misleading chart can be more dangerous than wrong data.

---

##  Why Does Visualization Ethics Matter?

> "With great power comes great responsibility."  Uncle Ben (and Data Analysts too!)

Charts are powerful. A well-designed chart can:
-  Help people make **better decisions**
-  **Simplify** complex information
-  **Mislead** audiences if done wrong (accidentally or on purpose)

In 2020, a government agency published a COVID case chart with a **reversed Y-axis**  it made cases look like they were going down when they were actually going up. Thousands of people were confused.

---

##  Common Misleading Chart Techniques

### 1. Truncated Y-Axis (Most Common!)

**Problem:** Starting the Y-axis at a value other than 0 makes small differences look huge.

```
 MISLEADING                     HONEST
Marks                            Marks
100                             100 
 98                          80 
 94                        60 
 90                    40 
    A  B  C                       20 
                                   0 
"Huge difference!!"                    A      B      C
                                "Very similar, actually."
```

**In Python  always start Y at 0:**
```python
plt.ylim(0, 100)  #  Always do this for comparison charts!
```

---

### 2. Cherry-Picking Data (Selective Reporting)

**Problem:** Showing only the data that supports your story.

```python
#  BAD: Only showing months where our product sold well
months_good = ["Mar", "Apr", "May"]
sales_good  = [85000, 90000, 92000]

#  GOOD: Show ALL months, even the bad ones
months_all = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales_all  = [45000, 42000, 85000, 90000, 92000, 41000]
```

> Showing only 3 good months makes it look like sales are always great.
> Showing all 6 months reveals the pattern is seasonal.

---

### 3. Misleading Pie Charts

**Problem:** Using pie when categories don't add up to 100%, or having too many slices.

```
 WRONG  Slices add up to 120%!     RIGHT  Adds to 100%

  Product A: 40%                       Product A: 35%
  Product B: 45%                       Product B: 40%
  Product C: 35%                       Product C: 25%
  Total:    120%  ERROR!              Total:    100% 
```

---

### 4. 3D Charts (Avoid!)

**Problem:** 3D effects distort proportions and make comparison difficult.

>  **Never use 3D pie charts** in professional data analysis.
> The tilted perspective makes front slices look bigger than they are!

---

### 5. Changing the Scale Midway

**Problem:** Inconsistent intervals make trends look different.

```
 Inconsistent:    0, 10, 20, 50, 100, 500
 Consistent:      0, 20, 40, 60, 80, 100
```

---

##  Rules for Ethical Visualization

| Rule | Why It Matters |
|------|----------------|
| **Start Y-axis at 0** for bar charts | Prevents exaggerating differences |
| **Show all data**, not just favorable parts | Prevents cherry-picking |
| **Label axes clearly** with units | "Sales" vs "Sales ( Lakhs)" is very different |
| **Use consistent scale** | Prevents misleading comparisons |
| **Choose the right chart type** | Pie with 10 slices misleads |
| **Add source and date** | Makes data trustworthy |
| **Don't use color to manipulate** | Red always makes people feel danger |
| **Don't add unnecessary ink** | Cluttered charts hide the message |

---

##  GOOD vs BAD: Side-by-Side Example

```python
import matplotlib.pyplot as plt

cities = ["Chennai", "Bangalore", "Hyderabad"]
marks  = [76.3, 86.7, 72.7]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

#  BAD: Truncated Y-axis
ax1.bar(cities, marks, color="steelblue")
ax1.set_ylim(70, 90)    # Starts at 70  MISLEADING!
ax1.set_title(" Misleading: Y starts at 70")
ax1.set_ylabel("Avg Marks")

#  GOOD: Y-axis starts at 0
ax2.bar(cities, marks, color="steelblue", edgecolor="black")
ax2.set_ylim(0, 100)    # Starts at 0  HONEST!
ax2.set_title(" Honest: Y starts at 0")
ax2.set_ylabel("Avg Marks")
# Add value labels
for i, (city, val) in enumerate(zip(cities, marks)):
    ax2.text(i, val + 0.5, f"{val:.1f}", ha="center", fontweight="bold")

plt.suptitle("Visualization Ethics: Truncated Y-Axis Demo", fontweight="bold")
plt.tight_layout()
plt.show()
```

---

##  Real-World Consequences

| What Happened | Impact |
|--------------|--------|
| Fox News in 2012 showed a pie chart where slices added to 193% | Viral misinformation |
| UK government COVID chart had inverted axis | Public confusion about safety |
| A pharma company showed trial data from just 3 good months | Misleading drug effectiveness |
| A tech startup showed user growth with a truncated Y-axis | Misled investors |

---

##  Key Takeaways

1. **Always start Y-axis at 0** for comparison charts
2. **Never cherry-pick**  show all the data honestly
3. **Avoid 3D charts**  they distort perception
4. **Pie charts** must add to exactly 100%
5. A misleading visualization can be **more harmful** than no visualization

---

##  Quick Check Questions

1. You're making a bar chart showing student marks (all between 7090). Should you start Y at 0 or 70? Why?
2. A company shows only JanuaryMarch sales data in their annual report. What's wrong?
3. You have 12 product categories  should you use a pie chart? Why not?
4. What's the difference between an honest chart and an ethical chart?

---

*Next: Session 2 Lab  [Lab_VSCode_Visualization.py](./Lab_VSCode_Visualization.py)*
