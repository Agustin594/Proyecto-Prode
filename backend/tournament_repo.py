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

def insert(user_id, competition_id, participant_limit, entry_price, public):
    db = Database()
    
    query = """
        INSERT INTO tournament (
            competition_id,
            registered_participants,
            participant_limit,
            entry_price,
            public
        )
        VALUES (%s, 1, %s, %s, %s)
        RETURNING id;
    """
    tournament_id = db.fetch_one(query, (
        competition_id,
        participant_limit,
        entry_price,
        public
    ))[0]

    registration(db, user_id, tournament_id)

    return tournament_id

def fetch_all():
    db = Database()
    
    query = """
        SELECT t.id, c.name, t.open, t.registered_participants, t.participant_limit, t.entry_price, t.public
        FROM tournament as t INNER JOIN competition as c ON t.competition_id = c.id
    """
    return db.fetch_all(query)

def fetch_competitions():
    db = Database()
    
    query = """
        SELECT id, name
        FROM competition
    """
    return db.fetch_all(query)

def fetch_by_user_id(user_id):
    db = Database()

    query = """
        SELECT t.id,
               c.name,
               t.open,
               t.registered_participants,
               t.participant_limit,
               t.entry_price,
               t.public
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
               t.open,
               t.registered_participants,
               t.participant_limit,
               t.entry_price,
               t.public
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

def fetch_matches(tournament_id):
    db = Database()

    query = """
        SELECT m.id,
            m.date,
            th.name AS home_team_name,
            ta.name AS away_team_name,
            m.home_goals,
            m.away_goals
        FROM match_ as m
        JOIN team as th ON m.home_team_id = th.id
        JOIN team as ta ON m.away_team_id = ta.id
        JOIN tournament as t ON t.competition_id = m.competition_id
        WHERE t.id = %s 
        ORDER BY m.date ASC
    """

    return db.fetch_all(query, (tournament_id,))

def fetch_scorers(tournament_id):
    db = Database()

    query = """
        SELECT p.name, g.goals
        FROM goalscorers as g
        INNER JOIN player as p ON p.id = g.player_id
        JOIN tournament as t ON t.competition_id = g.competition_id
        WHERE t.id = %s 
        ORDER BY g.goals DESC
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
        SET champion_id = %s, top_scorer_id = %s
        WHERE tournament_id = %s AND user_id %s 
    """

    db.execute(query, (data.champion_id, data.top_scorer_id, data.tournament_id, user_id))