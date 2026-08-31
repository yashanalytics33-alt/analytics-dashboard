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
# CUSTOM DESIGN
# =========================================================

st.markdown("""
<style>

/* -------------------------------------------------------
   MAIN BACKGROUND
------------------------------------------------------- */

.stApp {
    background-color: #f5f7fb;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}


/* -------------------------------------------------------
   HEADER
------------------------------------------------------- */

.dashboard-title {
    font-size: 34px;
    font-weight: 750;
    color: #102a43;
    margin-bottom: 2px;
}

.dashboard-subtitle {
    color: #627d98;
    font-size: 15px;
    margin-bottom: 25px;
}


/* -------------------------------------------------------
   SECTION TITLES
------------------------------------------------------- */

.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #102a43;
    margin-top: 22px;
    margin-bottom: 4px;
}

.section-subtitle {
    color: #829ab1;
    font-size: 14px;
    margin-bottom: 18px;
}


/* -------------------------------------------------------
   FILTER CONTAINER
------------------------------------------------------- */

.filter-box {
    background: white;
    border: 1px solid #e1e8f0;
    border-radius: 14px;
    padding: 18px 20px 8px 20px;
    box-shadow: 0 2px 8px rgba(16, 42, 67, 0.05);
    margin-bottom: 25px;
}


/* -------------------------------------------------------
   KPI CARDS
------------------------------------------------------- */

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e1e8f0;
    border-radius: 14px;
    padding: 20px 22px;
    box-shadow: 0 3px 10px rgba(16, 42, 67, 0.06);
    min-height: 125px;
}

[data-testid="stMetricLabel"] {
    color: #627d98 !important;
    font-size: 14px !important;
    font-weight: 550 !important;
}

[data-testid="stMetricValue"] {
    color: #102a43 !important;
    font-size: 28px !important;
    font-weight: 750 !important;
}


/* -------------------------------------------------------
   CHART CONTAINERS
------------------------------------------------------- */

.chart-card {
    background: white;
    border: 1px solid #e1e8f0;
    border-radius: 14px;
    padding: 8px;
    box-shadow: 0 3px 10px rgba(16, 42, 67, 0.05);
}


/* -------------------------------------------------------
   FILTERED ROW BADGE
------------------------------------------------------- */

.data-badge {
    display: inline-block;
    background: #eaf2ff;
    color: #2563eb;
    border-radius: 20px;
    padding: 7px 14px;
    font-size: 13px;
    font-weight: 600;
    margin-top: 5px;
}


/* -------------------------------------------------------
   DIVIDER
------------------------------------------------------- */

hr {
    border: none;
    border-top: 1px solid #e1e8f0;
    margin: 25px 0;
}


/* -------------------------------------------------------
   BUTTON
------------------------------------------------------- */

.stButton > button {
    border-radius: 9px;
    border: 1px solid #d9e2ec;
    background: white;
    color: #102a43;
    font-weight: 600;
}

.stButton > button:hover {
    border-color: #2563eb;
    color: #2563eb;
}


/* -------------------------------------------------------
   MULTISELECT
------------------------------------------------------- */

div[data-baseweb="select"] > div {
    border-radius: 9px;
    border-color: #d9e2ec;
    background-color: #ffffff;
}


/* -------------------------------------------------------
   SIDEBAR
------------------------------------------------------- */

section[data-testid="stSidebar"] {
    background-color: #eef2f7;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

header_col1, header_col2 = st.columns([8, 1])

with header_col1:

    st.markdown(
        '<div class="dashboard-title">📊 Campaign Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Subscription & Campaign Performance'
        '</div>',
        unsafe_allow_html=True
    )


with header_col2:

    if st.button("🔄 Refresh", use_container_width=True):
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

    if column in df.columns:

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
# SECTION - FILTERS
# =========================================================

st.markdown(
    '<div class="section-title">🎛️ Filters</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Use the filters below to explore campaign and subscription performance'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# FILTER HELPER
# =========================================================

def get_context_df(exclude=None):

    temp_df = df.copy()

    # -----------------------------------------------------
    # APP
    # -----------------------------------------------------

    if exclude != "App":

        selected = st.session_state.get(
            "app_filter", []
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
            "date_filter", []
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
            "month_filter", []
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
# FILTER ROW 1
# =========================================================

col1, col2, col3, col4, col5 = st.columns(5)


# ---------------------------------------------------------
# APP
# ---------------------------------------------------------

with col1:

    app_options = sorted([
        x for x in get_context_df("App")["App"].dropna().unique()
        if x != ""
    ])

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

    month_options = sorted([
        x for x in get_context_df("Month")["Month"].dropna().unique()
        if x != ""
    ])

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

    partner_type_options = sorted([
        x
        for x in get_context_df("Partner Type")["Partner Type"]
        .dropna()
        .unique()
        if x != ""
    ])

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

    partner_options = sorted([
        x
        for x in get_context_df("Partner")["Partner"]
        .dropna()
        .unique()
        if x != ""
    ])

    st.multiselect(
        "Partner",
        options=partner_options,
        key="partner_filter",
        placeholder="All"
    )


# =========================================================
# FILTER ROW 2
# =========================================================

col6, col7, col8, col9, col10 = st.columns(5)


# ---------------------------------------------------------
# AGENCY
# ---------------------------------------------------------

with col6:

    agency_options = sorted([
        x
        for x in get_context_df("Agency")["Agency"]
        .dropna()
        .unique()
        if x != ""
    ])

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

    campaign_options = sorted([
        x
        for x in get_context_df("Campaign")["Campaign"]
        .dropna()
        .unique()
        if x != ""
    ])

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

    currency_options = sorted([
        x
        for x in get_context_df("Currency")["currency"]
        .dropna()
        .unique()
        if x != ""
    ])

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

    gwprovider_options = sorted([
        x
        for x in get_context_df("Gwprovider")["gwprovider"]
        .dropna()
        .unique()
        if x != ""
    ])

    st.multiselect(
        "Gwprovider",
        options=gwprovider_options,
        key="gwprovider_filter",
        placeholder="All"
    )


# =========================================================
# FILTER ROW 3
# =========================================================

col11, col12, col13 = st.columns([1, 1, 1])


# ---------------------------------------------------------
# DEVICE TYPE
# ---------------------------------------------------------

with col11:

    device_options = sorted([
        x
        for x in get_context_df("devicetype")["devicetype"]
        .dropna()
        .unique()
        if x != ""
    ])

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

    week_options = sorted([
        x
        for x in get_context_df("Week")["Week"]
        .dropna()
        .unique()
        if x != ""
    ])

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

    status_options = sorted([
        x
        for x in get_context_df("Status")["transactionpurpose"]
        .dropna()
        .unique()
        if x != ""
    ])

    st.multiselect(
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
# PERFORMANCE OVERVIEW
# =========================================================

st.markdown(
    '<div class="section-title">📈 Performance Overview</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Key subscription and revenue metrics based on the selected filters'
    '</div>',
    unsafe_allow_html=True
)


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
# =========================================================

inr_data = filtered_df[
    filtered_df["currency"] == "INR"
]


total_revenue = inr_data["Plan"].sum()


# =========================================================
# KPI DISPLAY
# =========================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.metric(
        "💰 Total Revenue (INR)",
        f"₹{total_revenue:,.0f}"
    )


with kpi2:

    st.metric(
        "👥 Total Subscriptions",
        f"{total_subscriptions:,}"
    )


with kpi3:

    st.metric(
        "🆕 New Subscriptions",
        f"{new_subscriptions:,}"
    )


with kpi4:

    st.metric(
        "🔁 Renew Subscriptions",
        f"{renew_subscriptions:,}"
    )


# =========================================================
# FILTERED RECORDS
# =========================================================

st.markdown(
    f'<div class="data-badge">📄 {len(filtered_df):,} records matching current filters</div>',
    unsafe_allow_html=True
)


# =========================================================
# CHART FUNCTION
# =========================================================

def create_pie_chart(
    data,
    title,
    category,
    value_name="Subscriptions"
):

    if data.empty:
        return None

    fig = px.pie(
        data,
        names=category,
        values=value_name,
        title=title
    )

    fig.update_traces(

        texttemplate="%{percent:.1%}",

        textposition="inside",

        hovertemplate=(
            "<b>%{label}</b><br>"
            "Subscriptions: %{value:,}<br>"
            "Contribution: %{percent:.1%}"
            "<extra></extra>"
        ),

        hole=0.42
    )

    fig.update_layout(

        height=390,

        margin=dict(
            l=10,
            r=10,
            t=65,
            b=10
        ),

        title=dict(
            font=dict(
                size=17,
                color="#102a43"
            )
        ),

        legend=dict(
            orientation="v",
            font=dict(size=12)
        ),

        paper_bgcolor="white",

        plot_bgcolor="white"
    )

    return fig


# =========================================================
# PARTNER PERFORMANCE
# =========================================================

st.markdown(
    '<div class="section-title">🤝 Partner Performance</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'New and renewed subscription contribution by partner'
    '</div>',
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


fig_new_partner = create_pie_chart(
    new_partner,
    "New Subscription Contribution by Partner",
    "Partner"
)


# =========================================================
# RENEW SUBSCRIPTIONS BY PARTNER
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


fig_renew_partner = create_pie_chart(
    renew_partner,
    "Renewed Subscription Contribution by Partner",
    "Partner"
)


# =========================================================
# DISPLAY PARTNER CHARTS
# =========================================================

chart_col1, chart_col2 = st.columns(2)


with chart_col1:

    if fig_new_partner is not None:

        st.plotly_chart(
            fig_new_partner,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    else:

        st.info(
            "No new subscriptions for the selected filters."
        )


with chart_col2:

    if fig_renew_partner is not None:

        st.plotly_chart(
            fig_renew_partner,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    else:

        st.info(
            "No renewed subscriptions for the selected filters."
        )


# =========================================================
# PARTNER TYPE PERFORMANCE
# =========================================================

st.markdown(
    '<div class="section-title">🏷️ Partner Type Performance</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'New and renewed subscription contribution by partner type'
    '</div>',
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
    .sort_values(
        "Subscriptions",
        ascending=False
    )
)


chart_pt_new = create_pie_chart(
    pt_new,
    "New Subscription Contribution by Partner Type",
    "Partner Type"
)


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
    .sort_values(
        "Subscriptions",
        ascending=False
    )
)


chart_pt_renew = create_pie_chart(
    pt_renew,
    "Renewed Subscription Contribution by Partner Type",
    "Partner Type"
)


# =========================================================
# DISPLAY PARTNER TYPE
# =========================================================

pt_col1, pt_col2 = st.columns(2)


with pt_col1:

    if chart_pt_new is not None:

        st.plotly_chart(
            chart_pt_new,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    else:

        st.info("No new subscriptions.")


with pt_col2:

    if chart_pt_renew is not None:

        st.plotly_chart(
            chart_pt_renew,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    else:

        st.info("No renewed subscriptions.")


# =========================================================
# AGENCY PERFORMANCE
# =========================================================

st.markdown(
    '<div class="section-title">🏢 Agency Performance</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'New and renewed subscription contribution by agency'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# NEW - AGENCY
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
    .sort_values(
        "Subscriptions",
        ascending=False
    )
)


fig_agency_new = create_pie_chart(
    agency_new,
    "New Subscription Contribution by Agency",
    "Agency"
)


# =========================================================
# RENEW - AGENCY
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
    .sort_values(
        "Subscriptions",
        ascending=False
    )
)


fig_agency_renew = create_pie_chart(
    agency_renew,
    "Renewed Subscription Contribution by Agency",
    "Agency"
)


# =========================================================
# DISPLAY AGENCY CHARTS
# =========================================================

agency_col1, agency_col2 = st.columns(2)


with agency_col1:

    if fig_agency_new is not None:

        st.plotly_chart(
            fig_agency_new,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    else:

        st.info("No new subscriptions.")


with agency_col2:

    if fig_agency_renew is not None:

        st.plotly_chart(
            fig_agency_renew,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    else:

        st.info("No renewed subscriptions.")


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "Subscription Analytics • Campaign Performance Dashboard"
)
