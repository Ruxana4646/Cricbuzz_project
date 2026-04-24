import streamlit as st
import pandas as pd
from db_connection import get_connection

# ---------------- UI CONFIG ----------------
st.set_page_config(page_title="Player Stats", layout="wide")

# Cricbuzz-style theme
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: white;
}

.metric-card {
    background: linear-gradient(135deg, #1f4037, #99f2c8);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: black;
    font-weight: bold;
}

h1, h2, h3 {
    color: #00FFAA;
}

</style>
""", unsafe_allow_html=True)

st.title(" Player Performance Dashboard")

# ---------------- DB ----------------
conn = get_connection()

# ---------------- KPI CARDS ----------------
st.subheader(" Key Performance Indicators")

col1, col2, col3 = st.columns(3)

total_players = pd.read_sql("SELECT COUNT(DISTINCT name) AS cnt FROM players", conn)["cnt"][0]
total_runs = pd.read_sql("SELECT SUM(runs) AS runs FROM players", conn)["runs"][0]
total_matches = pd.read_sql("SELECT COUNT(DISTINCT match_id) AS cnt FROM players", conn)["cnt"][0]

col1.markdown(f"<div class='metric-card'>👥 Players<br>{total_players}</div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-card'>🏏 Total Runs<br>{total_runs}</div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric-card'>📅 Matches<br>{total_matches}</div>", unsafe_allow_html=True)

# ---------------- TOP SCORERS ----------------
st.divider()
st.subheader(" Top Run Scorers")

query1 = """
SELECT name, SUM(runs) AS total_runs
FROM players
GROUP BY name
ORDER BY total_runs DESC
LIMIT 10
"""

df1 = pd.read_sql(query1, conn)

col4, col5 = st.columns([2, 3])

with col4:
    st.dataframe(df1, use_container_width=True)

with col5:
    st.bar_chart(df1.set_index("name"))

# ---------------- STRIKE RATE ----------------
st.divider()
st.subheader(" Strike Rate Leaders")

query2 = """
SELECT name, AVG(strike_rate) AS avg_sr
FROM players
GROUP BY name
ORDER BY avg_sr DESC
LIMIT 10
"""

df2 = pd.read_sql(query2, conn)

col6, col7 = st.columns([2, 3])

with col6:
    st.dataframe(df2)

with col7:
    st.line_chart(df2.set_index("name"))

# ---------------- BOUNDARIES ----------------
st.divider()
st.subheader(" Boundary Kings")

query3 = """
SELECT name, SUM(fours + sixes) AS boundaries
FROM players
GROUP BY name
ORDER BY boundaries DESC
LIMIT 10
"""

df3 = pd.read_sql(query3, conn)

col8, col9 = st.columns([2, 3])

with col8:
    st.dataframe(df3)

with col9:
    st.bar_chart(df3.set_index("name"))

# ---------------- MATCH PERFORMANCE ----------------
st.divider()
st.subheader("📈 Match-wise Runs")

query4 = """
SELECT match_id, SUM(runs) AS total_runs
FROM players
GROUP BY match_id
ORDER BY total_runs DESC
LIMIT 10
"""

df4 = pd.read_sql(query4, conn)

st.bar_chart(df4.set_index("match_id"))

# ---------------- FOOTER ----------------
st.divider()
st.markdown("###  Cricbuzz Analytics Dashboard")
st.write("Live cricket insights powered  data pipeline")

conn.close()