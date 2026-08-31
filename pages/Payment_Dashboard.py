import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Payment Dashboard",
    page_icon="💳",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("💳 Payment Dashboard")


# =========================================================
# GOOGLE SHEETS CONNECTION
# =========================================================

conn = st.connection(
    "payment_gsheets",
    type=GSheetsConnection
)


# =========================================================
# READ PAYMENT DATA
# =========================================================

payment_df = conn.read(
    spreadsheet="Renew and Subscribed Report",
    worksheet="payment report",
    ttl=600
)


# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

payment_df.columns = (
    payment_df.columns
    .str.strip()
    .str.replace(" ", "_")
)


# =========================================================
# SUCCESS
# =========================================================

st.success("Payment data loaded successfully ✅")


# =========================================================
# BASIC INFORMATION
# =========================================================

st.write(f"**Total rows:** {len(payment_df):,}")


# =========================================================
# SHOW DATA
# =========================================================

st.dataframe(
    payment_df,
    use_container_width=True
)
