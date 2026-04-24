import streamlit as st
import pandas as pd
from db_connection import get_connection

# ---------------- UI CONFIG ----------------
st.set_page_config(page_title="Player Management", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: white;
    }
    .stButton>button {
        border-radius: 8px;
        height: 45px;
        width: 100%;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title(" Player Management System")

# ---------------- DB ----------------
conn = get_connection()
cur = conn.cursor()

# ---------------- CREATE ----------------
st.subheader("➕ Add New Player")

col1, col2 = st.columns(2)

with col1:
    player_id = st.text_input("Player ID")
    match_id = st.text_input("Match ID")
    name = st.text_input("Player Name")

with col2:
    runs = st.number_input("Runs", min_value=0)
    balls = st.number_input("Balls", min_value=0)
    fours = st.number_input("Fours", min_value=0)
    sixes = st.number_input("Sixes", min_value=0)
    strike_rate = st.number_input("Strike Rate", min_value=0.0)

out_desc = st.text_input("Out Description")

if st.button("➕ Add Player"):
    if not player_id.isdigit() or not match_id.isdigit():
        st.error(" Player ID and Match ID must be numbers")
    else:
        try:
            cur.execute("""
                INSERT INTO players 
                (player_id, match_id, name, runs, balls, fours, sixes, strike_rate, out_desc)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                int(player_id),
                int(match_id),
                name,
                runs,
                balls,
                fours,
                sixes,
                strike_rate,
                out_desc or "not out"
            ))

            conn.commit()
            st.success("✅ Player added successfully!")

        except Exception as e:
            st.error(f" {e}")

# ---------------- READ ----------------
st.divider()
st.subheader("📋 Player Records")

df = pd.read_sql("SELECT * FROM players ORDER BY match_id DESC LIMIT 100", conn)
st.dataframe(df, use_container_width=True)

# ---------------- UPDATE ----------------
st.divider()
st.subheader("✏ Update Player Runs")

col3, col4 = st.columns(2)

with col3:
    update_id = st.text_input("Player ID to Update")

with col4:
    new_runs = st.number_input("New Runs", min_value=0)

if st.button("🔄 Update"):
    if not update_id.isdigit():
        st.error("Invalid Player ID")
    else:
        try:
            cur.execute("""
                UPDATE players 
                SET runs = %s 
                WHERE player_id = %s
            """, (new_runs, int(update_id)))

            conn.commit()
            st.success("✅ Updated successfully!")

        except Exception as e:
            st.error(e)

# ---------------- DELETE ----------------
st.divider()
st.subheader("🗑 Delete Player")

delete_id = st.text_input("Player ID to Delete")

if st.button(" Delete"):
    if not delete_id.isdigit():
        st.error(" Invalid Player ID")
    else:
        try:
            cur.execute("DELETE FROM players WHERE player_id = %s", (int(delete_id),))
            conn.commit()
            st.success("✅ Player deleted!")

        except Exception as e:
            st.error(e)

# ---------------- CLOSE ----------------
cur.close()
conn.close()