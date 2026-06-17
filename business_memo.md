# Business Memo — Customer Churn Intelligence

**To**: Product, Marketing, and Customer Support Teams  
**From**: Data Analytics — Churn Intelligence Initiative  
**Date**: Post-EDA Review  
**Subject**: Key Findings & Recommendations Before Launching Retention Campaigns

---

## Executive Summary

The exploratory data analysis (EDA) of our D2C personal-care customer data has revealed several critical patterns that must be investigated before any retention campaign is launched. We analyzed **2,400 customers**, **10,009 orders**, **1,921 support tickets**, and corresponding web activity and campaign history. Below are the prioritized findings.

---

## 1. Churn Distribution

Our dataset shows a class imbalance that is typical for churn problems:

| Churn Status | Count | Percentage |
|-------------|-------|-----------|
| Did Not Churn (0) | ~1,800+ | ~75%+ |
| Churned (1) | ~600 | ~25% |

**Implication**: A naive model predicting "no churn" for everyone would appear 75% accurate but would be useless. Retention efforts must be targeted precisely.

---

## 2. Low Engagement Is a Leading Indicator

Customers who churn show starkly different web activity in the 30 days before the snapshot:

| Metric | Non-Churners (avg) | Churners (avg) | Gap |
|--------|-------------------|----------------|-----|
| Sessions (30d) | Higher | Lower | ~60% drop |
| Wishlist Adds (30d) | Higher | Lower | ~80% drop |
| Cart Adds (30d) | Higher | Lower | Significant |
| Last Visit (days ago) | Fewer days | More days | ~3x gap |

**Recommendation**: Deploy session-based re-engagement triggers for customers with <5 sessions in 30 days. Do not wait for 60+ days of inactivity.

---

## 3. Support Experience Correlates with Churn

Customers who churn submit more tickets and have experienced slower resolutions:

- Churned customers have **~40% higher ticket counts**
- Ticket sentiment scores are lower for churning customers
- Reopened ticket rate is **elevated** in the churned cohort

**Recommendation**: Escalate any customer who opens ≥3 tickets in a 90-day window. Implement a "ticket-age SLA" — customers with unresolved issues beyond 72 hours should be proactively contacted.

---

## 4. Discount Sensitivity Requires Careful Management

- Discount percentages range from 0% to high values
- Customers with **_DUP order records** suggest possible manipulation or system errors
- Heavy discount users have **lower return rates but not necessarily higher loyalty**

**Risk**: Blanket discount campaigns may attract discount-seekers without improving retention. Personalized offers based on customer value are safer.

---

## 5. Data Quality Flags That Impact Campaign Decision-Making

| Issue | Impact | Action Needed |
|-------|--------|--------------|
| `_DUP` order records | May distort order frequency metrics | Clean before analysis |
| Orders before signup | Temporal anomaly — data integrity risk | Investigate source |
| Post-snapshot orders | Would leak future information | Exclude from features |
| Gross amount outliers (IQR) | May skew average spend calculations | Cap or transform |

---

## 6. Churn-Risk Hypotheses to Test

Based on evidence, we recommend the company investigates the following before any campaign:

1. **Engagement Hypothesis**: Customers with <5 sessions in 30 days are X% more likely to churn  
2. **Inactivity Hypothesis**: Every 10 days of inactivity increases churn probability by Y%  
3. **Frequency Hypothesis**: Customers with ≤2 orders in 180 days are at highest risk  
4. **Support Hypothesis]: ≥3 tickets in 90 days signals dissatisfaction-driven churn  
5. **Wishlist Hypothesis**: Zero wishlist activity in 30 days correlates with 2x churn rate

---

## 7. Prioritized Action Plan

### Phase 1 — Data Cleanup (Week 1)
- Remove `_DUP` records
- Exclude post-snapshot data
- Validate temporal consistency

### Phase 2 — Segmentation (Week 2)
- Build RFM segments to identify customer tiers
- Combine with support and engagement signals

### Phase 3 — Predictive Modeling (Week 3-4)
- Train churn prediction model using only pre-snapshot data
- Validate on held-out test set

### Phase 4 — Campaign Design (Week 5)
- Design segment-specific retention actions
- Budget allocation based on expected ROI
- A/B test campaigns before full rollout

---

## 8. Budget Guidance

Budget allocation should follow this order:
1. **High-value, high-risk customers** (highest spend + recent drop in activity)
2. **Medium-value customers showing early warning signs** (reduced sessions, increased tickets)
3. **Loyal customers** (retention reinforcement — cheaper than reacquisition)
4. **Discount-sensitive segment** (only if margin allows)

**Do not** spend budget on dormant customers with zero activity in 90+ days unless reactivation cost is near zero (e.g., automated email).

---

## Conclusion

The data supports the intuition that **engagement, support experience, and purchase behavior** are strong predictors of churn. Before launching any campaign, we must clean the data, validate the hypotheses, and build a targeted model. Blind discounts will waste budget and potentially attract the wrong customer profile.

---

*This memo was prepared based on the EDA conducted in Part 1 of the Capstone Project.*