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
# HELPER FUNCTION
# Creates data based on all OTHER selected filters
# =========================================================

def get_context_df(exclude=None):

    temp_df = df.copy()

    # -----------------------------------------------------
    # APP
    # -----------------------------------------------------
    if exclude != "App":
        selected = st.session_state.get("app_filter", [])
        if selected:
            temp_df = temp_df[
                temp_df["App"].isin(selected)
            ]

    # -----------------------------------------------------
    # DATE
    # Uses CREATED column
    # -----------------------------------------------------
    if exclude != "Date":
        selected = st.session_state.get("date_filter", [])
        if selected:
            temp_df = temp_df[
                temp_df["created"].dt.date.isin(selected)
            ]

    # -----------------------------------------------------
    # MONTH
    # -----------------------------------------------------
    if exclude != "Month":
        selected = st.session_state.get("month_filter", [])
        if selected:
            temp_df = temp_df[
                temp_df["Month"].isin(selected)
            ]

    # -----------------------------------------------------
    # PARTNER TYPE
    # -----------------------------------------------------
    if exclude != "Partner Type":
        selected = st.session_state.get(
            "partner_type_filter", []
        )
        if selected:
            temp_df = temp_df[
                temp_df["Partner Type"].isin(selected)
            ]

    # -----------------------------------------------------
    # PARTNER
    # -----------------------------------------------------
    if exclude != "Partner":
        selected = st.session_state.get(
            "partner_filter", []
        )
        if selected:
            temp_df = temp_df[
                temp_df["Partner"].isin(selected)
            ]

    # -----------------------------------------------------
    # AGENCY
    # -----------------------------------------------------
    if exclude != "Agency":
        selected = st.session_state.get(
            "agency_filter", []
        )
        if selected:
            temp_df = temp_df[
                temp_df["Agency"].isin(selected)
            ]

    # -----------------------------------------------------
    # CAMPAIGN
    # -----------------------------------------------------
    if exclude != "Campaign":
        selected = st.session_state.get(
            "campaign_filter", []
        )
        if selected:
            temp_df = temp_df[
                temp_df["Campaign"].isin(selected)
            ]

    # -----------------------------------------------------
    # PLAN
    # -----------------------------------------------------
    if exclude != "Plan":
        selected = st.session_state.get(
            "plan_filter", []
        )
        if selected:
            temp_df = temp_df[
                temp_df["Plan"].isin(selected)
            ]

    # -----------------------------------------------------
    # CURRENCY
    # -----------------------------------------------------
    if exclude != "Currency":
        selected = st.session_state.get(
            "currency_filter", []
        )
        if selected:
            temp_df = temp_df[
                temp_df["currency"].isin(selected)
            ]

    # -----------------------------------------------------
    # GWPROVIDER
    # -----------------------------------------------------
    if exclude != "Gwprovider":
        selected = st.session_state.get(
            "gwprovider_filter", []
        )
        if selected:
            temp_df = temp_df[
                temp_df["gwprovider"].isin(selected)
            ]

    # -----------------------------------------------------
    # DEVICE TYPE
    # -----------------------------------------------------
    if exclude != "devicetype":
        selected = st.session_state.get(
            "device_filter", []
        )
        if selected:
            temp_df = temp_df[
                temp_df["devicetype"].isin(selected)
            ]

    # -----------------------------------------------------
    # WEEK
    # -----------------------------------------------------
    if exclude != "Week":
        selected = st.session_state.get(
            "week_filter", []
        )
        if selected:
            temp_df = temp_df[
                temp_df["Week"].isin(selected)
            ]

    # -----------------------------------------------------
    # STATUS
    # Uses TRANSACTIONPURPOSE
    # -----------------------------------------------------
    if exclude != "Status":
        selected = st.session_state.get(
            "status_filter", []
        )
        if selected:
            temp_df = temp_df[
                temp_df["transactionpurpose"].isin(selected)
            ]

    return temp_df


# =========================================================
# ROW 1
# App | Date | Month | Partner Type | Partner
# =========================================================

col1, col2, col3, col4, col5 = st.columns(5)


# ---------------------------------------------------------
# APP
# ---------------------------------------------------------

with col1:

    app_options = sorted(
        [
            x for x in get_context_df("App")["App"].dropna().unique()
            if x != ""
        ]
    )

    app_filter = st.multiselect(
        "App",
        options=app_options,
        key="app_filter",
        placeholder="All"
    )


# ---------------------------------------------------------
# DATE
# Uses CREATED column
# Latest date first
# ---------------------------------------------------------

with col2:

    date_options = sorted(
        get_context_df("Date")["created"]
        .dropna()
        .dt.date
        .unique()
        .tolist(),
        reverse=True
    )

    date_filter = st.multiselect(
        "Date",
        options=date_options,
        key="date_filter",
        format_func=lambda x: x.strftime("%d %b %Y"),
        placeholder="All"
    )


