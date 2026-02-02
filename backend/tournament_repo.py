from database import Database

def registration(db, user_id, tournament_id):
    query = """
        INSERT INTO registration (user_id, tournament_id) VALUES (%s, %s)
    """

    db.execute(query, (user_id, tournament_id))

    query = """
        INSERT INTO score (user_id, tournament_id, points) VALUES (%s, %s, 0)
    """

    db.execute(query, (user_id, tournament_id))

    query = """
        INSERT INTO special_prediction (user_id, tournament_id) VALUES (%s, %s)
    """

    db.execute(query, (user_id, tournament_id))

def get_season(db, competition_id):
    query = """
        SELECT id
        FROM season
        WHERE competition_id = %s
        ORDER BY external_id DESC
        LIMIT 1
    """

    return db.fetch_one(query, (competition_id,))[0]

def insert(user_id, competition_id, participant_limit, entry_price, public, password):
    db = Database()
    
    season_id = get_season(db, competition_id)

    query = """
        INSERT INTO tournament (
            competition_id,
            season_id,
            registered_participants,
            participant_limit,
            entry_price,
            public,
            password
        )
        VALUES (%s, %s, 1, %s, %s, %s, %s)
        RETURNING id;
    """
    tournament_id = db.fetch_one(query, (
        competition_id,
        season_id,
        participant_limit,
        entry_price,
        public,
        password
    ))[0]

    registration(db, user_id, tournament_id)

    return tournament_id

def fetch_all(user_id):
    db = Database()
    
    query = """
        SELECT t.id,
            c.name,
            c.id as competition_id,
            t.open,
            t.registered_participants,
            t.participant_limit,
            t.entry_price,
            t.public,
            t.password,
            c.image_name
        FROM tournament t
        JOIN competition c ON t.competition_id = c.id
        WHERE NOT EXISTS (
            SELECT 1
            FROM registration r
            WHERE r.tournament_id = t.id
            AND r.user_id = %s
        )
    """
    return db.fetch_all(query, (user_id,))

def fetch_competitions():
    db = Database()
    
    query = """
        SELECT id, name, image_name
        FROM competition
    """
    return db.fetch_all(query)

def fetch_by_user_id(user_id):
    db = Database()

    query = """
        SELECT t.id,
               c.name,
               c.id as competition_id,
               t.open,
               t.registered_participants,
               t.participant_limit,
               t.entry_price,
               t.public,
               t.password,
               c.image_name
        FROM registration r
        INNER JOIN tournament t ON r.tournament_id = t.id
        INNER JOIN competition c ON t.competition_id = c.id
        WHERE r.user_id = %s
    """

    return db.fetch_all(query, (user_id,))

def fetch_by_id(tournament_id):
    db = Database()

    query = """
        SELECT t.id,
               c.name,
               c.id as competition_id,
               t.open,
               t.registered_participants,
               t.participant_limit,
               t.entry_price,
               t.public,
               t.password,
               c.image_name
        FROM tournament as t
        INNER JOIN competition as c ON c.id = t.competition_id
        WHERE t.id = %s
    """

    return db.fetch_all(query, (tournament_id,))

def fetch_standings(tournament_id):
    db = Database()

    query = """
        SELECT u.name, s.points
        FROM score as s
        INNER JOIN user_ as u ON u.id = s.user_id
        WHERE s.tournament_id = %s
        ORDER BY s.points DESC
    """

    return db.fetch_all(query, (tournament_id,))

