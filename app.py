import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title="Subscription Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Subscription Analytics Dashboard")

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Read the payment report
df = conn.read(
    worksheet="payment report(combined)",
    ttl=600
)

st.success("Google Sheet connected successfully!")

st.write("Rows:", len(df))
st.write("Columns:", len(df.columns))

st.subheader("Columns")
st.write(list(df.columns))

st.subheader("Sample Data")
st.dataframe(
    df.head(10).astype(str),
    use_container_width=True
)
