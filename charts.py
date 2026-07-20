import plotly.express as px
import plotly.graph_objects as go


def _sample_for_plot(df, max_rows=12000):
    if len(df) > max_rows:
        return df.sample(max_rows, random_state=42)
    return df


def _apply_common_layout(fig, height=450):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=40, b=10),
        template="plotly_dark",
    )


def scatter_popularity(df):
    draw_df = _sample_for_plot(df)
    fig = px.scatter(
        draw_df,
        x="danceability",
        y="popularity",
        color="track_genre",
        size="energy",
        hover_data=["track_name", "artists", "album_name"],
        title="Danceability vs Popularity",
    )
    _apply_common_layout(fig)
    return fig


def top_artists(df):
    top = (
        df.groupby("artists", observed=True)["popularity"]
        .mean()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )
    fig = px.bar(
        top,
        x="popularity",
        y="artists",
        orientation="h",
        color="popularity",
        title="Top Artists by Average Popularity",
    )
    _apply_common_layout(fig)
    return fig


def popularity_distribution(df):
    fig = px.histogram(
        df,
        x="popularity",
        nbins=25,
        color="explicit",
        title="Popularity Distribution",
    )
    _apply_common_layout(fig)
    return fig


def genre_popularity(df):
    genre = (
        df.groupby("track_genre", observed=True)["popularity"]
        .mean()
        .nlargest(10)
        .reset_index()
    )
    fig = px.bar(
        genre,
        x="popularity",
        y="track_genre",
        orientation="h",
        color="popularity",
        title="Top Genres by Average Popularity",
    )
    fig.update_layout(yaxis=dict(categoryorder="total ascending"))
    _apply_common_layout(fig, 450)
    return fig