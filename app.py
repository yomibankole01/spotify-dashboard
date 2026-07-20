import streamlit as st
from utils import load_data
import charts as ch

data = load_data("data/spotify_data.csv")

st.set_page_config(
    page_title="Spotify Analytics Dashboard",
    page_icon="🎵",
    layout="wide"
)

st.title("🎵 Spotify Analytics Dashboard")

st.markdown(
"""
Explore Spotify songs using interactive visualizations.

Use the filters on the left to explore the data.
"""
)

st.markdown(
    """
    <style>

    .main{
        background-color:#121212;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("Filters")

genres = sorted(data["track_genre"].unique())

selected_genres = st.sidebar.multiselect(
    "Genre",
    options=genres,
    default=genres
)

artists = sorted(data["artists"].unique())

selected_artists = st.sidebar.multiselect(
    "Artist",
    options=artists,
    default=artists
)

popularity = st.sidebar.slider(
    "Popularity",
    min_value=int(data["popularity"].min()),
    max_value=int(data["popularity"].max()),
    value=(int(data["popularity"].min()), int(data["popularity"].max()))
)

explicit = st.sidebar.multiselect(
    "Explicit",
    data["explicit"].unique(),
    default=data["explicit"].unique()
)

filtered = data[
    (data["track_genre"].isin(selected_genres)) &
    (data["artists"].isin(selected_artists)) &
    (data["popularity"].between(popularity[0], popularity[1])) &
    (data["explicit"].isin(explicit))
]   

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Songs", filtered.shape[0])
col2.metric("Total Artists", filtered["artists"].nunique())
col3.metric("Average Popularity", round(filtered["popularity"].mean(), 2))
col4.metric("Average Danceability", round(filtered["danceability"].mean(), 2))

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(ch.scatter_popularity(filtered), use_container_width=True)

with col2:
    st.plotly_chart(ch.top_artists(filtered), use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(ch.popularity_distribution(filtered), use_container_width=True)

with col4:
    st.plotly_chart(ch.radar_features(filtered), use_container_width=True)

show_advanced = st.checkbox("Show advanced charts", value=False)

if show_advanced:
    st.plotly_chart(ch.correlation_heatmap(filtered), use_container_width=True)

overview, artists, genres = st.tabs(
    [
        "Overview",
        "Artists",
        "Genres"
    ]
)
