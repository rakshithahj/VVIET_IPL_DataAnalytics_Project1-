import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="IPL Data Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 IPL Data Analytics Dashboard")

uploaded_file = st.file_uploader(
    "Upload IPL CSV File",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Information")
    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])

    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns

    if len(numeric_columns) > 0:
        column = st.selectbox(
            "Select a column for visualization",
            numeric_columns
        )

        fig = px.histogram(
            df,
            x=column,
            title=f"Distribution of {column}"
        )

        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Please upload a CSV file to begin analysis.")
