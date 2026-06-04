# =========================================
# IPL Analytics Streamlit Dashboard
# app.py
# =========================================

import os
import zipfile
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -----------------------------------------
# Streamlit Config
# -----------------------------------------

st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)

# -----------------------------------------
# Title
# -----------------------------------------

st.title("🏏 PragyanAI - IPL Analytics Dashboard")
st.markdown("Interactive Cricket Data Analytics using Python, NumPy, Pandas and Streamlit")

# -----------------------------------------
# Create Data Folder
# -----------------------------------------

os.makedirs("data", exist_ok=True)

# -----------------------------------------
# ZIP Extraction
# -----------------------------------------

zip_path = "archive.zip"
extract_path = "data"

matches_file = os.path.join(extract_path, "matches.csv")
deliveries_file = os.path.join(extract_path, "deliveries.csv")

if not os.path.exists(matches_file):

    if not os.path.exists(zip_path):
        st.error("archive.zip not found!")
        st.stop()

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    st.success("Dataset Extracted Successfully")

# -----------------------------------------
# Load Dataset
# -----------------------------------------

try:
    matches = pd.read_csv(matches_file)
    deliveries = pd.read_csv(deliveries_file)

except Exception as e:
    st.error(f"Error Loading Dataset: {e}")
    st.stop()

# -----------------------------------------
# Show Columns (for debugging)
# -----------------------------------------

with st.expander("Dataset Columns"):
    st.write("Matches Columns:", matches.columns.tolist())
    st.write("Deliveries Columns:", deliveries.columns.tolist())

# -----------------------------------------
# Fix Batter/Batsman Column
# -----------------------------------------

if "batter" in deliveries.columns:
    batter_col = "batter"
elif "batsman" in deliveries.columns:
    batter_col = "batsman"
else:
    st.error("No batter/batsman column found.")
    st.stop()

# -----------------------------------------
# Sidebar
# -----------------------------------------

st.sidebar.title("Filters")

teams = sorted(matches["team1"].dropna().unique())

selected_team = st.sidebar.selectbox(
    "Select Team",
    teams
)

# -----------------------------------------
# Main Metrics
# -----------------------------------------

total_matches = matches.shape[0]
total_teams = len(teams)
top_team = matches["winner"].value_counts().idxmax()

c1, c2, c3 = st.columns(3)

c1.metric("Total Matches", total_matches)
c2.metric("Total Teams", total_teams)
c3.metric("Most Successful Team", top_team)

# -----------------------------------------
# Team Analysis
# -----------------------------------------

st.header(f"{selected_team} Match Analysis")

team_matches = matches[
    (matches["team1"] == selected_team)
    | (matches["team2"] == selected_team)
]

st.dataframe(team_matches.head(10))

# -----------------------------------------
# Team Wins
# -----------------------------------------

st.header("Team Wins Analysis")

team_wins = matches["winner"].value_counts()

fig1 = px.bar(
    x=team_wins.index,
    y=team_wins.values,
    labels={"x": "Team", "y": "Wins"},
    title="IPL Team Wins"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------------------
# Toss Analysis
# -----------------------------------------

st.header("Toss Decision Analysis")

toss = matches["toss_decision"].value_counts()

fig2 = px.pie(
    values=toss.values,
    names=toss.index,
    title="Toss Decisions"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------------
# Top Run Scorers
# -----------------------------------------

st.header("Top Run Scorers")

top_batsmen = (
    deliveries.groupby(batter_col)["batsman_runs"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig3 = px.bar(
    x=top_batsmen.index,
    y=top_batsmen.values,
    labels={"x": "Player", "y": "Runs"},
    title="Top 10 Run Scorers"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------------------
# Strike Rate
# -----------------------------------------

st.header("⚡ Top Strike Rate Players")

runs = deliveries.groupby(batter_col)["batsman_runs"].sum()
balls = deliveries.groupby(batter_col)["ball"].count()

strike_rate = ((runs / balls) * 100)

strike_rate = strike_rate[runs > 500]
strike_rate = strike_rate.sort_values(ascending=False).head(10)

fig4 = px.bar(
    x=strike_rate.index,
    y=strike_rate.values,
    labels={"x": "Player", "y": "Strike Rate"},
    title="Top Strike Rate Players"
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------------------
# Bowling Analysis
# -----------------------------------------

st.header("Top Wicket Takers")

wickets = deliveries[deliveries["is_wicket"] == 1]

top_bowlers = wickets["bowler"].value_counts().head(10)

fig5 = px.bar(
    x=top_bowlers.index,
    y=top_bowlers.values,
    labels={"x": "Bowler", "y": "Wickets"},
    title="Top Wicket Takers"
)

st.plotly_chart(fig5, use_container_width=True)

# -----------------------------------------
# Venue Analysis
# -----------------------------------------

st.header("Top IPL Venues")

venues = matches["venue"].value_counts().head(10)

fig6 = px.bar(
    x=venues.index,
    y=venues.values,
    labels={"x": "Venue", "y": "Matches"},
    title="Top IPL Venues"
)

st.plotly_chart(fig6, use_container_width=True)

# -----------------------------------------
# Season Analysis
# -----------------------------------------

st.header("Season Wise Matches")

season_matches = matches["season"].value_counts().sort_index()

fig7 = px.line(
    x=season_matches.index,
    y=season_matches.values,
    markers=True,
    labels={"x": "Season", "y": "Matches"},
    title="Matches Played Per Season"
)

st.plotly_chart(fig7, use_container_width=True)

# -----------------------------------------
# NumPy Statistics
# -----------------------------------------

st.header("NumPy Statistics")

match_scores = deliveries.groupby("match_id")["total_runs"].sum()

scores = np.array(match_scores)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Average Score", round(np.mean(scores), 2))
c2.metric("Maximum Score", int(np.max(scores)))
c3.metric("Minimum Score", int(np.min(scores)))
c4.metric("Std Deviation", round(np.std(scores), 2))

# -----------------------------------------
# Score Distribution
# -----------------------------------------

st.header("Match Score Distribution")

fig8 = px.histogram(
    x=scores,
    nbins=20,
    title="Distribution of Match Scores"
)

st.plotly_chart(fig8, use_container_width=True)

# -----------------------------------------
# Raw Data
# -----------------------------------------

st.header("Raw Dataset")

if st.checkbox("Show Matches Dataset"):
    st.dataframe(matches)

if st.checkbox("Show Deliveries Dataset"):
    st.dataframe(deliveries)

# -----------------------------------------
# Footer
# -----------------------------------------

st.markdown("---")
st.markdown("### IPL Analytics Dashboard")
st.markdown("Built with Python, NumPy, Pandas, Plotly and Streamlit")
