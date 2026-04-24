import streamlit as st
import requests

from extract import extract_matches, extract_players
from insert import insert_matches, insert_players

# ---------------- UI CONFIG ----------------
st.set_page_config(page_title="Cricbuzz Analytics", layout="wide")

st.markdown("""
<style>

/* Background */
body {
    background: linear-gradient(135deg, #0F172A, #1E293B, #020617);
    color: #E2E8F0;
}

/* Title */
.main-title {
    font-size: 40px;
    font-weight: bold;
    color: #2563EB;
}

/* Subtitle */
.sub-text {
    color: #94A3B8;
    font-size: 18px;
}

/* Cards */
.card {
    background: linear-gradient(135deg, #1E3A8A, #2563EB);
    padding: 20px;
    border-radius: 12px;
    color: white;
    text-align: center;
    font-weight: bold;
    box-shadow: 0 4px 20px rgba(37, 99, 235, 0.4);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #1E3A8A, #2563EB);
    color: white;
    border-radius: 8px;
    height: 45px;
    font-weight: bold;
    border: none;
}

/* Headings */
h1, h2, h3 {
    color: #3B82F6;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background-color: #020617;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='main-title'> Cricbuzz Analytics Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Live cricket data pipeline & insights</div>", unsafe_allow_html=True)

st.divider()

# ---------------- LIVE MATCH SECTION ----------------
st.subheader(" Live Match Overview")

st.info("Real-time match insights integrated to data analytics pipeline")

# ---------------- KPI CARDS ----------------
col1, col2, col3 = st.columns(3)

col1.markdown("<div class='card'> Data Pipeline<br>Active</div>", unsafe_allow_html=True)
col2.markdown("<div class='card'> Live Updates<br>Enabled</div>", unsafe_allow_html=True)
col3.markdown("<div class='card'> Database<br>Connected</div>", unsafe_allow_html=True)

st.divider()

# ---------------- API CALL ----------------
def get_scorecard(match_id):
    url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/hscard"

    headers = {
        "X-RapidAPI-Key": "b3d7f61023msh362a5491e103391p1f5aecjsnb0cb3e72401e",
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.json()
    except:
        return {}

# ---------------- PIPELINE ----------------
st.subheader(" Run Data Pipeline")

st.write("Extract → Transform → Load → Analyze")

if st.button("▶ Run Full Pipeline"):

    all_players = []
    skipped = 0

    with st.spinner("Processing live cricket data..."):

        matches = extract_matches()

        if not matches:
            st.error("❌ No matches found")
            st.stop()

        insert_matches(matches)

        for m in matches:
            match_id = m.get("match_id")

            if not match_id:
                skipped += 1
                continue

            try:
                scorecard = get_scorecard(match_id)

                if not scorecard:
                    skipped += 1
                    continue

                players = extract_players(scorecard, match_id)
                all_players.extend(players)

            except:
                skipped += 1
                continue

        if all_players:
            insert_players(all_players)

    # ---------------- RESULTS ----------------
    st.success("✅ Pipeline Completed Successfully!")

    col4, col5, col6 = st.columns(3)

    col4.metric("Matches Processed", len(matches))
    col5.metric("Players Inserted", len(all_players))
    col6.metric("Skipped Matches", skipped)

st.divider()

# ---------------- FOOTER ----------------
st.markdown("### Powered by Cricbuzz API + API → Extract → Transform → Load → Visualize")
st.write("Navigate using sidebar → Live Matches | Player Stats | CRUD | Queries")