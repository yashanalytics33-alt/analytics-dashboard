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
# HEADER
# =========================================================

st.title("💳 Payment Dashboard")


# =========================================================
# GOOGLE SHEETS CONNECTION
# =========================================================

conn = st.connection(
    "gsheets",
    type=GSheetsConnection
)


# =========================================================
# PAYMENT SUBSCRIPTION SHEET
# =========================================================

payment_df = conn.read(
    worksheet="payment subscription",
    ttl=600
)


# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

payment_df.columns = payment_df.columns.str.strip()


# =========================================================
# BASIC INFORMATION
# =========================================================

st.success("Payment subscription sheet connected successfully")


st.write(
    f"**Total rows:** {len(payment_df):,}"
)


# =========================================================
# COLUMNS AVAILABLE
# =========================================================

st.subheader("Payment Subscription Data")

st.dataframe(
    payment_df,
    use_container_width=True
)
