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


# =========================================================
# HEADER + REFRESH BUTTON
# =========================================================

header_col1, header_col2 = st.columns([6, 1])

with header_col1:
    st.title("📊 Subscription Analytics Dashboard")

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

text_columns = [
    "App",
    "Month",
    "Partner Type",
    "Partner",
    "Agency",
    "Campaign",
    "gwprovider",
    "devicetype",
    "Week"
]

for column in text_columns:
    df[column] = (
        df[column]
        .fillna("")
        .astype(str)
        .str.strip()
    )


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
        [
            x for x in df["App"].dropna().unique()
            if x != ""
        ]
    )

    app_filter = st.multiselect(
        "App",
        options=app_options,
        default=[],
        placeholder="All"
    )


# ---------------------------------------------------------
# DATE
# Uses CREATED
# Latest date first
# Multiple dates allowed
# ---------------------------------------------------------

with col2:

    date_options = sorted(
        df["created"]
        .dropna()
        .dt.date
        .unique()
        .tolist(),
        reverse=True
    )

    date_filter = st.multiselect(
        "Date",
        options=date_options,
        default=[],
        format_func=lambda x: x.strftime("%d %b %Y"),
        placeholder="All"
    )


# ---------------------------------------------------------
# CREATED
# Calendar date range
# ---------------------------------------------------------

with col3:

    created_option = st.selectbox(
        "Created",
        ["- Select -", "Select Date Range"]
    )

    created_start = None
    created_end = None

    if created_option == "Select Date Range":

        date_range = st.date_input(
            "Created Range",
            value=None,
            min_value=df["created"].min().date(),
            max_value=df["created"].max().date(),
            format="DD/MM/YYYY",
            key="created_range"
        )

        if isinstance(date_range, tuple):

            if len(date_range) == 2:
                created_start = date_range[0]
                created_end = date_range[1]

            elif len(date_range) == 1:
                created_start = date_range[0]


# ---------------------------------------------------------
# MONTH
# ---------------------------------------------------------

with col4:

    month_options = sorted(
        [
            x for x in df["Month"].unique()
            if x != ""
        ]
    )

    month_filter = st.multiselect(
        "Month",
        options=month_options,
        default=[],
        placeholder="All"
    )


# ---------------------------------------------------------
# PARTNER TYPE
# ---------------------------------------------------------

with col5:

    partner_type_options = sorted(
        [
            x for x in df["Partner Type"].unique()
            if x != ""
        ]
    )

    partner_type_filter = st.multiselect(
        "Partner Type",
        options=partner_type_options,
        default=[],
        placeholder="All"
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
        [
            x for x in df["Partner"].unique()
            if x != ""
        ]
    )

    partner_filter = st.multiselect(
        "Partner",
        options=partner_options,
        default=[],
        placeholder="All"
    )


# ---------------------------------------------------------
# AGENCY
# ---------------------------------------------------------

with col7:

    agency_options = sorted(
        [
            x for x in df["Agency"].unique()
            if x != ""
        ]
    )

    agency_filter = st.multiselect(
        "Agency",
        options=agency_options,
        default=[],
        placeholder="All"
    )


# ---------------------------------------------------------
# CAMPAIGN
# ---------------------------------------------------------

