from sofascoreclient import Sofascore 
from datetime import datetime

def normalize_competition(info, season: dict, champion_id: int) -> dict:
    return {
        "external_id": info["id"],
        "name": info["name"],
        "season": season["year"],
        "start_date": datetime.fromtimestamp(info["startDateTimestamp"]),
        "end_date": datetime.fromtimestamp(info["endDateTimestamp"]),
        "champion_id": champion_id
    }