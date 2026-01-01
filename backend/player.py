from sofascoreclient import Sofascore
from pprint import pprint

def normalize_player(raw) -> dict:
    return {
        "external_id": raw["player"]["id"],
        "name": raw["player"]["name"],
        "team_id": raw["team"]["id"]
    }