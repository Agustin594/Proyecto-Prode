from sofascoreclient import Sofascore
from competition import normalize_competition

def upsert_competition(db, competition):
    db.execute("""
        INSERT INTO competition (
            external_id,
            name,
            season,
            start_date,
            end_date,
            champion_id
        )
        VALUES (
            %(external_id)s,
            %(name)s,
            %(season)s,
            %(start_date)s,
            %(end_date)s,
            %(champion_id)s
        )
        ON CONFLICT (external_id)
        DO UPDATE SET
            season = EXCLUDED.season,
            start_date = EXCLUDED.start_date,
            end_date = EXCLUDED.end_date,
            champion_id = EXCLUDED.champion_id
    """, competition)

def sync_competitions(db, competition_id):
    client = Sofascore()

    seasons = client.get_seasons(competition_id)
    season = max(seasons, key=lambda s: s["year"]) # Se supone que devuelve la temporada actual
    
    info = client.get_competition(competition_id)

    data = client.get_champion(competition_id, season["id"])
    if data != None:
        champion_id = data["id"]
    else:
        champion_id = None

    map_competition = normalize_competition(info, season, champion_id)

    upsert_competition(db, map_competition)   

    #now = "tiempo actual" ###############################################################
    #if now > map_competition["end_date"]:
    #    update_tournament_data(db, competition_id)
    #    evaluate_general_predictions(db, competition_id, map_competition["champion_id"], map_competition["top_scorer_id"])


def calculate_points(real_champion, real_top_scorer, pred_champion, pred_top_scorer):
    points = 0
    
    if real_champion == pred_champion:
        points += 5

    if real_top_scorer == pred_top_scorer:
        points += 5

    return points

def evaluate_general_predictions(db, competition_id, real_champion, real_goalscorer):
    tournaments = db.fetch_all("""
        SELECT id
        FROM tournament
        WHERE competition_id = %s
    """, (competition_id,))
    
    for tournament in tournaments:
        preds = db.fetch_all("""
            SELECT id, champion_id, top_scorer_id, user_id, tournament_id
            FROM special_prediction
            WHERE tournament_id = %s AND evaluated = FALSE
        """, (tournament["id"],))

    for p in preds:
        points = calculate_points(
            real_champion, real_goalscorer,
            p["champion_id"], p["top_scorer_id"]
        )

        # marcar predicción
        db.execute("""
            UPDATE special_prediction
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

def update_tournament_data(db, competition_id):
    db.execute("""
            UPDATE tournament
            SET open = FALSE
            WHERE competition_id = %s
        """, (competition_id))