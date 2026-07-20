import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_data(file_path):
    """Load and lightly optimize the Spotify dataset for dashboard use."""
    required_columns = [
        "track_id",
        "artists",
        "album_name",
        "track_name",
        "track_genre",
        "popularity",
        "duration_ms",
        "explicit",
        "danceability",
        "energy",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
    ]

    try:
        data = pd.read_csv(file_path, usecols=required_columns, low_memory=False)
    except Exception as exc:
        raise RuntimeError(f"Error loading data: {exc}") from exc

    data = data.drop_duplicates().dropna()
    data["duration_min"] = data["duration_ms"] / 60000

    data["track_genre"] = data["track_genre"].astype("category")
    data["artists"] = data["artists"].astype("category")
    data["explicit"] = data["explicit"].astype(bool).map({True: "Explicit", False: "Clean"})
    data["explicit"] = data["explicit"].astype("category")

    for column in ["popularity", "danceability", "energy", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    data = data.dropna(subset=["popularity", "danceability", "energy"])
    return data
