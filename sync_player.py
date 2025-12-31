from sofascoreclient import Sofascore
from player import normalize_player

def upsert_player(db):
    db.execute("""
        INSERT INTO player (
            external_id,
            name,
        )
        VALUES (
            %(external_id)s,
            %(name)s
        )
        ON CONFLICT (external_id)
        DO UPDATE SET
    """,) ################################################################

def sync_teams(db, competition_id):
    client = Sofascore()

    seasons = client.get_seasons(competition_id)
    current_season = seasons[0] # temporada actual

    map_player = normalize_player()

    upsert_player(db)