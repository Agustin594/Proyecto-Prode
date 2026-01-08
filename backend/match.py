from sofascoreclient import Sofascore 
from datetime import datetime

def normalize_match(raw: dict, internal_season_id: int, internal_home_team_id: int, internal_away_team_id: int, internal_qualified_team_id: int) -> dict:
    play_off = raw.get('roundInfo', {}).get('name') != None

    return {
        "external_id": raw["id"],
        "season_id": internal_season_id,
        "date": datetime.fromtimestamp(raw["startTimestamp"]),
        "home_team_id": internal_home_team_id,
        "away_team_id": internal_away_team_id,
        "home_goals": raw.get("homeScore", {}).get("current"),
        "away_goals": raw.get("awayScore", {}).get("current"),
        "play_off": play_off,
        "qualified_team_id": internal_qualified_team_id,
        "status": raw["status"]["type"]
    }