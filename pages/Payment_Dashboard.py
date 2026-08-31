import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Payment Report",
    page_icon="💳",
    layout="wide"
)


# =========================================================
# HEADER + REFRESH BUTTON
# =========================================================

header_col1, header_col2 = st.columns([6, 1])

with header_col1:
    st.title("💳 Payment Report")

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
# LOAD PAYMENT DATA
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

df["currency"] = (
    df["currency"]
    .str.upper()
)

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

df["Net Revenue"] = pd.to_numeric(
    df["Net Revenue"],
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
# YEAR
# YEAR IS DERIVED FROM CREATED
# =========================================================

df["Year"] = df["created"].dt.year


# =========================================================
# FILTER SECTION
# =========================================================

st.subheader("Filters")


# =========================================================
# HELPER FUNCTION
# Applies all OTHER selected filters
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
    # CREATED DATE ONLY
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
    # CREATED
    # Uses CREATED column
    # -----------------------------------------------------

    if exclude != "created":

        selected = st.session_state.get(
            "created_filter",
            []
        )

        if selected:

            temp_df = temp_df[
                temp_df["created"].dt.date.isin(selected)
            ]


    # -----------------------------------------------------
    # TYPE
    # -----------------------------------------------------

    if exclude != "Type":

        selected = st.session_state.get(
            "type_filter",
            []
        )

        if selected:

            temp_df = temp_df[
                temp_df["Type"].isin(selected)
            ]


    return temp_df


# =========================================================
# ROW 1
# App | Year | Date | Month | Week
# =========================================================

col1, col2, col3, col4, col5 = st.columns(5)


# ---------------------------------------------------------
# APP
# ---------------------------------------------------------

with col1:

    app_options = sorted(
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
        options=app_options,
        key="app_filter",
        placeholder="All"
    )


# ---------------------------------------------------------
# YEAR
# ---------------------------------------------------------

with col2:

    year_options = sorted(
        get_context_df("Year")["Year"]
        .dropna()
        .astype(int)
        .unique()
        .tolist(),
        reverse=True
    )

    st.multiselect(
        "Year",
        options=year_options,
        key="year_filter",
        placeholder="All"
    )


# ---------------------------------------------------------
# DATE
# Uses CREATED
# Latest date first
# ---------------------------------------------------------

with col3:

    date_options = sorted(
        get_context_df("Date")["created"]
        .dropna()
        .dt.date
        .unique()
        .tolist(),
        reverse=True
    )

    st.multiselect(
        "Date",
        options=date_options,
        key="date_filter",
        format_func=lambda x: x.strftime("%d %b %Y"),
        placeholder="All"
    )


# ---------------------------------------------------------
# MONTH
# ---------------------------------------------------------

with col4:

    month_options = sorted(
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
        options=month_options,
        key="month_filter",
        placeholder="All"
    )


# ---------------------------------------------------------
# WEEK
# ---------------------------------------------------------

with col5:

    week_options = sorted(
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
        options=week_options,
        key="week_filter",
        placeholder="All"
    )


# =========================================================
# ROW 2
# Currency | Plan | Gwprovider | created | Type
# =========================================================

col6, col7, col8, col9, col10 = st.columns(5)


# ---------------------------------------------------------
# CURRENCY
# ---------------------------------------------------------

with col6:

    currency_options = sorted(
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
        options=currency_options,
        key="currency_filter",
        placeholder="All"
    )


# ---------------------------------------------------------
# PLAN
# ---------------------------------------------------------

with col7:

    plan_options = sorted(
        get_context_df("Plan")["Plan"]
        .dropna()
        .unique()
        .tolist()
    )

    st.multiselect(
        "Plan",
        options=plan_options,
        key="plan_filter",
        format_func=lambda x: f"{x:g}",
        placeholder="All"
    )


# ---------------------------------------------------------
# GWPROVIDER
# ---------------------------------------------------------

with col8:

    gwprovider_options = sorted(
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
        options=gwprovider_options,
        key="gwprovider_filter",
        placeholder="All"
    )


# ---------------------------------------------------------
# CREATED
# Uses CREATED column
# ---------------------------------------------------------

with col9:

    created_options = sorted(
        get_context_df("created")["created"]
        .dropna()
        .dt.date
        .unique()
        .tolist(),
        reverse=True
    )

    st.multiselect(
        "created",
        options=created_options,
        key="created_filter",
        format_func=lambda x: x.strftime("%d %b %Y"),
        placeholder="All"
    )


# ---------------------------------------------------------
# TYPE
# ---------------------------------------------------------

with col10:

    type_options = sorted(
        [
            x
            for x in get_context_df("Type")["Type"]
            .dropna()
            .unique()
            if x != ""
        ]
    )

    st.multiselect(
        "Type",
        options=type_options,
        key="type_filter",
        placeholder="All"
    )


# =========================================================
# FINAL FILTERED DATA
# =========================================================

filtered_df = get_context_df()


# =========================================================
# FILTERED ROW COUNT
# =========================================================

st.divider()

st.write(
    f"**Filtered rows:** {len(filtered_df):,}"
)

st.success(
    "Payment Report filters are working successfully ✅"
)
