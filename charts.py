import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def _sample_for_plot(df, max_rows=15000):
    if len(df) > max_rows:
        return df.sample(max_rows, random_state=42)
    return df


@st.cache_data(show_spinner=False)
def scatter_popularity(df):
    draw_df = _sample_for_plot(df, 15000)

    fig = px.scatter(
        draw_df,
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

@st.cache_data(show_spinner=False)
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

@st.cache_data(show_spinner=False)
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

@st.cache_data(show_spinner=False)
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

@st.cache_data(show_spinner=False)
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

    plot_df = _sample_for_plot(df, 12000)
    corr = plot_df[cols].corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title="Feature Correlation"
    )

    fig.update_layout(height=600)

    return fig