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
    "gsheets",
    type=GSheetsConnection
)


# =========================================================
# READ PAYMENT SHEET
# =========================================================

payment_df = conn.read(
    spreadsheet="https://docs.google.com/spreadsheets/d/1jin_QZwN7G1nwXebnWvs6rcged5xnggxefghpjehlfc/edit",
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

st.write(f"**Total rows:** {len(payment_df):,}")


# =========================================================
# DATA
# =========================================================

st.dataframe(
    payment_df,
    use_container_width=True
)
