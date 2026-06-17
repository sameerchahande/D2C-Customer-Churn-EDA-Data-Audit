# D2C Customer Churn Intelligence: Data Audit & Exploratory Data Analysis

## Project Overview

Customer retention is one of the most important growth drivers for any Direct-to-Consumer (D2C) business. Acquiring new customers is often more expensive than retaining existing ones, making churn analysis a critical business function.

This project focuses on performing a comprehensive Data Audit and Exploratory Data Analysis (EDA) for a D2C personal care brand. The objective is to assess data quality, identify customer behavior patterns, uncover churn-related insights, and generate actionable business recommendations that can support retention strategies.

The analysis integrates customer demographics, purchase history, support interactions, website engagement metrics, intervention campaigns, and churn labels to build a complete view of customer behavior.

---

## Business Problem

The company has observed a decline in repeat purchases and an increase in customer churn. Management wants to understand:

* Why customers stop purchasing
* Which customer behaviors indicate churn risk
* What engagement metrics correlate with retention
* How support interactions influence customer loyalty
* Which customer segments require proactive intervention

The goal of this project is to transform raw operational data into meaningful business intelligence that can guide retention-focused decision making.

---

## Project Objectives

### Data Quality Assessment

* Validate dataset integrity
* Identify missing values
* Detect duplicate records
* Check for invalid values
* Verify referential integrity
* Detect potential data leakage
* Analyze outliers

### Exploratory Data Analysis

* Understand customer demographics
* Analyze purchasing behavior
* Evaluate engagement metrics
* Investigate support interactions
* Study churn distribution patterns

### Business Intelligence

* Identify churn indicators
* Validate churn hypotheses
* Generate retention recommendations
* Provide actionable business insights

---

## Dataset Description

The project uses six interconnected datasets:

### Customers Dataset

Contains customer profile information including:

* Customer ID
* Age Group
* City Tier
* Acquisition Channel
* Signup Date

### Orders Dataset

Contains purchase transaction history:

* Order ID
* Customer ID
* Order Date
* Product Category
* Quantity
* Gross Amount
* Discounts
* Delivery Performance
* Customer Ratings
* Returns

### Support Tickets Dataset

Contains customer support interactions:

* Ticket ID
* Customer ID
* Resolution Hours
* Sentiment Scores
* Reopened Tickets
* Issue Types

### Web Events Dataset

Contains customer engagement metrics:

* Sessions
* Website Visits
* Wishlist Activity
* Browsing Behavior

### Intervention History Dataset

Contains retention campaign information.

### Churn Labels Dataset

Contains churn outcomes used for analysis.

---

## Data Audit Framework

A structured audit process was conducted before performing any analytical work.

### Dataset Inspection

* Shape validation
* Schema verification
* Data type review
* Sample record inspection

### Missing Value Analysis

* Missing count identification
* Missing percentage calculation
* Dataset-level quality assessment

### Duplicate Validation

* Detection of duplicate order records
* Comparison of original and duplicated transactions
* Duplicate impact assessment

### Leakage Validation

A snapshot date methodology was used to ensure future information was not inadvertently included in the analysis.

### Invalid Value Checks

Validation included:

* Negative order amounts
* Invalid quantities
* Rating range violations
* Sentiment score violations

### Join Integrity Validation

Cross-dataset customer identifiers were validated to detect orphan records and ensure consistency.

### Outlier Detection

IQR-based outlier analysis was performed on:

* Gross Order Amount
* Ticket Resolution Hours

---

## Exploratory Data Analysis

### Customer Analysis

Investigated customer demographics and acquisition trends.

Key areas:

* City Tier Distribution
* Age Group Distribution
* Acquisition Channel Analysis

### Engagement Analysis

Examined customer interaction patterns including:

* Session Activity
* Website Visits
* Wishlist Additions
* Customer Inactivity

### Order Behavior Analysis

Evaluated purchasing patterns:

* Product Categories
* Order Frequency
* Total Spend
* Discount Utilization
* Delivery Performance
* Customer Ratings
* Return Behavior

### Support Analysis

Explored customer service interactions:

* Ticket Volume
* Issue Categories
* Resolution Time
* Ticket Reopen Rates
* Sentiment Trends

---

## Churn Hypothesis Testing

Four business hypotheses were tested to understand the drivers of customer churn.

### Hypothesis 1

Lower Engagement → Higher Churn

Measured using:

* Sessions in the last 30 days

### Hypothesis 2

Longer Inactivity → Higher Churn

Measured using:

* Days since last website visit

### Hypothesis 3

Lower Purchase Frequency → Higher Churn

Measured using:

* Total order count

### Hypothesis 4

Lower Wishlist Activity → Higher Churn

Measured using:

* Wishlist additions in the last 30 days

---

## Key Findings

### Customer Engagement Matters

Customers with lower platform activity exhibit significantly higher churn rates.

### Inactivity is a Strong Churn Signal

Long periods without website visits are highly correlated with churn behavior.

### Purchase Frequency Influences Retention

Customers who purchase more frequently are substantially less likely to churn.

### Wishlist Activity Predicts Loyalty

Customers actively interacting with wishlists demonstrate stronger retention patterns.

### Customer Experience Impacts Retention

Support sentiment and issue resolution quality influence long-term customer relationships.

---

## Business Recommendations

### Proactive Churn Monitoring

Develop monitoring systems to identify customers exhibiting:

* Low session activity
* Extended inactivity
* Reduced purchasing behavior

### Personalized Retention Campaigns

Implement targeted:

* Product recommendations
* Re-engagement emails
* Promotional incentives
* Wishlist reminders

### Customer Experience Optimization

Focus on:

* Faster issue resolution
* Reduced ticket reopen rates
* Improved customer satisfaction

### Retention-Focused Segmentation

Create customer risk segments to prioritize intervention efforts and marketing spend.

---

## Technology Stack

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Jupyter Notebook

---

## Repository Structure

```text
README.md
eda_audit.ipynb
data_quality_report.md
business_memo.md
requirements.txt
```

---

## Expected Business Impact

The insights generated through this analysis can help the organization:

* Reduce customer churn
* Improve retention rates
* Increase customer lifetime value
* Optimize marketing spend
* Enhance customer satisfaction
* Support data-driven decision making

---

## Author

Data Analytics & Business Intelligence Project

Focused on transforming raw customer data into actionable insights through Data Auditing, Exploratory Data Analysis, and Churn Intelligence.
