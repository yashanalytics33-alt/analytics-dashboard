import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(
    page_title="Subscription Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Subscription Analytics Dashboard")

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Read payment report
df = conn.read(
    worksheet="payment report(combined)",
    ttl=600
)

# Clean column names
df.columns = df.columns.str.strip()

# Clean important columns
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

# Convert Plan to number
df["Plan"] = pd.to_numeric(df["Plan"], errors="coerce").fillna(0)

# -----------------------------
# SUBSCRIPTION CALCULATIONS
# -----------------------------

new_subscriptions = (
    df["transactionpurpose"] == "NEW"
).sum()

renew_subscriptions = (
    df["transactionpurpose"] == "RENEW"
).sum()

total_subscriptions = new_subscriptions + renew_subscriptions

# -----------------------------
# REVENUE CALCULATION
# -----------------------------

inr_data = df[df["currency"] == "INR"]

total_revenue = inr_data["Plan"].sum()

# -----------------------------
# KPI CARDS
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue (INR) (Gross)",
    f"₹{total_revenue:,.0f}"
)

col2.metric(
    "Total Subscriptions",
    f"{total_subscriptions:,}"
)

col3.metric(
    "New Subscriptions",
    f"{new_subscriptions:,}"
)

col4.metric(
    "Renew Subscriptions",
    f"{renew_subscriptions:,}"
)

# -----------------------------
# DATA CHECK
# -----------------------------

st.divider()

st.write("Total rows:", f"{len(df):,}")
st.write("INR rows:", f"{len(inr_data):,}")
