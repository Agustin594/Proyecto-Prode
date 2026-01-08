from sofascoreclient import Sofascore

def normalize_season(season_id: int, internal_competition_id: int) -> dict:
    return {
        "external_id": season_id,
        "competition_id": internal_competition_id
    }