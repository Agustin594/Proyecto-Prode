from sofascoreclient import Sofascore
from match import normalize_match

def upsert_match(db, match):
    db.execute("""
        INSERT INTO match_ (
            external_id,
            season_id,
            date,
            home_team_id,
            away_team_id,
            home_goals,
            away_goals,
            qualified_team_id,
            status,
            overtime_home_goals,
            overtime_away_goals,
            penalties_home_goals,
            penalties_away_goals,
            match_type,
            referenced_match
        )
        VALUES (
            %(external_id)s,
            %(season_id)s,
            %(date)s,
            %(home_team_id)s,
            %(away_team_id)s,
            %(home_goals)s,
            %(away_goals)s,
            %(qualified_team_id)s,
            %(status)s,
            %(overtime_home_goals)s,
            %(overtime_away_goals)s,
            %(penalties_home_goals)s,
            %(penalties_away_goals)s,
            %(match_type)s,
            %(referenced_match)s
        )
        ON CONFLICT (external_id)
        DO UPDATE SET
            home_goals = EXCLUDED.home_goals,
            away_goals = EXCLUDED.away_goals,
            date = EXCLUDED.date,
            qualified_team_id = EXCLUDED.qualified_team_id,
            status = EXCLUDED.status
            overtime_home_goals = EXCLUDED.overtime_home_goals,
            overtime_away_goals = EXCLUDED.overtime_away_goals,
            penalties_home_goals = EXCLUDED.penalties_home_goals,
            penalties_away_goals = EXCLUDED.penalties_away_goals,
            match_type = EXCLUDED.match_type,
            referenced_match = EXCLUDED.referenced_match
    """, match)

def finished_match(prev_status, new_status):
    return prev_status != "finished" and new_status == "finished"

def get_internal_season_id(db, season_id):
    return db.fetch_one("SELECT id FROM season WHERE external_id = %s",(season_id,))[0]

def get_internal_team_id(db, team_id: int) -> int:
    return db.fetch_one("SELECT id FROM team WHERE external_id = %s",(team_id,))[0]

def sync_matches(db, competition_id):
    client = Sofascore()

    seasons = client.get_seasons(competition_id)
    current_season_id = seasons[0]["id"] # current season ID
    
    matches = client.get_matches(competition_id, current_season_id)

    internal_season_id = get_internal_season_id(db, current_season_id)

    for match in matches:
        internal_home_team_id = get_internal_team_id(db, match["homeTeam"]["id"])
        internal_away_team_id = get_internal_team_id(db, match["awayTeam"]["id"])
        play_off = match.get('roundInfo', {}).get('name') != None
        if play_off:
            if match["status"]["type"] == "finished":
                if match["homeScore"]["current"] > match["awayScore"]["current"]: # VER PENALES
                    internal_qualified_team_id = internal_home_team_id
                else:
                    internal_qualified_team_id = internal_away_team_id
            else:
                internal_qualified_team_id = None
        else:
            internal_qualified_team_id = None

        map_match = normalize_match(match, internal_season_id, internal_home_team_id, internal_away_team_id, internal_qualified_team_id)

        existing = db.fetch_one(
            "SELECT status FROM match_ WHERE external_id = %s",
            (map_match["external_id"],)
        )

        upsert_match(db, map_match)

        if existing and finished_match(existing[0], map_match["status"]):
            evaluate_match_predictions(db,match_id=map_match["external_id"],real_h=map_match["home_goals"],real_a=map_match["away_goals"])

def calculate_points(real_h, real_a, pred_h, pred_a):
    if real_h == pred_h and real_a == pred_a:
        return 3

    real_result = (
        "H" if real_h > real_a else
        "A" if real_a > real_h else
        "D"
    )

    pred_result = (
        "H" if pred_h > pred_a else
        "A" if pred_a > pred_h else
        "D"
    )

    if real_result == pred_result:
        return 1

    return 0

def evaluate_match_predictions(db, match_id, real_h, real_a):
    preds = db.fetch_all("""
        SELECT id, home_goals, away_goals, user_id, tournament_id, qualified_team_id
        FROM match_prediction
        WHERE match_id = %s AND evaluated = FALSE
    """, (match_id,))

    for p in preds:
        points = calculate_points(
            real_h, real_a,
            p["pred_home_goals"], p["pred_away_goals"]
        )

        # marcar predicción
        db.execute("""
            UPDATE match_prediction
            SET evaluated = TRUE
            WHERE id = %s
        """, (p["id"]))

        # sumar al ranking
        db.execute("""
            INSERT INTO score (user_id, tournament_id, points)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, tournament_id)
            DO UPDATE SET points = score.points + EXCLUDED.points
        """, (p["user_id"], p["tournament_id"], points))