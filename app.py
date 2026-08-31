import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd


import streamlit as st

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# HOME PAGE
# =========================================================

def home():

    st.title("📊 Analytics Dashboard")

    st.markdown(
        "### Welcome to the Analytics Dashboard"
    )

    st.write(
        "Select a dashboard from the sidebar to view "
        "campaign and payment analytics."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📊 Campaign Dashboard")

        st.write(
            "Analyze subscriptions by campaign, partner, "
            "agency, partner type and other dimensions."
        )

        st.page_link(
            "pages/Campaign_Dashboard.py",
            label="Open Campaign Dashboard",
            icon="📊"
        )

    with col2:

        st.subheader("💳 Payment Dashboard")

        st.write(
            "View payment transactions, payment status, "
            "gateway information and transaction details."
        )

        st.page_link(
            "pages/Payment_Dashboard.py",
            label="Open Payment Dashboard",
            icon="💳"
        )

    st.divider()

    st.caption(
        "Analytics Dashboard • Campaign & Payment Insights"
    )


# =========================================================
# NAVIGATION
# =========================================================

pg = st.navigation(
    [
        st.Page(
            home,
            title="Analytics Dashboard",
            icon="🏠",
            default=True
        ),
        st.Page(
            "pages/Campaign_Dashboard.py",
            title="Campaign Dashboard",
            icon="📊"
        ),
        st.Page(
            "pages/Payment_Dashboard.py",
            title="Payment Dashboard",
            icon="💳"
        )
    ]
)

pg.run()
