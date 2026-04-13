# 📊 Data Analytics Complete

> **A complete Day-by-Day Data Analytics course with hands-on labs, notebooks, and real-world mini projects.**

---

## 📁 Repository Structure

```
```
Data_analytics_complete/
├── Day_1/
│   ├── Session_1_Introduction/
│   │   └── ...labs & documents
│   ├── Session_2_Data_Collection_Cleaning/
│   │   └── ...cleaned_ecommerce_data.csv
│   ├── Session_3_Python_for_Analytics/
│   │   └── ...session3_transactions_clean.csv
│   ├── Mini_Project_SuperMart/
│   │   └── ...scripts, data, output
│   └── pandas_intro.md
│
└── Day_2/
    ├── Session_1_EDA/
    │   └── ...labs & documents
    ├── Session_2_Visualization_Fundamentals/
    │   └── ...labs & documents
    ├── Session_3_Advanced_Visualization/
    │   └── ...labs & documents
    └── Mini_Project_Student_Performance/
        └── student_performance_analysis.py
├── Day_2_Complete_EDA_and_Visualization.ipynb
├── students_data.csv
```

---

## 🚀 Quick Start

### Run the Day 2 Complete Notebook
You can run the full EDA and Visualization pipeline in one go:
1. Open `Day_2_Complete_EDA_and_Visualization.ipynb` in VS Code or Jupyter.
2. The notebook will automatically generate `students_data.csv` and run all analyses.

### Run the Day 1 Model Mini Project
(unchanged instructions...)


---

## 🚀 Quick Start

### Run the Day 1 Model Mini Project

```bash
# 1. Install dependencies
pip install pandas numpy matplotlib seaborn requests

# 2. Navigate to mini project
cd Day_1/Mini_Project_SuperMart/scripts

# 3. Generate the dataset
python 00_generate_data.py

# 4. Run the full analytics pipeline
python supermart_analysis.py
```

### Run Individual Lab Scripts

```bash
# Session 1 Lab
python Day_1/Session_1_Introduction/Lab_VSCode_Dataset_Exploration.py

# Session 2 Lab
python Day_1/Session_2_Data_Collection_Cleaning/Lab_VSCode_Data_Cleaning.py

# Session 3 Lab
python Day_1/Session_3_Python_for_Analytics/Lab_VSCode_Dataset_Manipulation.py
```

---

## 📚 Day 1 Topics Covered

| Session | Topics |
|---------|--------|
| **Session 1: Introduction** | Data Analytics Lifecycle, 4 Types of Analytics (Descriptive/Diagnostic/Predictive/Prescriptive), Industry Applications, Career Pathways |
| **Session 2: Data Cleaning** | CSV/API/Database sources, Missing values (7 strategies), Duplicate detection & removal, Data transformation techniques |
| **Session 3: Python** | NumPy arrays & vectorized ops, Pandas DataFrames, Filtering & Boolean indexing, GroupBy & Aggregation |


| **Mini Project** | End-to-end SuperMart Sales Intelligence pipeline using all Day 1 topics |

---

## 📚 Day 2 Topics Covered

| Session | Topics |
|---------|--------|
| **Session 1: EDA** | Statistical Summaries (Mean/Median/Std), Correlation Analysis, Outlier Detection (IQR Method), Descriptive vs. Inferential basics |
| **Session 2: Visualization Fundamentals** | Chart Selection Principles, Bar/Line/Histogram/Boxplots, Visualization Ethics (Misleading scales) |
| **Session 3: Advanced Visualization** | Multi-Variable Visualization, Heatmaps, Distribution Plots (KDE), Interactive Visual Insights |


| **Capstone** | 6-Panel Student Performance Analytics Dashboard using `gridspec` |




---

## 🎯 Project: SuperMart Sales Intelligence

The Day 1 model mini project is a complete analytics pipeline for a fictional retail chain with 5 stores across India.

**What it covers:**
- ✅ Loading raw CSV with data quality issues
- ✅ Auditing and documenting 5 types of data problems
- ✅ Cleaning: duplicates, invalid prices, inconsistent text, missing values, mixed date formats
- ✅ Feature engineering: revenue, quarter, membership, basket size
- ✅ Multi-level analysis: store, category, quarterly trends
- ✅ Dashboard: 6-panel dark-themed visualization

**Student Mini Project:** After studying the model project, students build their own version with a different dataset (see `Mini_Project_SuperMart/README.md`).

---

## 🛠️ Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.8+ | python.org |
| Pandas | 1.5+ | `pip install pandas` |
| Kaggle Pandas Certification | - | https://www.kaggle.com/learn/pandas |
| NumPy | 1.20+ | `pip install numpy` |
| Matplotlib | 3.5+ | `pip install matplotlib` |
| Seaborn | 0.12+ | `pip install seaborn` |

Or install all at once:
```bash
pip install pandas numpy matplotlib seaborn requests jupyter
```

---

## 📓 Google Colab

To run in Google Colab, open the `.ipynb` files directly:
1. Go to [colab.research.google.com](https://colab.research.google.com)
2. File → Open notebook → GitHub tab
3. Paste this repo URL and select the notebook

---

*Data Analytics Complete — Building real skills, one day at a time.*