import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Subscription Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Subscription Analytics Dashboard")


# =========================================================
# CONNECT TO GOOGLE SHEETS
# =========================================================

conn = st.connection(
    "gsheets",
    type=GSheetsConnection
)

df = conn.read(
    worksheet="payment report(combined)",
    ttl=600
)


# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

df.columns = df.columns.str.strip()


# =========================================================
# CLEAN IMPORTANT COLUMNS
# =========================================================

df["transactionpurpose"] = (
    df["transactionpurpose"]
    .astype(str)
    .str.strip()
    .str.upper()
)

df["currency"] = (
    df["currency"]
    .astype(str)
    .str.strip()
    .str.upper()
)

df["App"] = df["App"].astype(str).str.strip()
df["Month"] = df["Month"].astype(str).str.strip()
df["Partner Type"] = df["Partner Type"].astype(str).str.strip()
df["Partner"] = df["Partner"].astype(str).str.strip()
df["Agency"] = df["Agency"].astype(str).str.strip()
df["Campaign"] = df["Campaign"].astype(str).str.strip()
df["gwprovider"] = df["gwprovider"].astype(str).str.strip()
df["devicetype"] = df["devicetype"].astype(str).str.strip()
df["Week"] = df["Week"].astype(str).str.strip()


# =========================================================
# PLAN
# =========================================================

df["Plan"] = pd.to_numeric(
    df["Plan"],
    errors="coerce"
).fillna(0)


# =========================================================
# CREATED DATE
# =========================================================

df["created"] = pd.to_datetime(
    df["created"],
    errors="coerce"
)


# =========================================================
# FILTER SECTION
# =========================================================

st.subheader("Filters")


# =========================================================
# ROW 1
# App | Date | Created | Month | Partner Type
# =========================================================

col1, col2, col3, col4, col5 = st.columns(5)


# ---------------------------------------------------------
# APP
# ---------------------------------------------------------

with col1:

    app_options = sorted(
        df["App"]
        .dropna()
        .unique()
        .tolist()
    )

    app_filter = st.selectbox(
        "App",
        ["All"] + app_options
    )


# ---------------------------------------------------------
# DATE
# Specific date from CREATED column
# ---------------------------------------------------------

with col2:

    date_options = sorted(
        df["created"]
        .dropna()
        .dt.date
        .unique()
        .tolist()
    )

    date_filter = st.selectbox(
        "Date",
        ["All"] + date_options
    )


# ---------------------------------------------------------
# CREATED
# Calendar date range from CREATED column
# ---------------------------------------------------------

with col3:

    if df["created"].notna().any():

        min_created = df["created"].min().date()
        max_created = df["created"].max().date()

        created_range = st.date_input(
            "Created",
            value=(min_created, max_created),
            min_value=min_created,
            max_value=max_created
        )

    else:

        created_range = ()


# ---------------------------------------------------------
# MONTH
# ---------------------------------------------------------

with col4:

    month_options = sorted(
        df["Month"]
        .dropna()
        .unique()
        .tolist()
    )

    month_filter = st.selectbox(
        "Month",
        ["All"] + month_options
    )


# ---------------------------------------------------------
# PARTNER TYPE
# ---------------------------------------------------------

with col5:

    partner_type_options = sorted(
        df["Partner Type"]
        .dropna()
        .unique()
        .tolist()
    )

    partner_type_filter = st.selectbox(
        "Partner Type",
        ["All"] + partner_type_options
    )


# =========================================================
# ROW 2
# Partner | Agency | Campaign | Plan | Currency
# =========================================================

col6, col7, col8, col9, col10 = st.columns(5)


# ---------------------------------------------------------
# PARTNER
# ---------------------------------------------------------

with col6:

    partner_options = sorted(
        df["Partner"]
        .dropna()
        .unique()
        .tolist()
    )

    partner_filter = st.selectbox(
        "Partner",
        ["All"] + partner_options
    )


# ---------------------------------------------------------
# AGENCY
# ---------------------------------------------------------

with col7:

    agency_options = sorted(
        df["Agency"]
        .dropna()
        .unique()
        .tolist()
    )

    agency_filter = st.selectbox(
        "Agency",
        ["All"] + agency_options
    )


# ---------------------------------------------------------
# CAMPAIGN
# ---------------------------------------------------------

with col8:

    campaign_options = sorted(
        df["Campaign"]
        .dropna()
        .unique()
        .tolist()
    )

    campaign_filter = st.selectbox(
        "Campaign",
        ["All"] + campaign_options
    )


# ---------------------------------------------------------
# PLAN
# ---------------------------------------------------------

with col9:

    plan_options = sorted(
        df["Plan"]
        .dropna()
        .unique()
        .tolist()
    )

    plan_filter = st.selectbox(
        "Plan",
        ["All"] + plan_options
    )


# ---------------------------------------------------------
# CURRENCY
# ---------------------------------------------------------

with col10:

    currency_options = sorted(
        df["currency"]
        .dropna()
        .unique()
        .tolist()
    )

    currency_filter = st.selectbox(
        "Currency",
        ["All"] + currency_options
    )


# =========================================================
# ROW 3
# Gwprovider | devicetype | Week | Status
# =========================================================

col11, col12, col13, col14 = st.columns(4)


# ---------------------------------------------------------
# GWPROVIDER
# ---------------------------------------------------------

