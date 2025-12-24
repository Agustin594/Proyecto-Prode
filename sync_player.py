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
    season = max(seasons, key=lambda s: s["year"]) # Se supone que devuelve la temporada actual

    data = client.get_top_players(competition_id, season["id"])
    #------------------ ARREGLAR ---------------------------
    scorer = data[0]["player"] # Supuesto goleador

    map_player = normalize_player(scorer)

    upsert_player(db)