from sofascoreclient import Sofascore 
from datetime import datetime

def normalize_competition(info, season, champion) -> dict:
    return {
        "external_id": info["id"],
        "name": info["name"],
        "season": season["year"],
        "start-time": datetime.fromtimestamp(info["startDateTimestamp"]),
        "end-time": datetime.fromtimestamp(info["endDateTimestamp"]),
        "champion": champion
    }