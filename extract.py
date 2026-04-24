import requests

API_KEY = "b3d7f61023msh362a5491e103391p1f5aecjsnb0cb3e72401e"   # 🔥 replace
API_HOST = "cricbuzz-cricket.p.rapidapi.com"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}


def fetch_api(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except:
        return {}


# 🔹 Extract matches
def extract_matches():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"
    data = fetch_api(url)

    matches = []

    for match_type in data.get("typeMatches", []):
        for series in match_type.get("seriesMatches", []):
            wrapper = series.get("seriesAdWrapper", {})

            for m in wrapper.get("matches", []):
                info = m.get("matchInfo", {})

                matches.append({
                    "match_id": info.get("matchId"),
                    "series_id": wrapper.get("seriesId"),
                    "series_name": wrapper.get("seriesName"),
                    "match_desc": info.get("matchDesc"),
                    "match_format": info.get("matchFormat"),
                    "status": info.get("status"),
                    "team1": info.get("team1", {}).get("teamName"),
                    "team2": info.get("team2", {}).get("teamName"),
                    "venue": info.get("venueInfo", {}).get("ground"),
                    "city": info.get("venueInfo", {}).get("city"),
                    "start_date": info.get("startDate"),
                    "end_date": info.get("endDate"),
                    "team1_runs": 0,
                    "team2_runs": 0
                })

    return matches


# 🔹 Extract players
def extract_players(scorecard, match_id):
    players = []

    for innings in scorecard.get("scorecard", []):
        innings_id = innings.get("inningsId")

        for b in innings.get("batsman", []):
            players.append({
                "player_id": b.get("id"),
                "match_id": match_id,
                "innings_id": innings_id,
                "name": b.get("name"),
                "runs": int(b.get("runs", 0) or 0),
                "balls": int(b.get("balls", 0) or 0),
                "fours": int(b.get("fours", 0) or 0),
                "sixes": int(b.get("sixes", 0) or 0),
                "strike_rate": float(b.get("strkrate") or 0),
                "out_desc": b.get("outdec") or "not out"
            })

    return players