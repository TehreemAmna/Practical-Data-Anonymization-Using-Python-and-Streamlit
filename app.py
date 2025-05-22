import streamlit as st
import pandas as pd
import hashlib
from faker import Faker
# Initialize Faker
faker = Faker()
# Function to anonymize data
def anonymize_data(df):
    df_anonymized = df.copy()
    for col in df.columns:
        col_lower = col.strip().lower()
        # Hash customer id or phone number if found
        if 'customer id' in col_lower or 'phone number' in col_lower:
            df_anonymized[col] = df[col].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest())
        # Anonymize other string columns
        elif df[col].dtype == object:
            df_anonymized[col] = df[col].apply(lambda x: faker.text(max_nb_chars=12))
    return df_anonymized
# Streamlit UI
st.set_page_config(page_title="🔐 Data Anonymizer", layout="centered")
st.title("🔐 Data Anonymization Tool")
uploaded_file = st.file_uploader("📁 Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📋 Original Data")
    st.dataframe(df.head())
if st.button("🚀 Anonymize Data"):
        df_anonymized = anonymize_data(df)
        st.subheader("🛡 Anonymized Data")
        st.dataframe(df_anonymized.head())
        csv = df_anonymized.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇ Download Anonymized CSV",
            data=csv,
            file_name="anonymized_data.csv",
            mime="text/csv"
)