with col8:

    campaign_options = sorted(
        [
            x for x in df["Campaign"].unique()
            if x != ""
        ]
    )

    campaign_filter = st.multiselect(
        "Campaign",
        options=campaign_options,
        default=[],
        placeholder="All"
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

    plan_filter = st.multiselect(
        "Plan",
        options=plan_options,
        default=[],
        format_func=lambda x: f"{x:g}",
        placeholder="All"
    )


# ---------------------------------------------------------
# CURRENCY
# ---------------------------------------------------------

with col10:

    currency_options = sorted(
        [
            x for x in df["currency"].unique()
            if x != ""
        ]
    )

    currency_filter = st.multiselect(
        "Currency",
        options=currency_options,
        default=[],
        placeholder="All"
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
        [
            x for x in df["gwprovider"].unique()
            if x != ""
        ]
    )

    gwprovider_filter = st.multiselect(
        "Gwprovider",
        options=gwprovider_options,
        default=[],
        placeholder="All"
    )


# ---------------------------------------------------------
# DEVICE TYPE
# ---------------------------------------------------------

with col12:

    device_options = sorted(
        [
            x for x in df["devicetype"].unique()
            if x != ""
        ]
    )

    device_filter = st.multiselect(
        "devicetype",
        options=device_options,
        default=[],
        placeholder="All"
    )


# ---------------------------------------------------------
# WEEK
# ---------------------------------------------------------

with col13:

    week_options = sorted(
        [
            x for x in df["Week"].unique()
            if x != ""
        ]
    )

    week_filter = st.multiselect(
        "Week",
        options=week_options,
        default=[],
        placeholder="All"
    )


# ---------------------------------------------------------
# STATUS
# Uses TRANSACTIONPURPOSE
# ---------------------------------------------------------

with col14:

    status_options = sorted(
        [
            x for x in df["transactionpurpose"].unique()
            if x != ""
        ]
    )

    status_filter = st.multiselect(
        "Status",
        options=status_options,
        default=[],
        placeholder="All"
    )



# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()


# ---------------------------------------------------------
# APP
# Multiple selection = OR
# ---------------------------------------------------------

if app_filter:

    filtered_df = filtered_df[
        filtered_df["App"].isin(app_filter)
    ]


# ---------------------------------------------------------
# DATE
# Uses CREATED
# Multiple selection = OR
# ---------------------------------------------------------

if date_filter:

    filtered_df = filtered_df[
        filtered_df["created"].dt.date.isin(date_filter)
    ]


# ---------------------------------------------------------
# CREATED RANGE
# ---------------------------------------------------------

# ---------------------------------------------------------
# CREATED RANGE
# Uses CREATED column
# ---------------------------------------------------------

if created_start is not None and created_end is not None:

    start_date = pd.Timestamp(created_start)
    end_date = pd.Timestamp(created_end)

    filtered_df = filtered_df[
        (filtered_df["created"] >= start_date) &
        (filtered_df["created"] < end_date + pd.Timedelta(days=1))
    ]

# ---------------------------------------------------------
# MONTH
# ---------------------------------------------------------

if month_filter:

    filtered_df = filtered_df[
        filtered_df["Month"].isin(month_filter)
    ]


# ---------------------------------------------------------
# PARTNER TYPE
# ---------------------------------------------------------

if partner_type_filter:

    filtered_df = filtered_df[
        filtered_df["Partner Type"].isin(
            partner_type_filter
        )
    ]


# ---------------------------------------------------------
# PARTNER
# ---------------------------------------------------------

if partner_filter:

    filtered_df = filtered_df[
        filtered_df["Partner"].isin(
            partner_filter
        )
    ]


# ---------------------------------------------------------
# AGENCY
# ---------------------------------------------------------

if agency_filter:

    filtered_df = filtered_df[
        filtered_df["Agency"].isin(
            agency_filter
        )
    ]


# ---------------------------------------------------------
# CAMPAIGN
# ---------------------------------------------------------

if campaign_filter:

    filtered_df = filtered_df[
        filtered_df["Campaign"].isin(
            campaign_filter
        )
    ]


# ---------------------------------------------------------
# PLAN
# ---------------------------------------------------------

if plan_filter:

    filtered_df = filtered_df[
        filtered_df["Plan"].isin(
            plan_filter
        )
    ]


# ---------------------------------------------------------
# CURRENCY
# ---------------------------------------------------------

if currency_filter:

    filtered_df = filtered_df[
        filtered_df["currency"].isin(
            currency_filter
        )
    ]


# ---------------------------------------------------------
# GWPROVIDER
# ---------------------------------------------------------

if gwprovider_filter:

    filtered_df = filtered_df[
        filtered_df["gwprovider"].isin(
            gwprovider_filter
        )
    ]


# ---------------------------------------------------------
# DEVICE
# ---------------------------------------------------------

if device_filter:

    filtered_df = filtered_df[
        filtered_df["devicetype"].isin(
            device_filter
        )
    ]


# ---------------------------------------------------------
# WEEK
# ---------------------------------------------------------

if week_filter:

    filtered_df = filtered_df[
        filtered_df["Week"].isin(
            week_filter
        )
    ]


# ---------------------------------------------------------
# STATUS
# Uses TRANSACTIONPURPOSE
# ---------------------------------------------------------

if status_filter:

    filtered_df = filtered_df[
        filtered_df["transactionpurpose"].isin(
            status_filter
        )
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
# INR ONLY + PLAN
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
