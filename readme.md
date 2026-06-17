# Part 1 — Data Audit, EDA & Business Understanding

## D2C Customer Churn Intelligence & Retention API — Capstone Project

### Overview
This repository contains **Part 1** of the D2C Customer Churn Intelligence Capstone Project. The objective is to understand the business problem, audit raw data quality, perform exploratory data analysis (EDA), and derive churn-risk hypotheses.

### Dataset
The dataset includes 6 CSV files:
| File | Description |
|------|-------------|
| `data/customers.csv` | Customer demographics (2,400 customers) |
| `data/orders.csv` | Order history (10,009 orders) |
| `data/support_tickets.csv` | Support ticket records (1,921 tickets) |
| `data/web_events_snapshot.csv` | Web/App activity snapshot |
| `data/churn_labels.csv` | Churn labels with train/validation/test split |
| `data/intervention_history.csv` | Campaign/intervention history |

**Snapshot Date**: 2025-09-30

### How to Run

```bash
# 1. Install dependencies
pip install pandas numpy matplotlib seaborn

# 2. Launch the notebook
jupyter notebook eda_audit.ipynb
```

Or open `eda_audit.ipynb` directly in VS Code or any Jupyter-compatible IDE.

### Project Structure
```
.
├── data/                       # Raw dataset files
│   ├── customers.csv
│   ├── orders.csv
│   ├── support_tickets.csv
│   ├── web_events_snapshot.csv
│   ├── churn_labels.csv
│   └── intervention_history.csv
├── eda_audit.ipynb             # Main EDA notebook
├── data_quality_report.md      # Data quality findings
├── business_memo.md            # Business recommendations
├── readme.md                   # This file
└── requirements.txt            # Python dependencies
```

### Key Findings

| Area | Finding |
|------|---------|
| Missing Values | None found in any dataset |
| Duplicate Records | `_DUP` records found in orders — removed for analysis |
| Outliers | Gross amount and resolution hours have IQR-based outliers |
| Leakage | Post-snapshot orders excluded from feature engineering |
| Churn Rate | ~25% churn rate (class imbalance) |

### Churn-Risk Hypotheses
1. **Low Engagement → Higher Churn**: Fewer sessions in last 30 days
2. **Longer Inactivity → Higher Churn**: More days since last visit
3. **Lower Purchase Frequency → Higher Churn**: Fewer total orders
4. **Lower Wishlist Activity → Higher Churn**: Fewer wishlist adds
5. **Higher Support Tickets → Higher Churn**: Frequent complaints indicate dissatisfaction

### Visual Outputs
The notebook generates 6+ meaningful charts:
- Churn Distribution (bar chart)
- City Tier, Age Group, Acquisition Channel (count plots)
- Orders by Category, Discounts, Delivery Times
- Customer Ratings & Returns
- Support Ticket Analysis (issue types, sentiment, reopened)
- Behavioral Signals vs Churn (box plots)

### Deliverables
- `eda_audit.ipynb` — Complete EDA notebook
- `data_quality_report.md` — Data quality audit report
- `business_memo.md` — Business memo with recommendations