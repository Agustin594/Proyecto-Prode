from sofascoreclient import Sofascore
from team import normalize_team

def upsert_team(db, team):
    # Agregar image_name
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
            name = EXCLUDED.name
    """, team) 

def sync_teams(db, competition_id):
    client = Sofascore()

    seasons = client.get_seasons(competition_id)
    current_season = seasons[0]

    teams = client.get_teams(competition_id, current_season["id"])

    for team in teams:
        map_team = normalize_team(team)
        upsert_team(db, map_team)