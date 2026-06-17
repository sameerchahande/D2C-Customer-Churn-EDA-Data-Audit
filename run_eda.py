import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os

sns.set_style("whitegrid")
pd.set_option("display.max_columns", None)

PLOTS_DIR = Path("plots")
PLOTS_DIR.mkdir(exist_ok=True)
plot_num = [0]

def save_plot(name):
    plot_num[0] += 1
    filename = f"{plot_num[0]:02d}_{name}.png"
    plt.savefig(PLOTS_DIR / filename, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"  [Plot saved: {filename}]")

DATA_DIR = Path("data")

customers = pd.read_csv(DATA_DIR / "customers.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")
tickets = pd.read_csv(DATA_DIR / "support_tickets.csv")
events = pd.read_csv(DATA_DIR / "web_events_snapshot.csv")
labels = pd.read_csv(DATA_DIR / "churn_labels.csv")
campaigns = pd.read_csv(DATA_DIR / "intervention_history.csv")

datasets = {
    'customers': customers,
    'orders': orders,
    'support_tickets': tickets,
    'web_events': events,
    'churn_labels': labels,
    'intervention_history': campaigns
}

for name, df in datasets.items():

    print("\n" + "="*60)
    print(f"DATASET : {name.upper()}")
    print("="*60)

    
    print(f"\nShape : {df.shape}")

    print("\nSample Records:")
    print(df.head())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\n")

    customers["signup_date"] = pd.to_datetime(customers["signup_date"])

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)

tickets["ticket_date"] = pd.to_datetime(
    tickets["ticket_date"]
)


print("Missing Values Report")

missing_report = pd.DataFrame({
    'Missing_Count': customers.isnull().sum(),
    'Missing_Percent': round((customers.isnull().sum()/len(customers))*100,2)
})

print(missing_report[missing_report['Missing_Count']>0])

print("\nOrders Missing Values")
print(pd.DataFrame({
    'Missing_Count': orders.isnull().sum(),
    'Missing_Percent': round((orders.isnull().sum()/len(orders))*100,2)
}))

print("\nSupport Tickets Missing Values")
print(pd.DataFrame({
    'Missing_Count': tickets.isnull().sum(),
    'Missing_Percent': round((tickets.isnull().sum()/len(tickets))*100,2)
}))

print("\nWeb Events Missing Values")
print(pd.DataFrame({
    'Missing_Count': events.isnull().sum(),
    'Missing_Percent': round((events.isnull().sum()/len(events))*100,2)
}))

dup_orders = orders[orders['order_id'].str.contains('_DUP', na=False)]

print("Duplicate-like records found:", len(dup_orders))
print(dup_orders.head())


dup_orders = dup_orders.copy()

dup_orders['original_order_id'] = dup_orders['order_id'].str.replace('_DUP','', regex=False)

original_orders = orders[
    orders['order_id'].isin(dup_orders['original_order_id'])
].copy()

comparison = dup_orders.merge(
    original_orders,
    left_on='original_order_id',
    right_on='order_id',
    suffixes=('_dup','_orig')
)

print("Matched duplicate pairs:", len(comparison))


cols_to_compare = [
    'customer_id',
    'order_date',
    'category',
    'quantity',
    'gross_amount',
    'discount_pct',
    'delivery_days',
    'returned',
    'rating'
]

for col in cols_to_compare:
    comparison[f'{col}_match'] = (
        comparison[f'{col}_dup'] ==
        comparison[f'{col}_orig']
    )

match_cols = [c for c in comparison.columns if c.endswith('_match')]

comparison['all_fields_match'] = comparison[match_cols].all(axis=1)

comparison['all_fields_match'].value_counts()


total_dup = len(comparison)

exact_dup = comparison['all_fields_match'].sum()

print(f"Total DUP Records: {total_dup}")
print(f"Exact Duplicates: {exact_dup}")
print(f"Non-Exact Duplicates: {total_dup-exact_dup}")



orders_clean = orders[~orders['order_id'].str.contains('_DUP', na=False)].copy()

print("Orders before cleaning:", len(orders))
print("Orders after cleaning:", len(orders_clean))
print("Records removed:", len(orders)-len(orders_clean))



SNAPSHOT = pd.Timestamp("2025-09-30")

orders_pre = orders[
    orders["order_date"] <= SNAPSHOT
].copy()

orders_post = orders[
    orders["order_date"] > SNAPSHOT
].copy()

print("\n")
print("=" * 60)
print("LEAKAGE CHECK")
print("=" * 60)

print(
    "Post snapshot orders:",
    len(orders_post)
)

