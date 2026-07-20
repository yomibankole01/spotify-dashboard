import streamlit as st
from utils import load_data
import charts as ch


@st.cache_data(show_spinner=False)
def get_filter_options(data):
    return {
        "genres": sorted(data["track_genre"].astype(str).unique()),
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
        initial_sidebar_state="expanded",
    )

    st.title("🎵 Spotify Analytics Dashboard")
    st.markdown(
        """
Explore Spotify songs using interactive visualizations.

Filter songs by genre, popularity and explicit content.
"""
    )

    st.markdown(
        """
        <style>
        .main { background-color:#121212; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.header("Filters")
    options = get_filter_options(data)

    selected_genres = st.sidebar.multiselect(
        "Genre",
        options=options["genres"],
        default=options["genres"][:10],
        placeholder="Search genres",
        key="genre_filter",
    )

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

    genre_values = data["track_genre"].astype(str)
    explicit_values = data["explicit"].astype(str)

    filtered = data[
        genre_values.isin(selected_genres)
        & data["popularity"].between(popularity[0], popularity[1])
        & explicit_values.isin(selected_explicit)
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
        delta=f"{filtered['popularity'].mean() - overall_popularity:.2f}",
    )
    col4.metric("💃 Danceability", f"{filtered['danceability'].mean():.2f}")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(ch.scatter_popularity(filtered), use_container_width=True)
    with col2:
        st.plotly_chart(ch.popularity_distribution(filtered), use_container_width=True)

    st.plotly_chart(ch.top_artists(filtered), use_container_width=True)
    st.plotly_chart(ch.genre_popularity(filtered), use_container_width=True)

    with st.expander("Preview Dataset"):
        st.dataframe(filtered, use_container_width=True, height=350)

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