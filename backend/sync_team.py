from sofascoreclient import Sofascore
from team import normalize_team, normalize_team_participation

def insert_team(db, team):
    return db.execute("""
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
        RETURNING id
    """, team)

def insert_team_participation(db, team_participation):
    db.execute("""
        INSERT INTO team_participations (
            team_id,
            season_id
        )
        VALUES (
            %(team_id)s,
            %(season_id)s
        )
    """, team_participation)

def get_internal_season_id(db, season_id):
    return db.fetch_one("SELECT id FROM season WHERE external_id = %s",(season_id,))[0]

def sync_teams(db, competition_id):
    client = Sofascore()

    seasons = client.get_seasons(competition_id)
    current_season = seasons[0]

    teams = client.get_teams(competition_id, current_season["id"])

    internal_season_id = get_internal_season_id(db, current_season["id"])

    for team in teams:
        internal_id = db.fetch_one("""SELECT id FROM team WHERE external_id = %s""",(team["id"],))

        if not internal_id:
            map_team = normalize_team(team, internal_season_id)
            internal_id = insert_team(db, map_team)
        else:
            internal_id = internal_id[0]
        
        result = db.fetch_one("""SELECT 1 FROM team_participations WHERE team_id = %s AND season_id = %s""",(internal_id, internal_season_id))

        if not result:
            map_team_participation = normalize_team_participation(internal_id, internal_season_id)
            insert_team_participation(db, map_team_participation)