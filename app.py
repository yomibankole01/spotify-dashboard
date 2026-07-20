import streamlit as st
from utils import load_data
import charts as ch


@st.cache_data(show_spinner=False)
def get_filter_options(data):
    return {
        "genres": sorted(data["track_genre"].astype(str).unique()),
        "artists": sorted(data["artists"].astype(str).unique()),
        "popularity_min": int(data["popularity"].min()),
        "popularity_max": int(data["popularity"].max()),
        "explicit": sorted(data["explicit"].astype(str).unique()),
    }


def main():
    data = load_data("data/spotify_data.csv")

    st.set_page_config(
        page_title="Spotify Analytics Dashboard",
        page_icon="🎵",
        layout="wide",
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
        .main { background-color: #121212; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.header("Filters")
    options = get_filter_options(data)

    if "selected_artists" not in st.session_state:
        st.session_state.selected_artists = []

    selected_genres = st.sidebar.multiselect(
        "Genre",
        options=options["genres"],
        default=options["genres"][:10],
        placeholder="Search genres",
        key="genre_filter",
    )

    artist_source = data if not selected_genres else data[data["track_genre"].astype(str).isin(selected_genres)]
    artist_options = sorted(artist_source["artists"].astype(str).unique())
    valid_previous_artists = [artist for artist in st.session_state.selected_artists if artist in artist_options]
    artist_defaults = valid_previous_artists if valid_previous_artists else artist_options

    selected_artists = st.sidebar.multiselect(
        "Artist",
        options=artist_options,
        default=artist_defaults,
        placeholder="Search artists",
        key="artist_filter",
    )
    st.session_state.selected_artists = selected_artists
    popularity = st.sidebar.slider(
        "Popularity",
        min_value=options["popularity_min"],
        max_value=options["popularity_max"],
        value=(options["popularity_min"], options["popularity_max"]),
    )
    selected_explicit = st.sidebar.multiselect(
        "Explicit",
        options=options["explicit"],
        default=options["explicit"],
    )

    filtered = data[
        (data["track_genre"].astype(str).isin(selected_genres))
        & (data["artists"].astype(str).isin(selected_artists))
        & (data["popularity"].between(popularity[0], popularity[1]))
        & (data["explicit"].isin(selected_explicit))
    ].copy()

    if filtered.empty:
        st.info("No songs match the current filters.")
        return

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Songs", int(filtered.shape[0]))
    col2.metric("Total Artists", int(filtered["artists"].nunique()))
    col3.metric("Average Popularity", round(float(filtered["popularity"].mean()), 2))
    col4.metric("Average Danceability", round(float(filtered["danceability"].mean()), 2))

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

    with st.expander("Advanced charts", expanded=False):
        st.plotly_chart(ch.correlation_heatmap(filtered), use_container_width=True)

    st.download_button(
        "Download filtered data",
        filtered.to_csv(index=False),
        "spotify_filtered.csv",
        "text/csv",
    )

    st.tabs(["Overview", "Artists", "Genres"])


if __name__ == "__main__":
    main()
