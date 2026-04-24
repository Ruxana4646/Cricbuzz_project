import streamlit as st
import pandas as pd
from db_connection import get_connection
from datetime import datetime
import time

# ---------------- AUTO REFRESH ----------------
st.set_page_config(page_title="Live Matches", layout="wide")

# refresh every 30 sec
st.experimental_rerun = False

# ---------------- STYLE ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0F172A, #1E293B, #020617);
    color: white;
}

.match-card {
    background: linear-gradient(135deg, #1E3A8A, #2563EB);
    padding: 20px;
    border-radius: 12px;
    color: white;
    margin-bottom: 15px;
    box-shadow: 0 4px 20px rgba(37, 99, 235, 0.3);
}

.live-dot {
    height: 10px;
    width: 10px;
    background-color: #22C55E;
    border-radius: 50%;
    display: inline-block;
    animation: blink 1s infinite;
}

@keyframes blink {
    50% { opacity: 0.3; }
}

.winner {
    color: #FACC15;
    font-weight: bold;
}

.team {
    font-size: 20px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

st.title("📺 Live Cricket Matches")

# ---------------- DB ----------------
conn = get_connection()

query = """
SELECT match_id, team1, team2, venue, city, 
       team1_runs, team2_runs, status, start_date
FROM matches
ORDER BY start_date DESC
LIMIT 20
"""

df = pd.read_sql(query, conn)

# ---------------- AUTO REFRESH ----------------
st.caption("🔄 Auto-refresh every 30 seconds")

# ---------------- MATCH CARDS ----------------
for _, row in df.iterrows():

    # 🔥 LIVE DETECTION
    is_live = "live" in str(row["status"]).lower() or "progress" in str(row["status"]).lower()

    # 🏆 WINNER LOGIC
    winner = ""
    if row["team1_runs"] > row["team2_runs"]:
        winner = f"{row['team1']} 🏆"
    elif row["team2_runs"] > row["team1_runs"]:
        winner = f"{row['team2']} 🏆"

    # ⏳ TIME CALCULATION
    match_time = ""
    try:
        start = pd.to_datetime(row["start_date"])
        now = datetime.now()
        diff = now - start
        hours = int(diff.total_seconds() // 3600)
        match_time = f"{hours}h ago"
    except:
        match_time = "N/A"

    # 🟢 LIVE DOT
    live_html = '<span class="live-dot"></span> LIVE' if is_live else ''

    st.markdown(f"""
    <div class="match-card">
        <div class="team">
            {row['team1']} vs {row['team2']} {live_html}
        </div>
        <div>📍 {row['venue']}, {row['city']}</div>
        <div>🏏 {row['team1']} : {row['team1_runs']} | {row['team2']} : {row['team2_runs']}</div>
        <div>⏳ {match_time}</div>
        <div class="winner">{winner}</div>
        <div>📡 {row['status']}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- OPTIONAL TABLE ----------------
st.divider()
st.subheader("📊 Raw Match Data")
st.dataframe(df, use_container_width=True)

conn.close()

# ---------------- AUTO REFRESH LOOP ----------------
time.sleep(30)
st.experimental_rerun()