# =========================================
# IPL Analytics Streamlit Dashboard
# app.py
# =========================================

# Import Libraries
import os
import zipfile
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -----------------------------------------
# Streamlit Page Config
# -----------------------------------------

st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)

# -----------------------------------------
# Title
# -----------------------------------------

st.title("PragyanAI - IPL Analytics Dashboard")

st.markdown("Interactive Cricket Data Analytics using Python, NumPy, Pandas and Streamlit")

# -----------------------------------------
# Create folders
# -----------------------------------------

os.makedirs("../data", exist_ok=True)

# -----------------------------------------
# Extract ZIP File
# -----------------------------------------

zip_path = "archive.zip"

extract_path = "data"

# Extract ZIP only if CSV files do not exist
matches_file = os.path.join(extract_path, "matches.csv")
deliveries_file = os.path.join(extract_path, "deliveries.csv")

if not os.path.exists(matches_file):

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    st.success("ZIP File Extracted Successfully")

# -----------------------------------------
# Load Dataset
# -----------------------------------------

matches = pd.read_csv(matches_file)
deliveries = pd.read_csv(deliveries_file)

# -----------------------------------------
# Sidebar
# -----------------------------------------

st.sidebar.title("Filters")

teams = sorted(matches['team1'].dropna().unique())

selected_team = st.sidebar.selectbox(
    "Select Team",
    teams
)

# -----------------------------------------
# Main Metrics
# -----------------------------------------

total_matches = matches.shape[0]

total_teams = len(teams)

top_team = matches['winner'].value_counts().idxmax()

col1, col2, col3 = st.columns(3)

col1.metric("Total Matches", total_matches)

col2.metric("Total Teams", total_teams)

col3.metric("Most Successful Team", top_team)

# -----------------------------------------
# Team Matches
# -----------------------------------------

st.header(f" {selected_team} Match Analysis")

team_matches = matches[
    (matches['team1'] == selected_team) |
    (matches['team2'] == selected_team)
]

st.dataframe(team_matches.head(10))

# -----------------------------------------
# Team Wins
# -----------------------------------------

team_wins = matches['winner'].value_counts()

st.header(" Team Wins Analysis")

fig1 = px.bar(
    x=team_wins.index,
    y=team_wins.values,
    labels={'x': 'Team', 'y': 'Wins'},
    title="IPL Team Wins"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------------------
# Toss Decision Analysis
# -----------------------------------------

toss_decision = matches['toss_decision'].value_counts()

st.header("Toss Decision Analysis")

fig2 = px.pie(
    values=toss_decision.values,
    names=toss_decision.index,
    title="Toss Decisions"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------------
# Top Batsmen
# -----------------------------------------

top_batsmen = deliveries.groupby(
    'batter'
)['batsman_runs'].sum().sort_values(
    ascending=False
).head(10)

st.header("Top Run Scorers")

fig3 = px.bar(
    x=top_batsmen.index,
    y=top_batsmen.values,
    labels={'x': 'Player', 'y': 'Runs'},
    title="Top 10 Batsmen"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------------------
# Strike Rate Analysis
# -----------------------------------------
