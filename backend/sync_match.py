from sofascoreclient import Sofascore
from match import normalize_match

def upsert_match(db, match):
    return db.fetch_one("""
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
            status = EXCLUDED.status,
            overtime_home_goals = EXCLUDED.overtime_home_goals,
            overtime_away_goals = EXCLUDED.overtime_away_goals,
            penalties_home_goals = EXCLUDED.penalties_home_goals,
            penalties_away_goals = EXCLUDED.penalties_away_goals,
            match_type = EXCLUDED.match_type,
            referenced_match = EXCLUDED.referenced_match
        RETURNING id
    """, match)[0]

def finished_match(prev_status, new_status):
    return prev_status != "finished" and new_status == "finished"

def get_internal_season_id(db, season_id):
    return db.fetch_one("SELECT id FROM season WHERE external_id = %s",(season_id,))[0]

def get_internal_team_id(db, team_id: int) -> int:
    return db.fetch_one("SELECT id FROM team WHERE external_id = %s",(team_id,))[0]

def get_internal_referenced_match(db, match_id: int | None) -> int:
    if match_id == None:
        return None
    result = db.fetch_one("SELECT id FROM match_ WHERE external_id = %s",(match_id,))
    if result:
        return result[0]
    else:
        return None
    
def get_matches_id(db, season_id):
    return db.fetch_all("SELECT id FROM match_ WHERE season_id = %s", (season_id,))

def link_first_and_secondleg(db, secondleg_id, first_leg_id):
    db.execute("""
        UPDATE match_
        SET referenced_match = %s, match_type = 'firstleg', qualified_team_id = NULL
        WHERE id = %s
    """, (secondleg_id, first_leg_id))

def sync_matches(db, competition_id):
    client = Sofascore()

    seasons = client.get_seasons(competition_id)
    current_season_id = seasons[0]["id"] # current season ID
    
    matches = client.get_matches(competition_id, current_season_id)

    internal_season_id = get_internal_season_id(db, current_season_id)

    priority_matches = []
    matches_on_hold = []
    matches_id = get_matches_id(db, internal_season_id)

    for match in matches:
        internal_home_team_id = get_internal_team_id(db, match["homeTeam"]["id"])
        internal_away_team_id = get_internal_team_id(db, match["awayTeam"]["id"])
        internal_referenced_match = get_internal_referenced_match(db, match.get("previousLegEventId"))
        play_off = match.get('roundInfo', {}).get('name') != None
        if play_off:
            if match.get("previousLegEventId") != None: # secondleg
                if match["aggregatedWinnerCode"] == 1:
                    internal_qualified_team_id = internal_home_team_id
                else:
                    internal_qualified_team_id = internal_away_team_id
            else: # single match or firstleg (then it removes the qualified team)
                if match["winnerCode"] == 1:
                    internal_qualified_team_id = internal_home_team_id
                else:
                    internal_qualified_team_id = internal_away_team_id
        else:
            internal_qualified_team_id = None

        map_match = normalize_match(match, internal_season_id, internal_home_team_id, internal_away_team_id, internal_qualified_team_id, internal_referenced_match)

        if not play_off:
            priority_matches.append(map_match) 
        elif match.get("previousLegEventId") == None:
            priority_matches.append(map_match)
        elif internal_referenced_match in matches_id:
            priority_matches.append(map_match)
        else:
            matches_on_hold.append(map_match)

    single_matches = []

    for match in priority_matches:
        existing = db.fetch_one(
            "SELECT status FROM match_ WHERE external_id = %s",
            (match["external_id"],)
        )

        internal_match_id = upsert_match(db, match)

        if match["referenced_match"] != None:
            link_first_and_secondleg(db, internal_match_id, match["referenced_match"])

        if existing and finished_match(existing[0], match["status"]) and match["match_type"] == 'single':
            single_matches.append(match)
        elif existing and finished_match(existing[0], match["status"]):
            evaluate_match_predictions(db, match)

    for match in matches_on_hold:
        existing = db.fetch_one(
            "SELECT status FROM match_ WHERE external_id = %s",
            (match["external_id"],)
        )

        internal_match_id = upsert_match(db, match)

        if match["referenced_match"] != None:
            print(internal_match_id)
            link_first_and_secondleg(db, internal_match_id, match["referenced_match"])

        if existing and finished_match(existing[0], match["status"]):
            evaluate_match_predictions(db, match)

    for match in single_matches:
        evaluate_match_predictions(db, match)

def calculate_points(match, pred_h, pred_a, pred_qualified_team):
    points = 0

    if match["home_goals"] == pred_h and match["away_goals"] == pred_a:
        points += 3

    real_result = (
        "H" if match["home_goals"] > match["away_goals"] else
        "A" if match["away_goals"] > match["home_goals"] else
        "D"
    )

    pred_result = (
        "H" if pred_h > pred_a else
        "A" if pred_a > pred_h else
        "D"
    )

    if real_result == pred_result:
        points +=  1
    
    if pred_qualified_team != None and pred_qualified_team == match["qualified_team_id"]:
        points += 2

    return points

def evaluate_match_predictions(db, match):
    preds = db.fetch_all("""
        SELECT id, home_goals, away_goals, user_id, tournament_id, qualified_team_id
        FROM match_prediction
        WHERE match_id = %s AND evaluated = FALSE
    """, (match["id"],))

    for p in preds:
        points = calculate_points(match, p["home_goals"], p["away_goals"], p["qualified_team_id"])

        # mark prediction 
        db.execute("""
            UPDATE match_prediction
            SET evaluated = TRUE
            WHERE id = %s
        """, (p["id"]))

        # add to ranking
        db.execute("""
            INSERT INTO score (user_id, tournament_id, points)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, tournament_id)
            DO UPDATE SET points = score.points + EXCLUDED.points
        """, (p["user_id"], p["tournament_id"], points))