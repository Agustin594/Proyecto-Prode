from sofascoreclient import Sofascore 
from datetime import datetime

ROUND_TYPE_BASE_ORDER = {
    "qualification": 0,
    "group": 1000,
    "knockout": 2000
}

def calculate_points_for_round(round_number: int, round_name: str | None):
    if round_name == None:
        return ROUND_TYPE_BASE_ORDER.get("group") + round_number
    elif "Qualification" in round_name or "Playoff" in round_name:
        return ROUND_TYPE_BASE_ORDER.get("qualification") + round_number
    else:
        return ROUND_TYPE_BASE_ORDER.get("knockout") + round_number


def normalize_match(raw: dict, internal_season_id: int, internal_home_team_id: int, internal_away_team_id: int, internal_qualified_team_id: int, internal_referenced_match: int) -> dict:
    if raw.get('roundInfo', {}).get('name') == None:
        match_type = 'points'
    elif raw.get("previousLegEventId") != None:
        match_type = 'secondleg'
    else: # single or firstleg (then it changes)
        match_type = 'single'

    return {
        "external_id": raw["id"],
        "season_id": internal_season_id,
        "date": datetime.fromtimestamp(raw["startTimestamp"]),
        "home_team_id": internal_home_team_id,
        "away_team_id": internal_away_team_id,
        "home_goals": raw.get("homeScore", {}).get("normaltime"),
        "away_goals": raw.get("awayScore", {}).get("normaltime"),
        "overtime_home_goals": raw.get("homeScore", {}).get("overtime"),
        "overtime_away_goals": raw.get("awayScore", {}).get("overtime"),
        "penalties_home_goals": raw.get("homeScore", {}).get("penalties"),
        "penalties_away_goals": raw.get("awayScore", {}).get("penalties"),
        "qualified_team_id": internal_qualified_team_id,
        "status": raw["status"]["type"],
        "match_type": match_type,
        "referenced_match": internal_referenced_match,
        "round": raw.get('roundInfo', {}).get('round'),
        "round_name": raw.get('roundInfo', {}).get('name'),
        "order_index": calculate_points_for_round(raw.get('roundInfo', {}).get('round'), raw.get('roundInfo', {}).get('name'))
    }