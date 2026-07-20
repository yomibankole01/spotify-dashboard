import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_data(file_path):
    """
    Load data from a CSV file.

    Parameters:
    - file_path (str): The path to the CSV file.

    Returns:
    - pd.DataFrame: The loaded data as a pandas DataFrame.
    """
    try:
        data = pd.read_csv(file_path)

    except Exception as e:
        print(f"Error loading data: {e}")

    if "Unnamed: 0" in data.columns:
        data = data.drop(columns="Unnamed: 0")

    data = data.drop_duplicates() 
    data = data.dropna()
    data["duration_min"] = data["duration_ms"] / 60000

    data["explicit"] = data["explicit"].map(
        {
            True: "Explicit",
            False: "Clean"
        }
    )

    return data
    