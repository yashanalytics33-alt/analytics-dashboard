import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Payment Report",
    page_icon="💳",
    layout="wide"
)


# =========================================================
# HEADER
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
# LOAD DATA
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
# BASIC CLEANING
# =========================================================

text_columns = [
    "App",
    "Month",
    "Partner Type",
    "Partner",
    "Agency",
    "Campaign",
    "gwprovider",
    "devicetype",
    "Week",
    "currency",
    "transactionpurpose"
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

if "currency" in df.columns:
    df["currency"] = (
        df["currency"]
        .str.upper()
    )


if "transactionpurpose" in df.columns:
    df["transactionpurpose"] = (
        df["transactionpurpose"]
        .str.upper()
    )


# =========================================================
# PLAN
# =========================================================

if "Plan" in df.columns:

    df["Plan"] = pd.to_numeric(
        df["Plan"],
        errors="coerce"
    ).fillna(0)


# =========================================================
# CREATED DATE
# =========================================================

if "created" in df.columns:

    df["created"] = pd.to_datetime(
        df["created"],
        errors="coerce"
    )


# =========================================================
# FILTER SECTION
# =========================================================

st.subheader("Filters")
