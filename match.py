from sofascoreclient import Sofascore 

def normalize_match(raw: dict) -> dict:
    return {
        "external_id": raw["id"],
        "start_time": raw["startTimestamp"],
        "home_team_id": raw["homeTeam"]["id"],
        "away_team_id": raw["awayTeam"]["id"],
        "goals_home": raw.get("homeScore", {}).get("current"),
        "goals_away": raw.get("awayScore", {}).get("current"),
        "status": raw["status"]["type"]
    }

def main():
    client = Sofascore()

    raw = client.get_match(12436557)

    print(normalize_match(raw))

main()