print("\n")
print("=" * 60)
print("INVALID VALUE CHECKS")
print("=" * 60)

print(
    "Negative gross amount:",
    (orders["gross_amount"] < 0).sum()
)

print(
    "Invalid quantity:",
    (orders["quantity"] <= 0).sum()
)

print(
    "Invalid rating:",
    (
        (~orders["rating"].between(1,5))
        &
        orders["rating"].notna()
    ).sum()
)

print(
    "Invalid sentiment:",
    (
        ~tickets["sentiment_score"]
        .between(-1,1)
    ).sum()
)


print("\n")
print("=" * 60)
print("JOIN VALIDATION")
print("=" * 60)

cust_ids = set(customers["customer_id"])

orders_orphans = len(
    set(orders["customer_id"]) - cust_ids
)

ticket_orphans = len(
    set(tickets["customer_id"]) - cust_ids
)

event_orphans = len(
    set(events["customer_id"]) - cust_ids
)

print("Order orphans:", orders_orphans)
print("Ticket orphans:", ticket_orphans)
print("Event orphans:", event_orphans)

date_check = orders_pre.merge(
    customers[
        ["customer_id","signup_date"]
    ],
    on="customer_id",
    how="left"
)

invalid_orders = date_check[
    date_check["order_date"]
    <
    date_check["signup_date"]
]

print(
    "\nOrders before signup:",
    len(invalid_orders)
)



Q1 = orders_clean['gross_amount'].quantile(0.25)
Q3 = orders_clean['gross_amount'].quantile(0.75)

IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

gross_outliers = orders_clean[
    (orders_clean['gross_amount'] < lower_bound) |
    (orders_clean['gross_amount'] > upper_bound)
]

print("Q1:", round(Q1,2))
print("Q3:", round(Q3,2))
print("IQR:", round(IQR,2))
print("Upper Bound:", round(upper_bound,2))

print("\nNumber of Gross Amount Outliers:", len(gross_outliers))

print(
    gross_outliers[['order_id','customer_id','gross_amount']]
    .sort_values('gross_amount', ascending=False)
    .head(10)
)



Q1 = tickets['resolution_hours'].quantile(0.25)
Q3 = tickets['resolution_hours'].quantile(0.75)

IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

resolution_outliers = tickets[
    (tickets['resolution_hours'] < lower_bound) |
    (tickets['resolution_hours'] > upper_bound)
]

print("Q1:", round(Q1,2))
print("Q3:", round(Q3,2))
print("IQR:", round(IQR,2))
print("Upper Bound:", round(upper_bound,2))

print("\nNumber of Resolution Time Outliers:", len(resolution_outliers))

print(
    resolution_outliers[
        ['ticket_id','resolution_hours']
    ].sort_values(
        'resolution_hours',
        ascending=False
    ).head(10)
)


print(
    f"Gross Amount Outlier %: "
    f"{round(len(gross_outliers)/len(orders_clean)*100,2)}%"
)

print(
    f"Resolution Time Outlier %: "
    f"{round(len(resolution_outliers)/len(tickets)*100,2)}%"
)

order_agg = orders_pre.groupby(
    "customer_id"
).agg(
    total_orders=("order_id","count"),
    total_spend=("gross_amount","sum"),
    avg_order_value=("gross_amount","mean"),
    avg_discount=("discount_pct","mean"),
    return_rate=("returned","mean"),
    avg_rating=("rating","mean"),
    avg_delivery_days=("delivery_days","mean")
).reset_index()

ticket_agg = tickets.groupby(
    "customer_id"
).agg(
    ticket_count=("ticket_id","count"),
    avg_resolution=("resolution_hours","mean"),
    avg_sentiment=("sentiment_score","mean"),
    reopened_rate=("reopened","mean")
).reset_index()

df = (
    customers
    .merge(order_agg,on="customer_id",how="left")
    .merge(ticket_agg,on="customer_id",how="left")
    .merge(events,on="customer_id",how="left")
    .merge(campaigns,on="customer_id",how="left")
    .merge(labels,on="customer_id",how="left")
)


numeric_cols = df.select_dtypes(
    include=np.number
).columns

df[numeric_cols] = (
    df[numeric_cols]
    .fillna(0)
)


plt.figure(figsize=(6,4))
sns.countplot(
    x="churn_next_60d",
    data=df
)
plt.title("Churn Distribution")
save_plot("churn_distribution")

print(
    df["churn_next_60d"]
    .value_counts(normalize=True)
)


plt.figure(figsize=(6,4))
sns.countplot(
    x="city_tier",
    data=df
)
plt.title("City Tier")
save_plot("city_tier")

