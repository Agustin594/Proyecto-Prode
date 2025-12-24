from sofascoreclient import Sofascore 
from datetime import datetime

def normalize_competition(info, season, champion, scorer) -> dict:
    return {
        "external_id": info["id"],
        "name": info["name"],
        "season": season["year"],
        "start-time": datetime.fromtimestamp(info["startDateTimestamp"]),
        "end-time": datetime.fromtimestamp(info["endDateTimestamp"]),
        "champion": champion["name"],
        "top-scorer": scorer,
    }

def main():
    client = Sofascore()

    info = client.get_competition(17)

    seasons = client.get_seasons(17)
    season = seasons[0]  # lógica temporada activa

    standings = client.get_standings(7, 61644)

    champion = standings["standings"][0]["rows"][0]["team"]

    print(champion)

    #print(normalize_competition(info, season, champion, scorer="Jose"))

main()