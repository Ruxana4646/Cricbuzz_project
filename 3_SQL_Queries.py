import streamlit as st
import pandas as pd
from db_connection import get_connection

st.title("🔍 SQL Queries Dashboard")

conn = get_connection()

# 🎯 ALL 25 QUERIES
queries = {

    #  Beginner
    "1. Top Run Scorers": """
        SELECT name, SUM(runs) AS total_runs
        FROM players
        GROUP BY name
        ORDER BY total_runs DESC
        LIMIT 10;
    """,

    "2. Matches in Last 30 Days": """
        SELECT match_desc, team1, team2, venue, city, start_date
        FROM matches
        WHERE start_date >= NOW() - INTERVAL 30 DAY;
    """,

    "3. Matches per Team": """
        SELECT team1 AS team, COUNT(*) AS matches
        FROM matches
        GROUP BY team1;
    """,

    "4. Players per Match": """
        SELECT match_id, COUNT(*) AS total_players
        FROM players
        GROUP BY match_id;
    """,

    "5. Highest Score": """
        SELECT name, MAX(runs) AS highest
        FROM players
        GROUP BY name
        ORDER BY highest DESC
        LIMIT 5;
    """,

    "6. Matches per City": """
        SELECT city, COUNT(*) AS matches
        FROM matches
        GROUP BY city;
    """,

    "7. Average Runs per Player": """
        SELECT name, AVG(runs) AS avg_runs
        FROM players
        GROUP BY name;
    """,

    "8. Total Runs per Match": """
        SELECT match_id, SUM(runs) AS total_runs
        FROM players
        GROUP BY match_id;
    """,

    #  Intermediate
    "9. Top Strike Rate Players": """
        SELECT name, AVG(strike_rate) AS avg_sr
        FROM players
        GROUP BY name
        ORDER BY avg_sr DESC
        LIMIT 5;
    """,

    "10. High Scoring Matches": """
        SELECT match_id, SUM(runs) AS total_runs
        FROM players
        GROUP BY match_id
        ORDER BY total_runs DESC
        LIMIT 5;
    """,

    "11. Player Match Performance": """
        SELECT p.name, m.match_desc, p.runs
        FROM players p
        JOIN matches m ON p.match_id = m.match_id;
    """,

    "12. Players Scoring 50+": """
        SELECT name, runs
        FROM players
        WHERE runs >= 50;
    """,

    "13. Venue Wise Runs": """
        SELECT m.venue, SUM(p.runs) AS total_runs
        FROM matches m
        JOIN players p ON m.match_id = p.match_id
        GROUP BY m.venue;
    """,

    "14. Boundary Hitters": """
        SELECT name, SUM(fours + sixes) AS boundaries
        FROM players
        GROUP BY name
        ORDER BY boundaries DESC;
    """,

    "15. Total Match Runs": """
        SELECT match_id, team1_runs + team2_runs AS total
        FROM matches
        ORDER BY total DESC;
    """,

    "16. Players Never Out for Zero": """
        SELECT name
        FROM players
        GROUP BY name
        HAVING MIN(runs) > 0;
    """,

    #  Advanced
    "17. Rank Players": """
        SELECT name, SUM(runs) AS total_runs,
        RANK() OVER (ORDER BY SUM(runs) DESC) AS rank_pos
        FROM players
        GROUP BY name;
    """,

    "18. Consistent Players": """
        SELECT name, AVG(runs) AS avg_runs, STDDEV(runs) AS consistency
        FROM players
        GROUP BY name
        ORDER BY consistency ASC;
    """,

    "19. Match Strike Rate": """
        SELECT match_id, AVG(strike_rate) AS avg_sr
        FROM players
        GROUP BY match_id
        ORDER BY avg_sr DESC;
    """,

    "20. Team Total Runs": """
        SELECT team1 AS team, SUM(team1_runs) AS runs
        FROM matches
        GROUP BY team1;
    """,

    "21. Contribution %": """
        SELECT name, match_id,
        (runs / SUM(runs) OVER (PARTITION BY match_id)) * 100 AS contribution
        FROM players;
    """,

    "22. Top Player per Match": """
        SELECT *
        FROM (
            SELECT name, match_id, runs,
            RANK() OVER (PARTITION BY match_id ORDER BY runs DESC) rnk
            FROM players
        ) t
        WHERE rnk = 1;
    """,

    "23. Rolling Average": """
        SELECT name, match_id, runs,
        AVG(runs) OVER (
            PARTITION BY name
            ORDER BY match_id
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS rolling_avg
        FROM players;
    """,

    "24. Most Active Venue": """
        SELECT venue, COUNT(*) AS matches
        FROM matches
        GROUP BY venue
        ORDER BY matches DESC
        LIMIT 1;
    """,

    "25. Performance Trend": """
        SELECT name, match_id, runs,
        LAG(runs) OVER (PARTITION BY name ORDER BY match_id) AS prev_runs
        FROM players;
    """
}

#  Dropdown
selected_query = st.selectbox("Choose a query", list(queries.keys()))

# ▶️ Run predefined query
if st.button("Run Selected Query"):
    df = pd.read_sql(queries[selected_query], conn)
    st.dataframe(df)

#  Custom query
st.subheader(" Run Your Own SQL Query")

user_query = st.text_area("Enter SQL Query")

if st.button("Run Custom Query"):
    try:
        df = pd.read_sql(user_query, conn)
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error: {e}")