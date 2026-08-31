import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd


# =========================================================
# PAYMENT DASHBOARD
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
# READ PAYMENT REPORT
# =========================================================

payment_df = conn.read(
    spreadsheet="https://docs.google.com/spreadsheets/d/1jin_QZwN7G1nwXebnWvs6rcged5xnggxefghpjehlfc/edit",
    worksheet="payment report",
    ttl=600
)


# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

payment_df.columns = payment_df.columns.str.strip()


# =========================================================
# TITLE / SUCCESS
# =========================================================

st.success("Payment data loaded successfully!")


# =========================================================
# BASIC INFORMATION
# =========================================================

st.write(f"**Total Rows:** {len(payment_df):,}")
st.write(f"**Total Columns:** {len(payment_df.columns):,}")


# =========================================================
# SHOW DATA
# =========================================================

st.dataframe(
    payment_df,
    use_container_width=True,
    hide_index=True
)