# ---------------------------------------------------------
# MONTH
# ---------------------------------------------------------

with col3:

    month_options = sorted(
        [
            x for x in get_context_df("Month")["Month"].dropna().unique()
            if x != ""
        ]
    )

    month_filter = st.multiselect(
        "Month",
        options=month_options,
        key="month_filter",
        placeholder="All"
    )


# ---------------------------------------------------------
# PARTNER TYPE
# ---------------------------------------------------------

with col4:

    partner_type_options = sorted(
        [
            x for x in get_context_df("Partner Type")[
                "Partner Type"
            ].dropna().unique()
            if x != ""
        ]
    )

    partner_type_filter = st.multiselect(
        "Partner Type",
        options=partner_type_options,
        key="partner_type_filter",
        placeholder="All"
    )


# ---------------------------------------------------------
# PARTNER
# ---------------------------------------------------------

with col5:

    partner_options = sorted(
        [
            x for x in get_context_df("Partner")[
                "Partner"
            ].dropna().unique()
            if x != ""
        ]
    )

    partner_filter = st.multiselect(
        "Partner",
        options=partner_options,
        key="partner_filter",
        placeholder="All"
    )


# =========================================================
# ROW 2
# Agency | Campaign | Plan | Currency | Gwprovider
# =========================================================

col6, col7, col8, col9, col10 = st.columns(5)


# ---------------------------------------------------------
# AGENCY
# ---------------------------------------------------------

with col6:

    agency_options = sorted(
        [
            x for x in get_context_df("Agency")[
                "Agency"
            ].dropna().unique()
            if x != ""
        ]
    )

    agency_filter = st.multiselect(
        "Agency",
        options=agency_options,
        key="agency_filter",
        placeholder="All"
    )


# ---------------------------------------------------------
# CAMPAIGN
# ---------------------------------------------------------

with col7:

    campaign_options = sorted(
        [
            x for x in get_context_df("Campaign")[
                "Campaign"
            ].dropna().unique()
            if x != ""
        ]
    )

    campaign_filter = st.multiselect(
        "Campaign",
        options=campaign_options,
        key="campaign_filter",
        placeholder="All"
    )


# ---------------------------------------------------------
# PLAN
# ---------------------------------------------------------

with col8:

    plan_options = sorted(
        get_context_df("Plan")["Plan"]
        .dropna()
        .unique()
        .tolist()
    )

    plan_filter = st.multiselect(
        "Plan",
        options=plan_options,
        key="plan_filter",
        format_func=lambda x: f"{x:g}",
        placeholder="All"
    )


# ---------------------------------------------------------
# CURRENCY
# ---------------------------------------------------------

with col9:

    currency_options = sorted(
        [
            x for x in get_context_df("Currency")[
                "currency"
            ].dropna().unique()
            if x != ""
        ]
    )

    currency_filter = st.multiselect(
        "Currency",
        options=currency_options,
        key="currency_filter",
        placeholder="All"
    )


# ---------------------------------------------------------
# GWPROVIDER
# ---------------------------------------------------------

with col10:

    gwprovider_options = sorted(
        [
            x for x in get_context_df("Gwprovider")[
                "gwprovider"
            ].dropna().unique()
            if x != ""
        ]
    )

    gwprovider_filter = st.multiselect(
        "Gwprovider",
        options=gwprovider_options,
        key="gwprovider_filter",
        placeholder="All"
    )


# =========================================================
# ROW 3
# Device Type | Week | Status
# =========================================================

col11, col12, col13 = st.columns(3)


# ---------------------------------------------------------
# DEVICE TYPE
# ---------------------------------------------------------

with col11:

    device_options = sorted(
        [
            x for x in get_context_df("devicetype")[
                "devicetype"
            ].dropna().unique()
            if x != ""
        ]
    )

    device_filter = st.multiselect(
        "devicetype",
        options=device_options,
        key="device_filter",
        placeholder="All"
    )


# ---------------------------------------------------------
# WEEK
# ---------------------------------------------------------

with col12:

    week_options = sorted(
        [
            x for x in get_context_df("Week")[
                "Week"
            ].dropna().unique()
            if x != ""
        ]
    )

    week_filter = st.multiselect(
        "Week",
        options=week_options,
        key="week_filter",
        placeholder="All"
    )


# ---------------------------------------------------------
# STATUS
# Uses TRANSACTIONPURPOSE
# ---------------------------------------------------------

with col13:

    status_options = sorted(
        [
            x for x in get_context_df("Status")[
                "transactionpurpose"
            ].dropna().unique()
            if x != ""
        ]
    )

    status_filter = st.multiselect(
        "Status",
        options=status_options,
        key="status_filter",
        placeholder="All"
    )


# =========================================================
# FINAL FILTERED DATA
# =========================================================

filtered_df = get_context_df()



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

