import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Payment Dashboard",
    page_icon="💳",
    layout="wide"
)


# =========================================================
# HEADER + REFRESH
# =========================================================

header_col1, header_col2 = st.columns([6, 1])

with header_col1:
    st.title("💳 Payment Dashboard")

with header_col2:
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()


# =========================================================
# GOOGLE SHEETS CONNECTION
# =========================================================

conn = st.connection(
    "gsheets",
    type=GSheetsConnection
)


# =========================================================
# LOAD DATA
# =========================================================

df = conn.read(
    worksheet="payment report(combined)",
    ttl=600
)


# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

df.columns = df.columns.str.strip()


# =========================================================
# CLEAN TEXT COLUMNS
# =========================================================

text_columns = [
    "App",
    "Month",
    "Type",
    "Plan Type",
    "Status",
    "Week",
    "currency",
    "gwprovider",
    "devicetype",
    "transactionpurpose",
    "paymentstatus",
    "transactionstatus",
    "transactionmode",
    "initiatedby",
    "reason",
    "errorcode"
]

for column in text_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )


# =========================================================
# STANDARDIZE TEXT
# =========================================================

if "currency" in df.columns:

    df["currency"] = (
        df["currency"]
        .str.upper()
    )


if "transactionpurpose" in df.columns:

    df["transactionpurpose"] = (
        df["transactionpurpose"]
        .str.upper()
    )


# =========================================================
# NUMERIC COLUMNS
# =========================================================

df["Plan"] = pd.to_numeric(
    df["Plan"],
    errors="coerce"
).fillna(0)


