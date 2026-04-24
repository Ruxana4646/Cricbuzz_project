import pandas as pd
from db_connection import get_connection


# 🔥 Universal datetime fix
def convert_date(date_val):
    if not date_val:
        return None

    try:
        val = str(date_val)

        if val.isdigit():
            ts = int(val)

            if len(val) >= 13:
                return pd.to_datetime(ts, unit='ms', errors='coerce')
            else:
                return pd.to_datetime(ts, unit='s', errors='coerce')

        return pd.to_datetime(val, errors='coerce')

    except:
        return None


# 🔹 Insert matches
def insert_matches(matches):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    INSERT INTO matches (
        match_id, series_id, series_name, match_desc, match_format,
        status, team1, team2, venue, city,
        start_date, end_date, team1_runs, team2_runs
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE status=VALUES(status)
    """

    values = []

    for m in matches:
        values.append((
            m["match_id"],
            m["series_id"],
            m["series_name"],
            m["match_desc"],
            m["match_format"],
            m["status"],
            m["team1"],
            m["team2"],
            m["venue"],
            m["city"],
            convert_date(m["start_date"]),
            convert_date(m["end_date"]),
            m["team1_runs"] or 0,
            m["team2_runs"] or 0
        ))

    cur.executemany(query, values)
    conn.commit()
    cur.close()
    conn.close()


# 🔹 Insert players
def insert_players(players):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    INSERT INTO players (
        player_id, match_id,
        name, runs, balls, fours, sixes,
        strike_rate, out_desc
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
        runs=VALUES(runs),
        balls=VALUES(balls),
        fours=VALUES(fours),
        sixes=VALUES(sixes),
        strike_rate=VALUES(strike_rate),
        out_desc=VALUES(out_desc)
    """

    values = []

    for p in players:
        values.append((
            p["player_id"],
            p["match_id"],           
            p["name"],
            p["runs"],
            p["balls"],
            p["fours"],
            p["sixes"],
            p["strike_rate"],
            p["out_desc"]
        ))

    cur.executemany(query, values)
    conn.commit()
    cur.close()
    conn.close()