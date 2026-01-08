from sofascoreclient import Sofascore
from player import normalize_player

def upsert_player(db, player):
    db.execute("""
        INSERT INTO player (
            external_id,
            name,
            team_id
        )
        VALUES (
            %(external_id)s,
            %(name)s,
            %(team_id)s
        )
        ON CONFLICT (external_id)
        DO UPDATE SET
            team_id = EXCLUDED.team_id
    """, player)

def sync_teams(db, competition_id):
    client = Sofascore()

    seasons = client.get_seasons(competition_id)
    current_season = seasons[0]

    teams = client.get_teams(competition_id, current_season["id"])

    for team in teams:
        players = client.get_players(team) ############# CREAR FUNCION

        for player in players:
            map_player = normalize_player(player)
            upsert_player(db, map_player)