df["amount"] = pd.to_numeric(
    df["amount"],
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
# YEAR FROM CREATED
# =========================================================

df["Year"] = df["created"].dt.year


# =========================================================
# FILTER SECTION
# =========================================================

st.subheader("Filters")


# =========================================================
# HELPER FUNCTION
# =========================================================

def get_context_df(exclude=None):

    temp_df = df.copy()

    # -----------------------------------------------------
    # APP
    # -----------------------------------------------------

    if exclude != "App":

        selected = st.session_state.get(
            "app_filter",
            []
        )

        if selected:

            temp_df = temp_df[
                temp_df["App"].isin(selected)
            ]


    # -----------------------------------------------------
    # YEAR
    # -----------------------------------------------------

    if exclude != "Year":

        selected = st.session_state.get(
            "year_filter",
            []
        )

        if selected:

            temp_df = temp_df[
                temp_df["Year"].isin(selected)
            ]


    # -----------------------------------------------------
    # DATE
    # CREATED ONLY
    # -----------------------------------------------------

    if exclude != "Date":

        selected = st.session_state.get(
            "date_filter",
            []
        )

        if selected:

            temp_df = temp_df[
                temp_df["created"].dt.date.isin(selected)
            ]


    # -----------------------------------------------------
    # MONTH
    # -----------------------------------------------------

    if exclude != "Month":

        selected = st.session_state.get(
            "month_filter",
            []
        )

        if selected:

            temp_df = temp_df[
                temp_df["Month"].isin(selected)
            ]


    # -----------------------------------------------------
    # WEEK
    # -----------------------------------------------------

    if exclude != "Week":

        selected = st.session_state.get(
            "week_filter",
            []
        )

        if selected:

            temp_df = temp_df[
                temp_df["Week"].isin(selected)
            ]


    # -----------------------------------------------------
    # CURRENCY
    # -----------------------------------------------------

    if exclude != "Currency":

        selected = st.session_state.get(
            "currency_filter",
            []
        )

        if selected:

            temp_df = temp_df[
                temp_df["currency"].isin(selected)
            ]


    # -----------------------------------------------------
    # PLAN
    # -----------------------------------------------------

    if exclude != "Plan":

        selected = st.session_state.get(
            "plan_filter",
            []
        )

        if selected:

            temp_df = temp_df[
                temp_df["Plan"].isin(selected)
            ]


    # -----------------------------------------------------
    # GWPROVIDER
    # -----------------------------------------------------

    if exclude != "Gwprovider":

        selected = st.session_state.get(
            "gwprovider_filter",
            []
        )

        if selected:

            temp_df = temp_df[
                temp_df["gwprovider"].isin(selected)
            ]


    # -----------------------------------------------------
    # TYPE
    # TYPE COMES FROM TRANSACTIONPURPOSE
    # -----------------------------------------------------

    if exclude != "Type":

        selected = st.session_state.get(
            "type_filter",
            []
        )

        if selected:

            temp_df = temp_df[
                temp_df["transactionpurpose"].isin(selected)
            ]


    return temp_df

# =========================================================
# ROW 1
# APP | YEAR | DATE | MONTH | WEEK
# =========================================================

col1, col2, col3, col4, col5 = st.columns(5)


# =========================================================
# APP
# =========================================================

with col1:

    options = sorted(
        [
            x
            for x in get_context_df("App")["App"]
            .dropna()
            .unique()
            if x != ""
        ]
    )

    st.multiselect(
        "App",
        options=options,
        key="app_filter",
        placeholder="All"
    )


# =========================================================
# YEAR
# =========================================================

with col2:

    options = sorted(
        get_context_df("Year")["Year"]
        .dropna()
        .astype(int)
        .unique()
        .tolist(),
        reverse=True
    )

    st.multiselect(
        "Year",
        options=options,
        key="year_filter",
        placeholder="All"
    )


# =========================================================
# DATE
# =========================================================

with col3:

    options = sorted(
        get_context_df("Date")["created"]
        .dropna()
        .dt.date
        .unique()
        .tolist(),
        reverse=True
    )

    st.multiselect(
        "Date",
        options=options,
        key="date_filter",
        format_func=lambda x: x.strftime("%d %b %Y"),
        placeholder="All"
    )


# =========================================================
# MONTH
# =========================================================

with col4:

    options = sorted(
        [
            x
            for x in get_context_df("Month")["Month"]
            .dropna()
            .unique()
            if x != ""
        ]
    )

    st.multiselect(
        "Month",
        options=options,
        key="month_filter",
        placeholder="All"
    )


# =========================================================
# WEEK
# =========================================================

with col5:

    options = sorted(
        [
            x
            for x in get_context_df("Week")["Week"]
            .dropna()
            .unique()
            if x != ""
        ]
    )

    st.multiselect(
        "Week",
        options=options,
        key="week_filter",
        placeholder="All"
    )


# =========================================================
# ROW 2
# CURRENCY | PLAN | GWPROVIDER | CREATED | TYPE
# =========================================================

col6, col7, col8, col9, col10 = st.columns(5)


# =========================================================
# CURRENCY
# =========================================================

with col6:

    options = sorted(
        [
            x
            for x in get_context_df("Currency")["currency"]
            .dropna()
            .unique()
            if x != ""
        ]
    )

    st.multiselect(
        "Currency",
        options=options,
        key="currency_filter",
        placeholder="All"
    )


# =========================================================
# PLAN
# =========================================================

with col7:

    options = sorted(
        get_context_df("Plan")["Plan"]
        .dropna()
        .unique()
        .tolist()
    )

    st.multiselect(
        "Plan",
        options=options,
        key="plan_filter",
        format_func=lambda x: f"{x:g}",
        placeholder="All"
    )


# =========================================================
# GWPROVIDER
# =========================================================

with col8:

    options = sorted(
        [
            x
            for x in get_context_df("Gwprovider")["gwprovider"]
            .dropna()
            .unique()
            if x != ""
        ]
    )

    st.multiselect(
        "Gwprovider",
        options=options,
        key="gwprovider_filter",
        placeholder="All"
    )

# =========================================================
# TYPE
# Uses transactionpurpose column
# =========================================================

with col9:

    options = sorted(
        [
            x
            for x in get_context_df("Type")["transactionpurpose"]
            .dropna()
            .unique()
            if x != ""
        ]
    )

    st.multiselect(
        "Type",
        options=options,
        key="type_filter",
        placeholder="All"
    )


# =========================================================
# FINAL FILTERED DATA
# =========================================================

filtered_df = get_context_df()


# =========================================================
# KPI CALCULATIONS
# =========================================================

# Total subscriptions

total_subscriptions = len(filtered_df)


# New subscriptions

new_subscriptions = (
    filtered_df["transactionpurpose"] == "NEW"
).sum()


# Renew subscriptions

renew_subscriptions = (
    filtered_df["transactionpurpose"] == "RENEW"
).sum()


# =========================================================
# REVENUE
# INR GROSS
# =========================================================

inr_data = filtered_df[
    filtered_df["currency"] == "INR"
]


total_revenue = inr_data["Plan"].sum()


# =========================================================
# ACTIVE / EXPIRED
# =========================================================

active_subscribers = 0
expired_subscribers = 0

if "Status" in filtered_df.columns:

    active_subscribers = (
        filtered_df["Status"]
        .astype(str)
        .str.upper()
        .eq("ACTIVE")
        .sum()
    )

    expired_subscribers = (
        filtered_df["Status"]
        .astype(str)
        .str.upper()
        .eq("EXPIRED")
        .sum()
    )


# =========================================================
# KPI SECTION
# =========================================================

st.divider()


kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)


# ---------------------------------------------------------
# TOTAL REVENUE
# ---------------------------------------------------------

with kpi1:

    st.metric(
        "Total Revenue (INR) (Gross)",
        f"₹{total_revenue:,.0f}"
    )


# ---------------------------------------------------------
# TOTAL SUBSCRIPTIONS
# ---------------------------------------------------------

with kpi2:

    st.metric(
        "Total Subscriptions",
        f"{total_subscriptions:,}"
    )


# ---------------------------------------------------------
# NEW SUBSCRIPTIONS
# ---------------------------------------------------------

with kpi3:

    st.metric(
        "New Subscriptions",
        f"{new_subscriptions:,}"
    )


# ---------------------------------------------------------
# RENEW SUBSCRIPTIONS
# ---------------------------------------------------------

with kpi4:

    st.metric(
        "Renewed Subscriptions",
        f"{renew_subscriptions:,}"
    )


# ---------------------------------------------------------
# ACTIVE
# ---------------------------------------------------------

with kpi5:

    st.metric(
        "Active Subscribers",
        f"{active_subscribers:,}"
    )


# ---------------------------------------------------------
# EXPIRED
# ---------------------------------------------------------

with kpi6:

    st.metric(
        "Expired Subscribers",
        f"{expired_subscribers:,}"
    )


# =========================================================
# FILTERED ROW COUNT
# =========================================================

st.divider()

st.write(
    f"**Filtered rows:** {len(filtered_df):,}"
)
