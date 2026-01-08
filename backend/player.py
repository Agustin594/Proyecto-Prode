from sofascoreclient import Sofascore

def normalize_player(raw) -> dict:
    return {
        "external_id": raw["player"]["id"],
        "name": raw["player"]["name"],
        "team_id": raw["team"]["id"],
    }