from sofascoreclient import Sofascore 

def normalize_team(raw) -> dict:
    return {
        "external_id": raw["id"],
        "name": raw["name"],
        "national": raw["national"]
    }