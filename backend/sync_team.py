from sofascoreclient import Sofascore
from team import normalize_team

def upsert_team(db, team):
    # Agregar image_name
    db.execute("""
        INSERT INTO team (
            external_id,
            name,
            national,
            season_id 
        )
        VALUES (
            %(external_id)s,
            %(name)s,
            %(national)s,
            %(season_id)s
        )
        ON CONFLICT (external_id, season_id)
        DO UPDATE SET
            name = EXCLUDED.name
    """, team)

def get_internal_season_id(db, season_id):
    return db.fetch_one("SELECT id FROM season WHERE external_id = %s",(season_id,))[0]

def sync_teams(db, competition_id):
    client = Sofascore()

    seasons = client.get_seasons(competition_id)
    current_season = seasons[0]

    teams = client.get_teams(competition_id, current_season["id"])

    internal_season_id = get_internal_season_id(db, current_season["id"])

    for team in teams:
        map_team = normalize_team(team, internal_season_id)
        upsert_team(db, map_team)