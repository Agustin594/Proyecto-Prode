from sofascoreclient import Sofascore 

def normalize_team(raw) -> dict:
    return {
        "external_id": raw["id"],
        "name": raw["name"],
        "national": raw["national"],
    }

def normalize_team_participation(internal_team_id, season_id) -> dict:
    return {
        "team_id": internal_team_id,
        "season_id": season_id
    }