from sofascoreclient import Sofascore
from team import normalize_team

def upsert_team(db):
    db.execute("""
        INSERT INTO team (
            external_id,
            name,
            national
        )
        VALUES (
            %(external_id)s,
            %(name)s,
            %(national)s
        )
        ON CONFLICT (external_id)
        DO UPDATE SET
    """,) ################################################################

def sync_teams(db, competition_id):
    client = Sofascore()

    seasons = client.get_seasons(competition_id)
    season = max(seasons, key=lambda s: s["year"]) # Se supone que devuelve la temporada actual

    data = client.get_standings(competition_id, season["id"])
    #------------------ ARREGLAR ---------------------------
    champion = data["standings"][0]["rows"][0]["team"] # Supuesto campeon

    map_team = normalize_team(champion)

    upsert_team(db)