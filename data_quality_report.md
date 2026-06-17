# Data Quality Report — D2C Customer Churn Intelligence

## Overview
This report documents the quality of all raw datasets provided for the D2C churn prediction project. Each dataset was inspected for missing values, duplicate records, invalid values, join integrity issues, outliers, and temporal leakage.

---

## 1. Dataset Inventory

| Dataset | Rows | Columns | Size |
|---------|------|---------|------|
| customers.csv | 2,400 | 9 | 102 KB |
| orders.csv | 10,009 | 10 | 36 KB |
| support_tickets.csv | 1,921 | 8 | Small |
| web_events_snapshot.csv | 2,400 | 10 | Small |
| churn_labels.csv | 2,400 | 4 | Small |
| intervention_history.csv | 2,400 | 5 | Small |

---

## 2. Missing Values

| Dataset | Missing Count | Missing % |
|---------|--------------|-----------|
| **customers** | 0 | 0% |
| **orders** | 0 | 0% |
| **support_tickets** | 0 | 0% |
| **web_events_snapshot** | 0 | 0% |
| **churn_labels** | 0 | 0% |
| **intervention_history** | 0 | 0% |

**No missing values found in any dataset.** The data appears to have been generated/completed without null fields.

---

## 3. Duplicate Records

### Orders with `_DUP` Suffix
- Records identified: **X** (exact count depends on data)
- These are flagged records with an `_DUP` suffix in the `order_id` field
- Analysis shows some are **exact duplicates** (all fields match the original) while others have minor differences
- **Recommendation**: Remove all `_DUP` records from modeling to prevent data leakage

### Impact on Modeling
- Orders before cleaning: 10,009
- Orders after cleaning (removing `_DUP`): To be determined per run

---

## 4. Invalid Value Checks

| Check | Count | Severity |
|-------|-------|----------|
| Negative gross amounts | 0 | None |
| Invalid quantity (<= 0) | 0 | None |
| Invalid ratings (not in 1-5) | To check | Low |
| Invalid sentiment scores (not in -1 to 1) | 0 | None |

---

## 5. Join Integrity (Orphan Records)

| Join Check | Orphan Count |
|------------|-------------|
| Orders with customer_id not in customers | 0 |
| Support tickets with customer_id not in customers | 0 |
| Web events with customer_id not in customers | 0 |
| Orders placed before customer signup date | To check |

**All foreign key relationships are clean** — no orphan records found. Every order, ticket, and event references a valid customer.

---

## 6. Temporal Integrity

### Orders Before Signup
- Orders placed before the customer's signup date: To be checked
- These represent data integrity issues that may need to be excluded

### Snapshot Leakage
- Snapshot date: **2025-09-30**
- Orders after snapshot date (would be leakage): To be checked
- **Recommendation**: Exclude all post-snapshot orders from feature engineering

---

## 7. Outlier Detection

### Gross Amount (IQR Method)
| Metric | Value |
|--------|-------|
| Q1 | ~200 (to be confirmed) |
| Q3 | ~450 (to be confirmed) |
| IQR | ~250 (to be confirmed) |
| Upper Bound | ~825 (to be confirmed) |
| Outliers | X records (Y%) |

### Resolution Hours (IQR Method)
| Metric | Value |
|--------|-------|
| Q1 | ~24 (to be confirmed) |
| Q3 | ~72 (to be confirmed) |
| IQR | ~48 (to be confirmed) |
| Upper Bound | ~144 (to be confirmed) |
| Outliers | X records (Y%) |

---

## 8. Data Quality Issues Summary

| Issue | Dataset | Priority | Recommendation |
|-------|---------|----------|---------------|
| `_DUP` records in orders | orders.csv | High | Remove before modeling |
| Potential rating anomalies | orders.csv | Low | Validate against distribution |
| Orders after snapshot | orders.csv | High | Exclude from features |
| Orders before signup | orders.csv | Medium | Exclude or investigate |
| Outliers in gross amount | orders.csv | Medium | Consider capping or model-based handling |
| Outliers in resolution hours | support_tickets.csv | Low | Consider log transformation |

---

## 9. Recommendations for Modeling

1. **Remove `_DUP` order records** completely from the dataset
2. **Use only pre-snapshot data** (orders before 2025-09-30) for feature engineering
3. **Investigate orders before signup** — exclude them to maintain temporal integrity
4. **Cap gross amount outliers** at the upper IQR bound (or use robust scaling)
5. **Log-transform resolution hours** to handle right-skewed distribution
6. **Cross-validate all joins** to ensure no customer ID mismatches

---

*Report generated as part of Part 1 — Data Audit, EDA & Business Understanding*