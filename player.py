from sofascoreclient import Sofascore 

def normalize_player(raw) -> dict:
    return {
        "external_id": raw["id"],
        "name": raw["name"],
        "team_id": raw["team"]["id"]
    }