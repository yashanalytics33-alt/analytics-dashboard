import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Subscription Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    .stApp {
        background-color: #f5f7fb;
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    [data-testid="stSidebar"] {
        background-color: #eef2f7;
    }


    /* =====================================================
       HEADER
       ===================================================== */

    .dashboard-title {
        font-size: 36px;
        font-weight: 800;
        color: #102a43;
        margin-bottom: 0px;
        letter-spacing: -1px;
    }

    .dashboard-subtitle {
        font-size: 15px;
        color: #627d98;
        margin-top: 2px;
        margin-bottom: 25px;
    }


    /* =====================================================
       SECTION HEADINGS
       ===================================================== */

    .section-title {
        font-size: 22px;
        font-weight: 750;
        color: #102a43;
        margin-top: 18px;
        margin-bottom: 12px;
    }

    .section-subtitle {
        font-size: 13px;
        color: #829ab1;
        margin-top: -7px;
        margin-bottom: 15px;
    }


    /* =====================================================
       FILTER BOX
       ===================================================== */

    .filter-container {
        background: white;
        border: 1px solid #e1e8f0;
        border-radius: 14px;
        padding: 20px 22px 8px 22px;
        margin-bottom: 28px;
        box-shadow: 0 2px 8px rgba(16, 42, 67, 0.05);
    }


    /* =====================================================
       KPI CARDS
       ===================================================== */

    .kpi-card {
        background: white;
        border: 1px solid #e1e8f0;
        border-radius: 14px;
        padding: 19px 20px;
        min-height: 118px;
        box-shadow: 0 3px 10px rgba(16, 42, 67, 0.06);
        transition: all 0.2s ease;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 18px rgba(16, 42, 67, 0.10);
    }

    .kpi-label {
        font-size: 13px;
        color: #627d98;
        font-weight: 500;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 29px;
        font-weight: 750;
        color: #102a43;
        line-height: 1.1;
    }

    .kpi-icon {
        font-size: 20px;
        margin-bottom: 8px;
    }


    /* =====================================================
       CHART CONTAINER
       ===================================================== */

    .chart-header {
        background: white;
        border: 1px solid #e1e8f0;
        border-radius: 14px 14px 0px 0px;
        padding: 15px 20px 5px 20px;
        margin-top: 10px;
        margin-bottom: -5px;
    }


    /* =====================================================
       FILTERED ROWS
       ===================================================== */

    .filtered-info {
        background: #edf2f7;
        border-radius: 8px;
        padding: 8px 12px;
        color: #486581;
        font-size: 13px;
        display: inline-block;
        margin-top: 10px;
        margin-bottom: 15px;
    }


    /* =====================================================
       STREAMLIT BUTTON
       ===================================================== */

    div.stButton > button {
        border-radius: 9px;
        border: 1px solid #d9e2ec;
        background-color: white;
        color: #102a43;
        font-weight: 600;
    }

    div.stButton > button:hover {
        border-color: #486581;
        color: #102a43;
    }


    /* =====================================================
       MULTISELECT
       ===================================================== */

    div[data-baseweb="select"] > div {
        border-radius: 9px;
        border-color: #d9e2ec;
        background-color: #f8fafc;
    }


    /* =====================================================
       DIVIDER
       ===================================================== */

    hr {
        border: none;
        border-top: 1px solid #e1e8f0;
        margin: 25px 0px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

header_col1, header_col2 = st.columns([7, 1])

with header_col1:

    st.markdown(
        """
        <div class="dashboard-title">
            📊 Campaign Dashboard
        </div>

        <div class="dashboard-subtitle">
            Subscription & Campaign Performance
        </div>
        """,
        unsafe_allow_html=True
    )


with header_col2:

    st.write("")

    if st.button(
        "🔄 Refresh",
        use_container_width=True
    ):
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

st.markdown(
    """
    <div class="section-title">
        🎛️ Filters
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FILTER CONTAINER START
# =========================================================

st.markdown(
    '<div class="filter-container">',
    unsafe_allow_html=True
)


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
    # DATE
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
    # PARTNER TYPE
    # -----------------------------------------------------

    if exclude != "Partner Type":

        selected = st.session_state.get(
            "partner_type_filter",
            []
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
            "partner_filter",
            []
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
            "agency_filter",
            []
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
            "campaign_filter",
            []
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
            "plan_filter",
            []
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
            "currency_filter",
            []
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
            "gwprovider_filter",
            []
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
            "device_filter",
            []
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
            "week_filter",
            []
        )

        if selected:

            temp_df = temp_df[
                temp_df["Week"].isin(selected)
            ]


    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    if exclude != "Status":

        selected = st.session_state.get(
            "status_filter",
            []
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
# DATE
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

with col3:

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
# PARTNER TYPE
# ---------------------------------------------------------

with col4:

    partner_type_options = sorted(
        [
            x
            for x in get_context_df("Partner Type")["Partner Type"]
            .dropna()
            .unique()
            if x != ""
        ]
    )

    st.multiselect(
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
            x
            for x in get_context_df("Partner")["Partner"]
            .dropna()
            .unique()
            if x != ""
        ]
    )

    st.multiselect(
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
            x
            for x in get_context_df("Agency")["Agency"]
            .dropna()
            .unique()
            if x != ""
        ]
    )

    st.multiselect(
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
            x
            for x in get_context_df("Campaign")["Campaign"]
            .dropna()
            .unique()
            if x != ""
        ]
    )

    st.multiselect(
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

    st.multiselect(
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
# GWPROVIDER
# ---------------------------------------------------------

with col10:

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


# =========================================================
# ROW 3
# Device Type | Week | Status
# =========================================================

col11, col12, col13 = st.columns([1, 1, 1])


# ---------------------------------------------------------
# DEVICE TYPE
# ---------------------------------------------------------

with col11:

    device_options = sorted(
        [
            x
            for x in get_context_df("devicetype")["devicetype"]
            .dropna()
            .unique()
            if x != ""
        ]
    )

    st.multiselect(
        "Device Type",
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


# ---------------------------------------------------------
# STATUS
# ---------------------------------------------------------

with col13:

    status_options = sorted(
        [
            x
            for x in get_context_df("Status")[
                "transactionpurpose"
            ]
            .dropna()
            .unique()
            if x != ""
        ]
    )

    st.multiselect(
        "Status",
        options=status_options,
        key="status_filter",
        placeholder="All"
    )


# =========================================================
# CLOSE FILTER CONTAINER
# =========================================================

st.markdown(
    "</div>",
    unsafe_allow_html=True
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
    new_subscriptions +
    renew_subscriptions
)


# =========================================================
# REVENUE
# INR ONLY
# =========================================================

inr_data = filtered_df[
    filtered_df["currency"] == "INR"
]


total_revenue = inr_data["Plan"].sum()


# =========================================================
# PERFORMANCE OVERVIEW
# =========================================================

st.markdown(
    """
    <div class="section-title">
        📈 Performance Overview
    </div>

    <div class="section-subtitle">
        Key subscription and revenue metrics based on the selected filters
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# KPI CARDS
# =========================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">💰</div>

            <div class="kpi-label">
                Total Revenue (INR)
            </div>

            <div class="kpi-value">
                ₹{total_revenue:,.0f}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with kpi2:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">👥</div>

            <div class="kpi-label">
                Total Subscriptions
            </div>

            <div class="kpi-value">
                {total_subscriptions:,}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with kpi3:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">🆕</div>

            <div class="kpi-label">
                New Subscriptions
            </div>

            <div class="kpi-value">
                {new_subscriptions:,}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with kpi4:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">🔄</div>

            <div class="kpi-label">
                Renew Subscriptions
            </div>

            <div class="kpi-value">
                {renew_subscriptions:,}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# FILTERED ROW COUNT
# =========================================================

st.markdown(
    f"""
    <div class="filtered-info">
        📄 <b>{len(filtered_df):,}</b> records matching current filters
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CHART SECTION TITLE
# =========================================================

st.markdown(
    """
    <div class="section-title">
        🤝 Partner Performance
    </div>

    <div class="section-subtitle">
        New and renewed subscription contribution by partner
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# NEW SUBSCRIPTIONS BY PARTNER
# =========================================================

new_partner_df = filtered_df[
    filtered_df["transactionpurpose"] == "NEW"
].copy()


new_partner = (
    new_partner_df
    .groupby("Partner")
    .size()
    .reset_index(name="Subscriptions")
    .sort_values(
        "Subscriptions",
        ascending=False
    )
)


if not new_partner.empty:

    fig_new_partner = px.pie(
        new_partner,
        names="Partner",
        values="Subscriptions",
        hole=0.42
    )

    fig_new_partner.update_traces(
        texttemplate="%{percent:.1%}",
        textposition="inside",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Subscriptions: %{value:,}<br>"
            "Contribution: %{percent:.1%}"
            "<extra></extra>"
        )
    )

    fig_new_partner.update_layout(
        title={
            "text": "New Subscriptions",
            "x": 0.03,
            "xanchor": "left"
        },
        legend_title_text="Partner",
        margin=dict(
            l=20,
            r=20,
            t=65,
            b=20
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            color="#102a43"
        )
    )

else:

    fig_new_partner = None


# =========================================================
# RENEWED SUBSCRIPTIONS BY PARTNER
# =========================================================

renew_partner_df = filtered_df[
    filtered_df["transactionpurpose"] == "RENEW"
].copy()


renew_partner = (
    renew_partner_df
    .groupby("Partner")
    .size()
    .reset_index(name="Subscriptions")
    .sort_values(
        "Subscriptions",
        ascending=False
    )
)


if not renew_partner.empty:

    fig_renew_partner = px.pie(
        renew_partner,
        names="Partner",
        values="Subscriptions",
        hole=0.42
    )

    fig_renew_partner.update_traces(
        texttemplate="%{percent:.1%}",
        textposition="inside",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Subscriptions: %{value:,}<br>"
            "Contribution: %{percent:.1%}"
            "<extra></extra>"
        )
    )

    fig_renew_partner.update_layout(
        title={
            "text": "Renewed Subscriptions",
            "x": 0.03,
            "xanchor": "left"
        },
        legend_title_text="Partner",
        margin=dict(
            l=20,
            r=20,
            t=65,
            b=20
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            color="#102a43"
        )
    )

else:

    fig_renew_partner = None


# =========================================================
# DISPLAY PARTNER CHARTS
# =========================================================

chart_col1, chart_col2 = st.columns(2)


with chart_col1:

    if fig_new_partner is not None:

        st.plotly_chart(
            fig_new_partner,
            use_container_width=True
        )

    else:

        st.info(
            "No new subscriptions for selected filters."
        )


with chart_col2:

    if fig_renew_partner is not None:

        st.plotly_chart(
            fig_renew_partner,
            use_container_width=True
        )

    else:

        st.info(
            "No renewed subscriptions for selected filters."
        )


# =========================================================
# PARTNER TYPE SECTION
# =========================================================

st.markdown(
    """
    <div class="section-title">
        🏷️ Partner Type Performance
    </div>

    <div class="section-subtitle">
        Subscription contribution across partner categories
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# NEW - PARTNER TYPE
# =========================================================

pt_new = filtered_df[
    filtered_df["transactionpurpose"] == "NEW"
]


pt_new = (
    pt_new
    .groupby("Partner Type")
    .size()
    .reset_index(name="Subscriptions")
)


if not pt_new.empty:

    chart_pt_new = px.pie(
        pt_new,
        names="Partner Type",
        values="Subscriptions",
        hole=0.42
    )

    chart_pt_new.update_traces(
        texttemplate="%{percent:.1%}",
        textposition="inside",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Subscriptions: %{value:,}<br>"
            "Contribution: %{percent:.1%}"
            "<extra></extra>"
        )
    )

    chart_pt_new.update_layout(
        title={
            "text": "New Subscriptions",
            "x": 0.03,
            "xanchor": "left"
        },
        legend_title_text="Partner Type",
        margin=dict(
            l=20,
            r=20,
            t=65,
            b=20
        ),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

else:

    chart_pt_new = None


# =========================================================
# RENEW - PARTNER TYPE
# =========================================================

pt_renew = filtered_df[
    filtered_df["transactionpurpose"] == "RENEW"
]


pt_renew = (
    pt_renew
    .groupby("Partner Type")
    .size()
    .reset_index(name="Subscriptions")
)


if not pt_renew.empty:

    chart_pt_renew = px.pie(
        pt_renew,
        names="Partner Type",
        values="Subscriptions",
        hole=0.42
    )

    chart_pt_renew.update_traces(
        texttemplate="%{percent:.1%}",
        textposition="inside",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Subscriptions: %{value:,}<br>"
            "Contribution: %{percent:.1%}"
            "<extra></extra>"
        )
    )

    chart_pt_renew.update_layout(
        title={
            "text": "Renewed Subscriptions",
            "x": 0.03,
            "xanchor": "left"
        },
        legend_title_text="Partner Type",
        margin=dict(
            l=20,
            r=20,
            t=65,
            b=20
        ),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

else:

    chart_pt_renew = None


# =========================================================
# DISPLAY PARTNER TYPE
# =========================================================

pt_col1, pt_col2 = st.columns(2)


with pt_col1:

    if chart_pt_new is not None:

        st.plotly_chart(
            chart_pt_new,
            use_container_width=True
        )

    else:

        st.info(
            "No new subscriptions."
        )


with pt_col2:

    if chart_pt_renew is not None:

        st.plotly_chart(
            chart_pt_renew,
            use_container_width=True
        )

    else:

        st.info(
            "No renewed subscriptions."
        )


# =========================================================
# AGENCY PERFORMANCE
# =========================================================

st.markdown(
    """
    <div class="section-title">
        🏢 Agency Performance
    </div>

    <div class="section-subtitle">
        New and renewed subscriptions generated through agencies
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# NEW SUBSCRIPTIONS BY AGENCY
# =========================================================

agency_new = filtered_df[
    (filtered_df["transactionpurpose"] == "NEW") &
    (filtered_df["Agency"].astype(str).str.strip() != "") &
    (filtered_df["Agency"].astype(str).str.strip() != "0")
].copy()


agency_new = (
    agency_new
    .groupby("Agency")
    .size()
    .reset_index(name="Subscriptions")
)


if not agency_new.empty:

    fig_agency_new = px.pie(
        agency_new,
        names="Agency",
        values="Subscriptions",
        hole=0.42
    )

    fig_agency_new.update_traces(
        texttemplate="%{percent:.1%}",
        textposition="inside",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Subscriptions: %{value:,}<br>"
            "Contribution: %{percent:.1%}"
            "<extra></extra>"
        )
    )

    fig_agency_new.update_layout(
        title={
            "text": "New Subscriptions",
            "x": 0.03,
            "xanchor": "left"
        },
        legend_title_text="Agency",
        margin=dict(
            l=20,
            r=20,
            t=65,
            b=20
        ),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

else:

    fig_agency_new = None


# =========================================================
# RENEWED SUBSCRIPTIONS BY AGENCY
# =========================================================

agency_renew = filtered_df[
    (filtered_df["transactionpurpose"] == "RENEW") &
    (filtered_df["Agency"].astype(str).str.strip() != "") &
    (filtered_df["Agency"].astype(str).str.strip() != "0")
].copy()


agency_renew = (
    agency_renew
    .groupby("Agency")
    .size()
    .reset_index(name="Subscriptions")
)


if not agency_renew.empty:

    fig_agency_renew = px.pie(
        agency_renew,
        names="Agency",
        values="Subscriptions",
        hole=0.42
    )

    fig_agency_renew.update_traces(
        texttemplate="%{percent:.1%}",
        textposition="inside",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Subscriptions: %{value:,}<br>"
            "Contribution: %{percent:.1%}"
            "<extra></extra>"
        )
    )

    fig_agency_renew.update_layout(
        title={
            "text": "Renewed Subscriptions",
            "x": 0.03,
            "xanchor": "left"
        },
        legend_title_text="Agency",
        margin=dict(
            l=20,
            r=20,
            t=65,
            b=20
        ),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

else:

    fig_agency_renew = None


# =========================================================
# DISPLAY AGENCY CHARTS
# =========================================================

agency_col1, agency_col2 = st.columns(2)


with agency_col1:

    if fig_agency_new is not None:

        st.plotly_chart(
            fig_agency_new,
            use_container_width=True
        )

    else:

        st.info(
            "No new subscriptions."
        )


with agency_col2:

    if fig_agency_renew is not None:

        st.plotly_chart(
            fig_agency_renew,
            use_container_width=True
        )

    else:

        st.info(
            "No renewed subscriptions."
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <hr>

    <div style="
        text-align:center;
        color:#829ab1;
        font-size:12px;
        padding:8px;
    ">
        Subscription Analytics Dashboard
    </div>
    """,
    unsafe_allow_html=True
)
