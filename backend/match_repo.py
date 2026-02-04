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
            c.name AS competition_name,
            th.image_name as home_team_image,
            ta.image_name as away_team_image,
            c.image_name,
            m.overtime_home_goals,
            m.overtime_away_goals,
            m.penalties_home_goals,
            m.penalties_away_goals
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
            c.name AS competition_name,
            th.image_name AS home_team_image,
            ta.image_name AS away_team_image,
            c.image_name,
            m.overtime_home_goals,
            m.overtime_away_goals,
            m.penalties_home_goals,
            m.penalties_away_goals
        FROM match_ AS m
        JOIN team AS th 
            ON m.home_team_id = th.id
        JOIN team AS ta 
            ON m.away_team_id = ta.id
        JOIN season AS s
            ON s.id = m.season_id
        JOIN competition AS c
            ON c.id = s.competition_id
        WHERE m.date >= %s 
        AND m.date < %s
        AND EXISTS (
                SELECT 1
                FROM tournament t
                JOIN registration r 
                    ON r.tournament_id = t.id
                WHERE t.season_id = s.id
                AND r.user_id = %s
        )
        ORDER BY c.id ASC, m.date ASC;
    """

    return db.fetch_all(query, (start_date, end_date, user_id))

def fetch_calendar_matches(month, year, user_id):
    db = Database()

    start = date(year, month, 1)

    if month == 12:
        end = date(year + 1, 1, 1)
    else:
        end = date(year, month + 1, 1)

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
            c.name AS competition_name,
            th.image_name AS home_team_image,
            ta.image_name AS away_team_image,
            c.image_name 
        FROM match_ AS m
        JOIN team AS th 
            ON m.home_team_id = th.id
        JOIN team AS ta 
            ON m.away_team_id = ta.id
        JOIN season AS s
            ON s.id = m.season_id
        JOIN competition AS c
            ON c.id = s.competition_id
        WHERE m.date >= %s 
        AND m.date < %s
        AND EXISTS (
                SELECT 1
                FROM tournament t
                JOIN registration r 
                    ON r.tournament_id = t.id
                WHERE t.season_id = s.id
                AND r.user_id = %s
        )
        ORDER BY m.date ASC;
    """

    return db.fetch_all(query, (start, end, user_id))

def fetch_important_matches():
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
            c.id AS competition_id,
            c.name AS competition_name,
            th.image_name AS home_team_image,
            ta.image_name AS away_team_image,
            c.image_name,
            m.overtime_home_goals,
            m.overtime_away_goals,
            m.penalties_home_goals,
            m.penalties_away_goals
        FROM match_ AS m
        JOIN team AS th 
            ON m.home_team_id = th.id
        JOIN team AS ta 
            ON m.away_team_id = ta.id
        JOIN season AS s
            ON s.id = m.season_id
        JOIN competition AS c
            ON c.id = s.competition_id
        WHERE m.date >= CURRENT_DATE AND m.status IN ('inprogress', 'notstarted');
    """

    return db.fetch_all(query, ())