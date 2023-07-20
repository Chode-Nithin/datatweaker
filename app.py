import numpy as np
import pandas as pd
# import pandas_profiling as pp
import streamlit as st
from sklearn.preprocessing import LabelEncoder
from ydata_profiling import ProfileReport

# Set dark theme
st.set_page_config(layout="wide", page_title="The EDA App", page_icon=":rocket:")

# Web App Title
st.markdown('''
# **The EDA App**

This is the **EDA App** created in Streamlit using the **pandas-profiling** library.

 App built in `Python` + `Streamlit`)

---
''')

# Upload CSV data
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
    st.sidebar.markdown("""
[Example CSV input file](./player_playingtime.csv)
""")

# Helper function to remove duplicate values
def remove_duplicates(dataframe):
    return dataframe.drop_duplicates()

# Helper function to identify primary key candidates
def identify_primary_key(dataframe):
    primary_key_candidates = []

    for col in dataframe.columns:
        if dataframe[col].nunique() == len(dataframe):
            primary_key_candidates.append(col)

    return primary_key_candidates

# Helper function to replace missing values based on strategy
def replace_missing_values(dataframe, strategy):
    if strategy == "Replace with 0":
        return dataframe.fillna(0)
    elif strategy == "Replace with mean":
        return dataframe.fillna(dataframe.mean())
    elif strategy == "Replace with median":
        return dataframe.fillna(dataframe.median())
    else:
        return dataframe

# Helper function to convert categorical data to numerical
def convert_categorical_to_numerical(df):
    label_encoder = LabelEncoder()

    for col in df.select_dtypes(include=['object']):
        df[col] = label_encoder.fit_transform(df[col])

    return df

# Main Streamlit app
def main():
    global uploaded_file

    if uploaded_file is not None:
        
        def load_csv():
            csv = pd.read_csv(uploaded_file)
            return csv

        df = load_csv()
        st.header("Missing Values Report")
        pr = ProfileReport(df, explorative=True)
        # st.markdown(pr.to_html(), unsafe_allow_html=True)
        st.components.v1.html(pr.to_html(), height=800, scrolling=True)
        # Display options after getting the report
        st.header("Data Transformation Options")

        if st.checkbox("Remove Duplicate Values"):
            df = remove_duplicates(df)

        primary_key_candidates = identify_primary_key(df)

        if st.checkbox("Identify Primary Key"):
            if len(primary_key_candidates) > 0:
                st.info(f"Possible Primary Key(s): {', '.join(primary_key_candidates)}")
            else:
                st.warning("No Primary Key candidates found.")

        if st.checkbox("Replace Missing Values"):
            missing_value_strategy = st.selectbox(
                "Choose missing value replacement strategy:",
                ["Leave as NaN", "Replace with 0", "Replace with mean", "Replace with median"]
            )

            df = replace_missing_values(df, missing_value_strategy)

        if st.checkbox("Convert Categorical Data to Numerical"):
            df = convert_categorical_to_numerical(df)

        st.header("Processed DataFrame")
        st.dataframe(df)


    else:
        st.info('Awaiting for CSV file to be uploaded.')
        if st.button('Press to use Example Dataset'):
            # Example data
            @st.cache_data
            def load_data():
                a = pd.DataFrame(
                    np.random.rand(100, 5),
                    columns=['a', 'b', 'c', 'd', 'e']
                )
                return a

            df = load_data()

            # Show missing values report using pandas_profiling
            st.header("Missing Values Report")
            pr = pp.ProfileReport(df, explorative=True)
            st_profile_report(pr)

            # Display options after getting the report
            st.header("Data Transformation Options")

            if st.checkbox("Remove Duplicate Values"):
                df = remove_duplicates(df)

            primary_key_candidates = identify_primary_key(df)

            if st.checkbox("Identify Primary Key"):
                if len(primary_key_candidates) > 0:
                    st.info(f"Possible Primary Key(s): {', '.join(primary_key_candidates)}")
                else:
                    st.warning("No Primary Key candidates found.")

            if st.checkbox("Replace Missing Values"):
                missing_value_strategy = st.selectbox(
                    "Choose missing value replacement strategy:",
                    ["Leave as NaN", "Replace with 0", "Replace with mean", "Replace with median"]
                )

                df = replace_missing_values(df, missing_value_strategy)

            if st.checkbox("Convert Categorical Data to Numerical"):
                df = convert_categorical_to_numerical(df)

            st.header("Processed DataFrame")
            st.dataframe(df)

if __name__ == "__main__":
    main()
