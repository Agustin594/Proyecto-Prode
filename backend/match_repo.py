from database import Database
from datetime import date, timedelta

def fetch_all_matches(date):
    db = Database()

    start_date = date
    end_date = date + timedelta(days=1)

    query = """
        SELECT 
            m.id,
            m.date,
            th.name AS home_team_name,
            ta.name AS away_team_name,
            m.home_goals,
            m.away_goals,
            m.status,
            c.id AS competition_id,
            c.name AS competition_name
        FROM match_ as m
        JOIN team as th 
            ON m.home_team_id = th.id
        JOIN team as ta 
            ON m.away_team_id = ta.id
        JOIN season as s
            ON s.id = m.season_id
        JOIN competition as c
            ON c.id = s.competition_id
        WHERE m.date >= %s AND m.date < %s
        ORDER BY c.id ASC, m.date ASC
    """

    return db.fetch_all(query, (start_date, end_date))

def fetch_personal_matches(date, user_id):
    db = Database()

    start_date = date
    end_date = date + timedelta(days=1)

    query = """
        SELECT 
            m.id,
            m.date,
            th.name AS home_team_name,
            ta.name AS away_team_name,
            m.home_goals,
            m.away_goals,
            m.status,
            c.id AS competition_id,
            c.name AS competition_name
        FROM match_ as m
        JOIN team as th 
            ON m.home_team_id = th.id
        JOIN team as ta 
            ON m.away_team_id = ta.id
        JOIN season as s
            ON s.id = m.season_id
        JOIN competition as c
            ON c.id = s.competition_id
        JOIN tournament as t
            ON t.season_id = s.id
        JOIN registration as r
            ON r.tournament_id = t.id
        WHERE m.date >= %s AND m.date < %s AND r.user_id = %s
        ORDER BY c.id ASC, m.date ASC
    """

    return db.fetch_all(query, (start_date, end_date, user_id))