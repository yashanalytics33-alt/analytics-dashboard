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
    "payment_gsheets",
    type=GSheetsConnection,
    spreadsheet="https://docs.google.com/spreadsheets/d/1jin_QZwN7G1nwXebnWvs6rcged5xnggxefghpjehlfc/edit"
)


# =========================================================
# READ PAYMENT REPORT
# =========================================================

payment_df = conn.read(
    worksheet="payment report",
    ttl=600
)


# =========================================================
# BASIC CLEANING
# =========================================================

payment_df.columns = payment_df.columns.str.strip()


# =========================================================
# SHOW DATA
# =========================================================

st.success("Payment data loaded successfully!")

st.write("Rows:", len(payment_df))
st.write("Columns:", len(payment_df.columns))

st.dataframe(
    payment_df,
    use_container_width=True,
    hide_index=True
)
