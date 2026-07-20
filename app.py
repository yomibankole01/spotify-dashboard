import streamlit as st
from utils import load_data
import charts as ch

# ------------------ PAGE CONFIG ------------------ #
st.set_page_config(
    page_title="Spotify Analytics Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)


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

    st.title("🎵 Spotify Analytics Dashboard")

    st.markdown(
        """
Explore Spotify songs using interactive visualizations.

Filter songs by genre, artist, popularity and explicit content.
"""
    )

    st.markdown(
        """
        <style>
        .main {
            background-color:#121212;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ------------------ SIDEBAR ------------------ #

    st.sidebar.header("Filters")

    options = get_filter_options(data)

    if st.sidebar.button("Reset Filters"):
        st.session_state.clear()
        st.rerun()

    if "selected_artists" not in st.session_state:
        st.session_state.selected_artists = []

    selected_genres = st.sidebar.multiselect(
        "Genre",
        options=options["genres"],
        default=options["genres"][:10],
        placeholder="Search genres",
        key="genre_filter",
    )

    artist_source = (
        data
        if not selected_genres
        else data[data["track_genre"].astype(str).isin(selected_genres)]
    )

    top_artists = (
        artist_source.groupby("artists", observed=True)["popularity"]
        .mean()
        .sort_values(ascending=False)
        .head(20)
        .index.tolist()
    )

    artist_options = sorted(top_artists)

    valid_previous = [
        artist
        for artist in st.session_state.selected_artists
        if artist in artist_options
    ]

    artist_defaults = valid_previous if valid_previous else artist_options

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
        value=(
            options["popularity_min"],
            options["popularity_max"],
        ),
    )

    selected_explicit = st.sidebar.multiselect(
        "Explicit",
        options=options["explicit"],
        default=options["explicit"],
    )

    # ------------------ FILTER ------------------ #

    filtered = data[
        (data["track_genre"].astype(str).isin(selected_genres))
        & (data["artists"].astype(str).isin(selected_artists))
        & (data["popularity"].between(popularity[0], popularity[1]))
        & (data["explicit"].isin(selected_explicit))
    ].copy()

    if filtered.empty:
        st.warning("No songs match the selected filters.")
        return

    # ------------------ KPI ------------------ #

    overall_popularity = data["popularity"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🎵 Total Songs",
        f"{filtered.shape[0]:,}",
    )

    col2.metric(
        "🎤 Artists",
        filtered["artists"].nunique(),
    )

    col3.metric(
        "⭐ Avg Popularity",
        f"{filtered['popularity'].mean():.2f}",
        delta=f"{filtered['popularity'].mean()-overall_popularity:.2f}",
    )

    col4.metric(
        "💃 Danceability",
        f"{filtered['danceability'].mean():.2f}",
    )

    # ------------------ INSIGHTS ------------------ #

    top_artist = filtered["artists"].value_counts().idxmax()

    top_genre = filtered["track_genre"].mode()[0]

    st.info(
        f"""
### Dashboard Insights

• **{filtered.shape[0]:,} songs**

• **Top Genre:** {top_genre}

• **Top Artist:** {top_artist}

• **Average Popularity:** {filtered["popularity"].mean():.2f}

• **Average Energy:** {filtered["energy"].mean():.2f}
"""
    )

    # ------------------ TABS ------------------ #

    overview, artists_tab, genres_tab = st.tabs(
        [
            "Overview",
            "Artists",
            "Genres",
        ]
    )

    # =====================================================

    with overview:

        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(
                ch.scatter_popularity(filtered),
                use_container_width=True,
            )

        with col2:
            st.plotly_chart(
                ch.popularity_distribution(filtered),
                use_container_width=True,
            )

        col3, col4 = st.columns(2)

        with col3:
            st.plotly_chart(
                ch.radar_features(filtered),
                use_container_width=True,
            )

        with col4:
            st.plotly_chart(
                ch.correlation_heatmap(filtered),
                use_container_width=True,
            )

    # =====================================================

    with artists_tab:

        st.plotly_chart(
            ch.top_artists(filtered),
            use_container_width=True,
        )

        with st.expander("Summary Statistics"):

            st.dataframe(
                filtered.describe(numeric_only=True).round(2),
                use_container_width=True,
            )

    # =====================================================

    with genres_tab:

        # NEW CHART
        st.plotly_chart(
            ch.genre_popularity(filtered),
            use_container_width=True,
        )

        with st.expander("Preview Dataset"):

            st.dataframe(
                filtered,
                use_container_width=True,
                height=350,
            )

    # ------------------ DOWNLOAD ------------------ #

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Filtered Data",
        csv,
        "spotify_filtered.csv",
        "text/csv",
    )

    # ------------------ FOOTER ------------------ #

    st.markdown("---")

    st.caption(
        "Spotify Analytics Dashboard • Built with Streamlit + Plotly • Bankole Abayomi"
    )


if __name__ == "__main__":
    main()