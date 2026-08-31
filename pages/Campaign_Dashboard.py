import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Campaign Dashboard",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# CUSTOM DESIGN
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Remove excessive top spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* Main title */
    .dashboard-title {
        font-size: 32px;
        font-weight: 700;
        color: #172033;
        margin-bottom: 2px;
    }

    .dashboard-subtitle {
        font-size: 15px;
        color: #6b7280;
        margin-bottom: 20px;
    }

    /* Section title */
    .section-title {
        font-size: 20px;
        font-weight: 650;
        color: #172033;
        margin-top: 20px;
        margin-bottom: 12px;
    }

    /* Filter container */
    .filter-box {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 18px 20px 8px 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    /* KPI cards */
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        min-height: 115px;
    }

    div[data-testid="stMetricLabel"] {
        color: #6b7280;
        font-size: 14px;
        font-weight: 500;
    }

    div[data-testid="stMetricValue"] {
        color: #172033;
        font-size: 27px;
        font-weight: 700;
    }

    /* Chart cards */
    .chart-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 8px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    /* Buttons */
    .stButton > button {
        border-radius: 9px;
        border: 1px solid #d1d5db;
        font-weight: 600;
        padding: 7px 16px;
    }

    /* Multiselect */
    div[data-baseweb="select"] > div {
        border-radius: 9px;
    }

    /* Hide Streamlit footer */
    footer {
        visibility: hidden;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

header_col1, header_col2 = st.columns([7, 1])

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
    '<div class="section-title">🎛️ Filters</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="filter-box">',
    unsafe_allow_html=True
)


# =========================================================
# HELPER FUNCTION
# =========================================================

def get_context_df(exclude=None):

    temp_df = df.copy()

    # APP
    if exclude != "App":

        selected = st.session_state.get(
            "app_filter", []
        )

        if selected:

            temp_df = temp_df[
                temp_df["App"].isin(selected)
            ]


    # DATE
    if exclude != "Date":

        selected = st.session_state.get(
            "date_filter", []
        )

        if selected:

            temp_df = temp_df[
                temp_df["created"].dt.date.isin(selected)
            ]


    # MONTH
    if exclude != "Month":

        selected = st.session_state.get(
            "month_filter", []
        )

        if selected:

            temp_df = temp_df[
                temp_df["Month"].isin(selected)
            ]


    # PARTNER TYPE
    if exclude != "Partner Type":

        selected = st.session_state.get(
            "partner_type_filter", []
        )

        if selected:

            temp_df = temp_df[
                temp_df["Partner Type"].isin(selected)
            ]


    # PARTNER
    if exclude != "Partner":

        selected = st.session_state.get(
            "partner_filter", []
        )

        if selected:

            temp_df = temp_df[
                temp_df["Partner"].isin(selected)
            ]


    # AGENCY
    if exclude != "Agency":

        selected = st.session_state.get(
            "agency_filter", []
        )

        if selected:

            temp_df = temp_df[
                temp_df["Agency"].isin(selected)
            ]


    # CAMPAIGN
    if exclude != "Campaign":

        selected = st.session_state.get(
            "campaign_filter", []
        )

        if selected:

            temp_df = temp_df[
                temp_df["Campaign"].isin(selected)
            ]


    # PLAN
    if exclude != "Plan":

        selected = st.session_state.get(
            "plan_filter", []
        )

        if selected:

            temp_df = temp_df[
                temp_df["Plan"].isin(selected)
            ]


    # CURRENCY
    if exclude != "Currency":

        selected = st.session_state.get(
            "currency_filter", []
        )

        if selected:

            temp_df = temp_df[
                temp_df["currency"].isin(selected)
            ]


    # GWPROVIDER
    if exclude != "Gwprovider":

        selected = st.session_state.get(
            "gwprovider_filter", []
        )

        if selected:

            temp_df = temp_df[
                temp_df["gwprovider"].isin(selected)
            ]


    # DEVICE TYPE
    if exclude != "devicetype":

        selected = st.session_state.get(
            "device_filter", []
        )

        if selected:

            temp_df = temp_df[
                temp_df["devicetype"].isin(selected)
            ]


    # WEEK
    if exclude != "Week":

        selected = st.session_state.get(
            "week_filter", []
        )

        if selected:

            temp_df = temp_df[
                temp_df["Week"].isin(selected)
            ]


    # STATUS
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


