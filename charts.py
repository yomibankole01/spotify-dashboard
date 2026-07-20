import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def scatter_popularity(df):

    fig = px.scatter(
        df,
        x="danceability",
        y="popularity",
        color="track_genre",
        size="energy",
        hover_data=[
            "track_name",
            "artists",
            "album_name"
        ],
        title="Danceability vs Popularity"
    )

    fig.update_layout(height=500)

    return fig

def top_artists(df):

    top = (
        df.groupby("artists")["popularity"]
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
        title="Top Artists by Average Popularity"
    )

    fig.update_layout(height=500)

    return fig

def popularity_distribution(df):

    fig = px.histogram(
        df,
        x="popularity",
        nbins=30,
        color="explicit",
        title="Popularity Distribution"
    )

    fig.update_layout(height=500)

    return fig

def radar_features(df):

    features = [
        "danceability",
        "energy",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence"
    ]

    averages = df[features].mean()

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=averages.values,
            theta=features,
            fill="toself",
            name="Average"
        )
    )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        title="Average Audio Features",
        height=500
    )

    return fig

def correlation_heatmap(df):

    cols = [
        "popularity",
        "danceability",
        "energy",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo"
    ]

    corr = df[cols].corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title="Feature Correlation"
    )

    fig.update_layout(height=600)

    return fig