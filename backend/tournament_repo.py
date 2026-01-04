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

def fetch_by_id(user_id):
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

def inscription(user_id, tournament_id):
    db = Database()

    query = """
        UPDATE tournament
        SET registered_participants = registered_participants + 1
        WHERE id = %s AND registered_participants < participant_limit
    """

    db.execute(query, (tournament_id,))

    registration(db, user_id, tournament_id)

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