# APP
with col1:

    app_options = sorted(
        [
            x for x in get_context_df("App")["App"]
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


# DATE
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


# MONTH
with col3:

    month_options = sorted(
        [
            x for x in get_context_df("Month")["Month"]
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


# PARTNER TYPE
with col4:

    partner_type_options = sorted(
        [
            x for x in get_context_df("Partner Type")["Partner Type"]
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


# PARTNER
with col5:

    partner_options = sorted(
        [
            x for x in get_context_df("Partner")["Partner"]
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
# FILTER ROW 2
# =========================================================

col6, col7, col8, col9, col10 = st.columns(5)


# AGENCY
with col6:

    agency_options = sorted(
        [
            x for x in get_context_df("Agency")["Agency"]
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


# CAMPAIGN
with col7:

    campaign_options = sorted(
        [
            x for x in get_context_df("Campaign")["Campaign"]
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


# PLAN
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


# CURRENCY
with col9:

    currency_options = sorted(
        [
            x for x in get_context_df("Currency")["currency"]
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


# GWPROVIDER
with col10:

    gwprovider_options = sorted(
        [
            x for x in get_context_df("Gwprovider")["gwprovider"]
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
# FILTER ROW 3
# =========================================================

col11, col12, col13 = st.columns(3)


# DEVICE
with col11:

    device_options = sorted(
        [
            x for x in get_context_df("devicetype")["devicetype"]
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


# WEEK
with col12:

    week_options = sorted(
        [
            x for x in get_context_df("Week")["Week"]
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


# STATUS
with col13:

    status_options = sorted(
        [
            x for x in get_context_df("Status")["transactionpurpose"]
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


st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# FINAL FILTERED DATA
# =========================================================

filtered_df = get_context_df()


# =========================================================
# PERFORMANCE OVERVIEW
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
# =========================================================

inr_data = filtered_df[
    filtered_df["currency"] == "INR"
]

total_revenue = inr_data["Plan"].sum()


# =========================================================
# SECTION TITLE
# =========================================================

st.markdown(
    '<div class="section-title">📈 Performance Overview</div>',
    unsafe_allow_html=True
)


# =========================================================
# KPI CARDS
# =========================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.metric(
        "Total Revenue (INR)",
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

st.markdown(
    f"""
    <div style="
        text-align:right;
        color:#6b7280;
        font-size:13px;
        margin-top:10px;
        margin-bottom:15px;
    ">
        Filtered rows: <b>{len(filtered_df):,}</b>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# PARTNER PERFORMANCE
# =========================================================

st.markdown(
    '<div class="section-title">👥 Partner Performance</div>',
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
    .sort_values("Subscriptions", ascending=False)
)


if not new_partner.empty:

    fig_new_partner = px.pie(
        new_partner,
        names="Partner",
        values="Subscriptions"
    )

    fig_new_partner.update_traces(
        texttemplate="%{percent:.1%}",
        textposition="inside",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Subscriptions: %{value:,}<br>"
            "Contribution: %{percent:.1%}"
            "<extra></extra>"
        ),
        sort=False
    )

    fig_new_partner.update_layout(
        title={
            "text": "New Subscriptions",
            "x": 0.02,
            "xanchor": "left"
        },
        height=430,
        margin=dict(l=10, r=10, t=55, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend_title_text="Partner"
    )

else:

    fig_new_partner = None


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
    .sort_values("Subscriptions", ascending=False)
)


if not renew_partner.empty:

    fig_renew_partner = px.pie(
        renew_partner,
        names="Partner",
        values="Subscriptions"
    )

    fig_renew_partner.update_traces(
        texttemplate="%{percent:.1%}",
        textposition="inside",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Subscriptions: %{value:,}<br>"
            "Contribution: %{percent:.1%}"
            "<extra></extra>"
        ),
        sort=False
    )

    fig_renew_partner.update_layout(
        title={
            "text": "Renewed Subscriptions",
            "x": 0.02,
            "xanchor": "left"
        },
        height=430,
        margin=dict(l=10, r=10, t=55, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend_title_text="Partner"
    )

else:

    fig_renew_partner = None


# =========================================================
# DISPLAY PARTNER CHARTS
# =========================================================

chart_col1, chart_col2 = st.columns(2)


with chart_col1:

    if fig_new_partner is not None:

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)

        st.plotly_chart(
            fig_new_partner,
            use_container_width=True,
            config={"displayModeBar": False}
        )

        st.markdown("</div>", unsafe_allow_html=True)

    else:

        st.info("No new subscriptions for selected filters.")


with chart_col2:

    if fig_renew_partner is not None:

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)

        st.plotly_chart(
            fig_renew_partner,
            use_container_width=True,
            config={"displayModeBar": False}
        )

        st.markdown("</div>", unsafe_allow_html=True)

    else:

        st.info("No renewed subscriptions for selected filters.")


# =========================================================
# PARTNER TYPE PERFORMANCE
# =========================================================

st.markdown(
    '<div class="section-title">🏢 Partner Type Performance</div>',
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


if len(pt_new) > 0:

    chart_pt_new = px.pie(
        pt_new,
        names="Partner Type",
        values="Subscriptions"
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
            "x": 0.02,
            "xanchor": "left"
        },
        height=430,
        margin=dict(l=10, r=10, t=55, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend_title_text="Partner Type"
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


if len(pt_renew) > 0:

    chart_pt_renew = px.pie(
        pt_renew,
        names="Partner Type",
        values="Subscriptions"
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
            "x": 0.02,
            "xanchor": "left"
        },
        height=430,
        margin=dict(l=10, r=10, t=55, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend_title_text="Partner Type"
    )

else:

    chart_pt_renew = None


# =========================================================
# DISPLAY PARTNER TYPE
# =========================================================

pt_col1, pt_col2 = st.columns(2)


with pt_col1:

    if chart_pt_new is not None:

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)

        st.plotly_chart(
            chart_pt_new,
            use_container_width=True,
            config={"displayModeBar": False}
        )

        st.markdown("</div>", unsafe_allow_html=True)

    else:

        st.info("No new subscriptions.")


with pt_col2:

    if chart_pt_renew is not None:

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)

        st.plotly_chart(
            chart_pt_renew,
            use_container_width=True,
            config={"displayModeBar": False}
        )

        st.markdown("</div>", unsafe_allow_html=True)

    else:

        st.info("No renewed subscriptions.")


# =========================================================
# AGENCY PERFORMANCE
# =========================================================

st.markdown(
    '<div class="section-title">🏷️ Agency Performance</div>',
    unsafe_allow_html=True
)


# =========================================================
# NEW BY AGENCY
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


if len(agency_new) > 0:

    fig_agency_new = px.pie(
        agency_new,
        names="Agency",
        values="Subscriptions"
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
            "x": 0.02,
            "xanchor": "left"
        },
        height=430,
        margin=dict(l=10, r=10, t=55, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend_title_text="Agency"
    )

else:

    fig_agency_new = None


# =========================================================
# RENEW BY AGENCY
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


if len(agency_renew) > 0:

    fig_agency_renew = px.pie(
        agency_renew,
        names="Agency",
        values="Subscriptions"
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
            "x": 0.02,
            "xanchor": "left"
        },
        height=430,
        margin=dict(l=10, r=10, t=55, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend_title_text="Agency"
    )

else:

    fig_agency_renew = None


# =========================================================
# DISPLAY AGENCY
# =========================================================

agency_col1, agency_col2 = st.columns(2)


with agency_col1:

    if fig_agency_new is not None:

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)

        st.plotly_chart(
            fig_agency_new,
            use_container_width=True,
            config={"displayModeBar": False}
        )

        st.markdown("</div>", unsafe_allow_html=True)

    else:

        st.info("No new subscriptions.")


with agency_col2:

    if fig_agency_renew is not None:

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)

        st.plotly_chart(
            fig_agency_renew,
            use_container_width=True,
            config={"displayModeBar": False}
        )

        st.markdown("</div>", unsafe_allow_html=True)

    else:

        st.info("No renewed subscriptions.")