plt.figure(figsize=(6,4))
sns.countplot(
    x="age_group",
    data=df
)
plt.title("Age Group")
save_plot("age_group")

plt.figure(figsize=(10,4))
sns.countplot(
    y="acquisition_channel",
    data=df
)
plt.title("Acquisition Channel")
save_plot("acquisition_channel")


plt.figure(figsize=(8,5))
orders_clean['category'].value_counts().plot(kind='bar')
plt.title('Orders by Product Category')
plt.ylabel('Number of Orders')
save_plot("orders_by_category")

print(
    orders_clean['category']
    .value_counts()
    .reset_index()
)


plt.figure(figsize=(8,4))
sns.histplot(
    df["total_orders"],
    bins=30
)
plt.title("Total Orders")
save_plot("total_orders")

plt.figure(figsize=(8,4))
sns.histplot(
    df["total_spend"],
    bins=30
)
plt.title("Total Spend")
save_plot("total_spend")


plt.figure(figsize=(7,4))
sns.boxplot(
    x="churn_next_60d",
    y="sessions_30d",
    data=df
)
plt.title("Sessions vs Churn")
save_plot("sessions_vs_churn")

plt.figure(figsize=(7,4))
sns.boxplot(
    x="churn_next_60d",
    y="last_visit_days_ago",
    data=df
)
plt.title("Last Visit vs Churn")
save_plot("last_visit_vs_churn")


plt.figure(figsize=(8,5))
sns.histplot(orders_clean['discount_pct'], bins=20)
plt.title('Discount Distribution')
save_plot("discount_distribution")

orders_clean['discount_pct'].describe()

plt.figure(figsize=(8,5))
sns.boxplot(x=orders_clean['delivery_days'])
plt.title('Delivery Time Distribution')
save_plot("delivery_time")

orders_clean['delivery_days'].describe()

plt.figure(figsize=(8,5))
orders_clean['rating'].value_counts().sort_index().plot(kind='bar')

plt.title('Customer Ratings')
plt.xlabel('Rating')
plt.ylabel('Count')
save_plot("customer_ratings")

orders_clean['rating'].describe()


return_rate = orders_clean['returned'].mean()*100

print(f"Overall Return Rate: {return_rate:.2f}%")

sns.countplot(x='returned', data=orders_clean)
plt.title('Returned vs Non-Returned Orders')
save_plot("returned_vs_nonreturned")


plt.figure(figsize=(10,5))
tickets['issue_type'].value_counts().plot(kind='bar')

plt.title('Support Ticket Issue Types')
plt.ylabel('Count')
save_plot("ticket_issue_types")

print(
    tickets['issue_type']
    .value_counts()
    .reset_index()
)


reopened_rate = tickets['reopened'].mean()*100

print(f"Reopened Ticket Rate: {reopened_rate:.2f}%")

sns.countplot(x='reopened', data=tickets)
plt.title('Reopened Tickets')
save_plot("reopened_tickets")


print("\n" + "="*70)
print("CHURN HYPOTHESIS ANALYSIS")
print("="*70)



# FOUR CHURN HYPOTHESES TABLES

print("\n" + "="*70)
print("HYPOTHESIS 1: LOWER ENGAGEMENT -> HIGHER CHURN")
print("="*70)

print(
    df.groupby("churn_next_60d")["sessions_30d"]
    .mean()
    .round(2)
    .reset_index()
)


print("\n" + "="*70)
print("HYPOTHESIS 2: LONGER INACTIVITY -> HIGHER CHURN")
print("="*70)

print(
    df.groupby("churn_next_60d")["last_visit_days_ago"]
    .mean()
    .round(2)
    .reset_index()
)

print("\n" + "="*70)
print("HYPOTHESIS 3: LOWER PURCHASE FREQUENCY -> HIGHER CHURN")
print("="*70)

print(
    df.groupby("churn_next_60d")["total_orders"]
    .mean()
    .round(2)
    .reset_index()
)

print("\n" + "="*70)
print("HYPOTHESIS 4: LOWER WISHLIST ACTIVITY -> HIGHER CHURN")
print("="*70)

print(
    df.groupby("churn_next_60d")["wishlist_adds_30d"]
    .mean()
    .round(2)
    .reset_index()
)

print("\n" + "="*70)
print("HYPOTHESIS 5: HIGHER SUPPORT TICKETS -> HIGHER CHURN")
print("="*70)

print(
    df.groupby("churn_next_60d")["ticket_count"]
    .mean()
    .round(2)
    .reset_index()
)

print("\n" + "="*70)
print("EDA COMPLETE")
print("="*70)