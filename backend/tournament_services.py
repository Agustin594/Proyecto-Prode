import tournament_repo as tr
import security
from database import Database
from fastapi import HTTPException

def create_tournament(user_id, data):
    db = Database()

    result = db.fetch_one("""SELECT 1 FROM competition WHERE id = %s""", (data.competition_id))

    if not result:
        raise HTTPException(status_code=400, detail="That competition does not exist.")
    
    if data.participant_limit < 5:
        raise HTTPException(status_code=400, detail="Wrong limit to the participants.")
    
    if data.participant_limit > 10000:
        raise HTTPException(status_code=400, detail="Participant limit too high.")
    
    if data.entry_price < 0:
        raise HTTPException(status_code=400, detail="The entry price cannot be negative.")
    
    if data.entry_price > 1000000:
        raise HTTPException(status_code=400, detail="Entry price too high.")
    
    if not data.public and (not data.password or data.password.strip() == ""):
        raise HTTPException(status_code=400, detail="It needs a password.")
    
    if data.public and data.password:
        raise HTTPException(status_code=400, detail="Public tournaments cannot have a password.")

    if data.public:
        password = None
    else:
        password = security.hash_password(data.password)

    return tr.insert(user_id, data.competition_id, data.participant_limit, data.entry_price, data.public, password)

def get_competitions():
    rows = tr.fetch_competitions()

    competitions = []
    for r in rows:
        competitions.append({
            "id": r[0],
            "name": r[1]
        })

    return competitions

def get_tournaments(user_id):
    rows = tr.fetch_all(user_id)

    tournaments = []
    for r in rows:
        tournaments.append({
            "id": r[0],
            "name": r[1],
            "open": r[2],
            "registered_participants": r[3],
            "participant_limit": r[4],
            "entry_price": r[5],
            "public": r[6],
            "password": r[7]
        })

    return tournaments

def get_inscription(tournament_id, user_id): 
    rows = tr.fetch_inscription(tournament_id, user_id)

    data = []
    for r in rows:
        data.append({
            "id": r[0]
        })

    return data

def get_tournaments_by_user_id(user_id):
    rows = tr.fetch_by_user_id(user_id)

    tournaments = []
    for r in rows:
        tournaments.append({
            "id": r[0],
            "name": r[1],
            "open": r[2],
            "registered_participants": r[3],
            "participant_limit": r[4],
            "entry_price": r[5],
            "public": r[6],
            "password": r[7]
        })

    return tournaments

def tournament_inscription(user_id, data):
    db = Database()

    result = db.fetch_one(
        "SELECT public, password FROM tournament WHERE id = %s",
        (data.tournament_id,)
    )

    if not result:
        raise HTTPException(status_code=401, detail="Torneo inexistente.")

    if not result[0] and not security.verify_password(data.password, result[1]):
        raise HTTPException(status_code=401, detail="Contraseña inválida.")

    tr.inscription(user_id, data.tournament_id)

def delete_tournament_user(user_id, data):
    if not isRegistered(user_id, data.tournament_id):
        raise HTTPException(status_code=400, detail="The user is not in that tournament.")

    return tr.delete_user(user_id, data.tournament_id)

def get_tournament_by_id(tournament_id):
    tournament = tr.fetch_by_id(tournament_id)

    t = tournament[0]
    
    return {
        "id": t[0],
        "name": t[1],
        "open": t[2],
        "registered_participants": t[3],
        "participant_limit": t[4],
        "entry_price": t[5],
        "public": t[6],
        "password": t[7]
    }

def get_tournament_standings(tournament_id):
    rows = tr.fetch_standings(tournament_id)

    standings = []
    for r in rows:
        standings.append({
            "user_name": r[0],
            "points": r[1]
        })

    return standings

def get_tournament_matches(tournament_id, user_id):
    rows = tr.fetch_matches(tournament_id, user_id)

    matches = []
    for r in rows:
        matches.append({
            "id": r[0],
            "date": r[1],
            "home_team_name": r[2],
            "away_team_name": r[3],
            "home_goals": r[4],
            "away_goals": r[5],
            "status": r[6],
            "prediction": {
                "home_goals": r[7],
                "away_goals": r[8]
            } if r[7] is not None else None
        })

    return matches

def get_tournament_scorers(tournament_id):
    rows = tr.fetch_scorers(tournament_id)

    scorers = []
    for r in rows:
        scorers.append({
            "id": r[0],
            "name": r[1],
            "goals": r[2]
        })

    return scorers

def update_special_prediction(data, user_id):
    db= Database()

    result = db.fetch_one("""SELECT 1 FROM team as te INNER JOIN tournament as t ON t.season_id = te.season_id WHERE te.id = %s AND t.id = %s""",(data.champion_id, data.tournament_id))

    if not result:
        raise HTTPException(status_code=400, detail="The team cannot be the champion of the competition.")
    
    if not isRegistered(user_id, data.tournament_id):
        raise HTTPException(status_code=400, detail="The user is not in that tournament.")
    
    return tr.update_special_prediction(data, user_id)

def update_match_prediction(tournament_id, match_id, data, user_id):
    db= Database()

    result = db.fetch_one("""SELECT 1 FROM match_ as m INNER JOIN tournament as t ON t.season_id = m.season_id WHERE m.id = %s AND t.id = %s""",(match_id, tournament_id))

    if not result:
        raise HTTPException(status_code=400, detail="The match is not part of the tournament.")
    
    if data.home_goals < 0 or data.away_goals < 0:
        raise HTTPException(status_code=400, detail="Goals cannot be negative.")

    return tr.upsert_match_prediction(tournament_id, match_id, data, user_id)

def get_teams(tournament_id):
    rows = tr.fetch_teams(tournament_id)

    teams = []
    for r in rows:
        teams.append({
            "id": r[0],
            "name": r[1]
        })

    return teams

def get_champion_id_prediction(tournament_id, user_id):
    return {
        "champion_id": tr.get_champion_id_prediction(tournament_id, user_id)
    }

def isRegistered(user_id, tournament_id):
    db = Database()

    result = db.fetch_one("""SELECT 1 FROM registration WHERE user_id = %s AND tournament_id = %s""",(user_id, tournament_id))

    return result != None