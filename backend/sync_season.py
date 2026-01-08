from sofascoreclient import Sofascore
from season import normalize_season

### POSIBLE REFACTORIZACION
def upsert_season(db, season):
    db.execute("""
        INSERT INTO season (
            external_id,
            competition_id
        )
        VALUES (
            %(external_id)s,
            %(competition_id)s
        )
        ON CONFLICT (external_id)
        DO UPDATE SET
            competition_id = EXCLUDED.competition_id
    """, season)

def get_internal_competition_id(db, competition_id):
    return db.fetch_one("SELECT id FROM competition WHERE external_id = %s",(competition_id,))[0]

def sync_season(db, competition_id):
    client = Sofascore()

    seasons = client.get_seasons(competition_id)
    internal_competition_id = get_internal_competition_id(db, competition_id)
    
    map_season = normalize_season(seasons[0]["id"], internal_competition_id)

    upsert_season(db, map_season)