with col11:

    gwprovider_options = sorted(
        df["gwprovider"]
        .dropna()
        .unique()
        .tolist()
    )

    gwprovider_filter = st.selectbox(
        "Gwprovider",
        ["All"] + gwprovider_options
    )


# ---------------------------------------------------------
# DEVICE TYPE
# ---------------------------------------------------------

with col12:

    device_options = sorted(
        df["devicetype"]
        .dropna()
        .unique()
        .tolist()
    )

    device_filter = st.selectbox(
        "devicetype",
        ["All"] + device_options
    )


# ---------------------------------------------------------
# WEEK
# ---------------------------------------------------------

with col13:

    week_options = sorted(
        df["Week"]
        .dropna()
        .unique()
        .tolist()
    )

    week_filter = st.selectbox(
        "Week",
        ["All"] + week_options
    )


# ---------------------------------------------------------
# STATUS
# IMPORTANT:
# STATUS USES TRANSACTIONPURPOSE
# ---------------------------------------------------------

with col14:

    status_options = sorted(
        df["transactionpurpose"]
        .dropna()
        .unique()
        .tolist()
    )

    status_filter = st.selectbox(
        "Status",
        ["All"] + status_options
    )


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()


# ---------------------------------------------------------
# APP
# ---------------------------------------------------------

if app_filter != "All":

    filtered_df = filtered_df[
        filtered_df["App"] == app_filter
    ]


# ---------------------------------------------------------
# DATE
# Uses CREATED
# ---------------------------------------------------------

if date_filter != "All":

    filtered_df = filtered_df[
        filtered_df["created"].dt.date == date_filter
    ]


# ---------------------------------------------------------
# CREATED RANGE
# Uses CREATED
# ---------------------------------------------------------

if len(created_range) == 2:

    start_date = created_range[0]
    end_date = created_range[1]

    filtered_df = filtered_df[
        (filtered_df["created"].dt.date >= start_date)
        &
        (filtered_df["created"].dt.date <= end_date)
    ]


# ---------------------------------------------------------
# MONTH
# ---------------------------------------------------------

if month_filter != "All":

    filtered_df = filtered_df[
        filtered_df["Month"] == month_filter
    ]


# ---------------------------------------------------------
# PARTNER TYPE
# ---------------------------------------------------------

if partner_type_filter != "All":

    filtered_df = filtered_df[
        filtered_df["Partner Type"] == partner_type_filter
    ]


# ---------------------------------------------------------
# PARTNER
# ---------------------------------------------------------

if partner_filter != "All":

    filtered_df = filtered_df[
        filtered_df["Partner"] == partner_filter
    ]


# ---------------------------------------------------------
# AGENCY
# ---------------------------------------------------------

if agency_filter != "All":

    filtered_df = filtered_df[
        filtered_df["Agency"] == agency_filter
    ]


# ---------------------------------------------------------
# CAMPAIGN
# ---------------------------------------------------------

if campaign_filter != "All":

    filtered_df = filtered_df[
        filtered_df["Campaign"] == campaign_filter
    ]


# ---------------------------------------------------------
# PLAN
# ---------------------------------------------------------

if plan_filter != "All":

    filtered_df = filtered_df[
        filtered_df["Plan"] == plan_filter
    ]


# ---------------------------------------------------------
# CURRENCY
# ---------------------------------------------------------

if currency_filter != "All":

    filtered_df = filtered_df[
        filtered_df["currency"] == currency_filter
    ]


# ---------------------------------------------------------
# GWPROVIDER
# ---------------------------------------------------------

if gwprovider_filter != "All":

    filtered_df = filtered_df[
        filtered_df["gwprovider"] == gwprovider_filter
    ]


# ---------------------------------------------------------
# DEVICE
# ---------------------------------------------------------

if device_filter != "All":

    filtered_df = filtered_df[
        filtered_df["devicetype"] == device_filter
    ]


# ---------------------------------------------------------
# WEEK
# ---------------------------------------------------------

if week_filter != "All":

    filtered_df = filtered_df[
        filtered_df["Week"] == week_filter
    ]


# ---------------------------------------------------------
# STATUS
# Uses TRANSACTIONPURPOSE
# ---------------------------------------------------------

if status_filter != "All":

    filtered_df = filtered_df[
        filtered_df["transactionpurpose"] == status_filter
    ]


# =========================================================
# KPI CALCULATIONS
# =========================================================

new_subscriptions = (
    filtered_df["transactionpurpose"] == "NEW"
).sum()


renew_subscriptions = (
    filtered_df["transactionpurpose"] == "RENEW"
).sum()


total_subscriptions = (
    new_subscriptions + renew_subscriptions
)


# =========================================================
# REVENUE
# INR ONLY
# PLAN COLUMN
# =========================================================

inr_data = filtered_df[
    filtered_df["currency"] == "INR"
]


total_revenue = inr_data["Plan"].sum()


# =========================================================
# KPI DISPLAY
# =========================================================

st.divider()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.metric(
        "Total Revenue (INR) (Gross)",
        f"₹{total_revenue:,.0f}"
    )


with kpi2:

    st.metric(
        "Total Subscriptions",
        f"{total_subscriptions:,}"
    )


with kpi3:

    st.metric(
        "New Subscriptions",
        f"{new_subscriptions:,}"
    )


with kpi4:

    st.metric(
        "Renew Subscriptions",
        f"{renew_subscriptions:,}"
    )


# =========================================================
# FILTERED ROW COUNT
# =========================================================

st.divider()

st.write(
    f"**Filtered rows:** {len(filtered_df):,}"
)
