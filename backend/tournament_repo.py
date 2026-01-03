from database import Database

def insert(competition_id, open, participant_limit, entry_price, public):
    db = Database()
    
    query = """
        INSERT INTO tournament (
            competition_id,
            open,
            registered_participants,
            participant_limit,
            entry_price,
            public
        )
        VALUES (%s, %s, 0, %s, %s, %s)
        RETURNING id;
    """
    return db.fetch_one(query, (
        competition_id,
        open,
        participant_limit,
        entry_price,
        public
    ))[0]

def fetch_all():
    db = Database()
    
    query = """
        SELECT t.id, c.name, t.open, t.registered_participants, t.participant_limit, t.entry_price, t.public
        FROM tournament as t INNER JOIN competition as c ON t.competition_id = c.id
    """
    return db.fetch_all(query)