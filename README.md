# Spotify Analytics Dashboard

This project contains a Streamlit dashboard for exploring a Spotify tracks dataset with interactive charts. The app loads the cleaned dataset from the repository, filters it by genre and popularity, and displays four linked Plotly visualizations that work together as a single narrative:
- a scatter plot for danceability versus popularity
- a popularity distribution chart
- a top artists chart
- a top genres chart

## Project structure

- app.py: the main Streamlit dashboard entry point
- charts.py: Plotly chart definitions
- utils.py: dataset loading and cleaning helpers
- data/spotify_data.csv: the source dataset used by the dashboard
- dashboard_notebook.ipynb: a narrative tutorial notebook demonstrating the visualizations
- requirements.txt: Python dependencies

## Requirements

This project uses Python 3.9+ and the following core packages:

- streamlit
- plotly
- pandas

## Reproducibility steps

1. Clone the repository:

```bash
git clone https://github.com/yomibankole01/spotify-dashboard
cd spotify-analysis
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the dashboard locally:

```bash
streamlit run app.py
```

The app should open in your browser at the local Streamlit URL.

## Dataset

The dashboard expects a CSV file at:

```bash
data/spotify_data.csv
```

The loader in utils.py cleans the data by:
- removing an index-like column if present
- dropping duplicates and missing values
- adding a duration-in-minutes column
- converting the explicit flag to readable labels
- ensuring numeric columns are suitable for visualization

## Notebook tutorial

A walkthrough notebook is included at:

```bash
dashboard_notebook.ipynb
```

It explains the dashboard visualizations, shows how to generate them from charts.py, describes the data cleaning process, and includes deployment guidance.

## Optional export dependencies

If you want to export charts as PNG images from the notebook, install:

```bash
pip install kaleido
```

## Troubleshooting

- If Streamlit cannot find the app, run the command from the repository root.
- If the dataset is missing, confirm that data/spotify_data.csv exists.
- If Plotly charts do not render in the notebook, make sure the notebook has Plotly installed and that you are running it from the repo root.
