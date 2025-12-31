from sofascoreclient import Sofascore 
from datetime import datetime

def normalize_match(raw: dict, internal_competition_id: int) -> dict:
    play_off = raw.get('roundInfo', {}).get('name') != None
    if play_off:
        if raw["status"]["type"] == "finished":
            if raw["homeScore"]["current"] > raw["awayScore"]["current"]:
                qualified_team_id = raw["homeTeam"]["id"]
            else:
                qualified_team_id = raw["awayTeam"]["id"]
        else:
            qualified_team_id = None
    else:
        qualified_team_id = None

    return {
        "external_id": raw["id"],
        "competition_id": internal_competition_id,
        "date": datetime.fromtimestamp(raw["startTimestamp"]),
        "home_team_id": raw["homeTeam"]["id"],
        "away_team_id": raw["awayTeam"]["id"],
        "home_goals": raw.get("homeScore", {}).get("current"),
        "away_goals": raw.get("awayScore", {}).get("current"),
        "play_off": play_off,
        "qualified_team_id": qualified_team_id,
        "status": raw["status"]["type"]
    }