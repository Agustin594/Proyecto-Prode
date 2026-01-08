from sofascoreclient import Sofascore 

def normalize_team(raw, season_id) -> dict:
    return {
        "external_id": raw["id"],
        "name": raw["name"],
        "national": raw["national"],
        "season_id": season_id
    }