def fetch_matches(tournament_id, user_id):
    db = Database()

    query = """
        SELECT  
            m.id,
            m.date,
            th.name AS home_team_name,
            ta.name AS away_team_name,
            m.home_goals,
            m.away_goals,
            m.status,
            th.image_name AS home_team_image,
            ta.image_name AS away_team_image,
            p.home_goals AS predicted_home_goals,
            p.away_goals AS predicted_away_goals,
            rm.home_goals AS referenced_home_goals,
            rm.away_goals AS referenced_away_goals,
            rm.status as referenced_status,
            m.match_type,
            m.overtime_home_goals,
            m.overtime_away_goals,
            m.penalties_home_goals,
            m.penalties_away_goals,
            th.id as home_team_id,
            ta.id as away_team_id,
            m.round,
            m.round_name,
            m.order_index
        FROM tournament t
        JOIN match_ m 
            ON m.season_id = t.season_id
        JOIN team th 
            ON m.home_team_id = th.id
        JOIN team ta 
            ON m.away_team_id = ta.id
        LEFT JOIN match_prediction p 
            ON p.match_id = m.id
            AND p.tournament_id = t.id
            AND p.user_id = %s
        LEFT JOIN match_ rm
            ON rm.id = m.referenced_match
        WHERE t.id = %s
        ORDER BY m.date ASC;
    """

    return db.fetch_all(query, (user_id, tournament_id))

def fetch_scorers(tournament_id):
    db = Database()

    query = """
        SELECT p.name, g.goals
        FROM goalscorers as g
        INNER JOIN player as p ON p.id = g.player_id
        JOIN tournament as t ON t.season_id = g.season_id
        WHERE t.id = %s 
        ORDER BY g.goals DESC
    """

    return db.fetch_all(query, (tournament_id,))

def fetch_teams(tournament_id):
    db = Database()

    query = """
        SELECT te.id, te.name, te.image_name
        FROM team as te
        INNER JOIN team_participations as tp ON tp.team_id = te.id
        INNER JOIN tournament as t ON tp.season_id = t.season_id
        WHERE t.id = %s
        ORDER BY te.name
    """

    return db.fetch_all(query, (tournament_id,))

def inscription(user_id, tournament_id):
    db = Database()

    query = """
        UPDATE tournament
        SET registered_participants = registered_participants + 1
        WHERE id = %s AND registered_participants < participant_limit
    """

    db.execute(query, (tournament_id,))

    registration(db, user_id, tournament_id)

def fetch_inscription(tournament_id, user_id):
    db = Database()

    query = """
        SELECT id FROM registration WHERE tournament_id = %s AND user_id = %s
    """

    return db.fetch_all(query, (tournament_id, user_id))

def delete_user(user_id, tournament_id):
    db = Database()
    
    query = """
        DELETE FROM registration WHERE user_id = %s AND tournament_id = %s
    """

    db.execute(query, (user_id, tournament_id))

    query = """
        DELETE FROM score WHERE user_id = %s AND tournament_id = %s
    """

    db.execute(query, (user_id, tournament_id))

    query = """
        DELETE FROM special_prediction WHERE user_id = %s AND tournament_id = %s
    """

    db.execute(query, (user_id, tournament_id))

    query = """
        DELETE FROM match_prediction WHERE user_id = %s AND tournament_id = %s
    """

    db.execute(query, (user_id, tournament_id))

    query = """
        UPDATE tournament
        SET registered_participants = registered_participants - 1
        WHERE id = %s AND registered_participants > 0
    """

    db.execute(query, (tournament_id,))

    return tournament_id

def update_special_prediction(data, user_id):
    db = Database()

    query = """
        UPDATE special_prediction 
        SET champion_id = %s
        WHERE tournament_id = %s AND user_id = %s 
    """

    db.execute(query, (data.champion_id, data.tournament_id, user_id))

def upsert_match_prediction(tournament_id, match_id, data, user_id):
    db = Database()

    ############ FALTA QUALIFIED TEAM ID
    query = """
        INSERT INTO match_prediction (
            user_id,
            tournament_id,
            match_id,
            home_goals,
            away_goals,
            qualified_team_id
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id, tournament_id, match_id)
        DO UPDATE SET
            home_goals = EXCLUDED.home_goals,
            away_goals = EXCLUDED.away_goals,
            qualified_team_id = EXCLUDED.qualified_team_id
    """

    db.execute(query, (user_id, tournament_id, match_id, data.home_goals, data.away_goals, data.qualified_team_id))

def get_champion_id_prediction(tournament_id, user_id):
    db = Database()

    query = """
        SELECT champion_id
        FROM special_prediction
        WHERE tournament_id = %s AND user_id = %s
    """

    return db.fetch_one(query,(tournament_id,user_id))