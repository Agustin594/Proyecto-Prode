import tournament_repo as tr
import security
from database import Database
from fastapi import HTTPException

def create_tournament(user_id, data):
    db = Database()

    result = db.fetch_one("""SELECT 1 FROM competition WHERE id = %s""", (data.competition_id,))

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
            "name": r[1],
            "image_name": r[2]
        })

    return competitions

def get_tournaments(user_id):
    rows = tr.fetch_all(user_id)

    tournaments = []
    for r in rows:
        tournaments.append({
            "id": r[0],
            "name": r[1],
            "competition_id": r[2],
            "open": r[3],
            "registered_participants": r[4],
            "participant_limit": r[5],
            "entry_price": r[6],
            "public": r[7],
            "password": r[8],
            "image_name": r[9]
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
            "competition_id": r[2],
            "open": r[3],
            "registered_participants": r[4],
            "participant_limit": r[5],
            "entry_price": r[6],
            "public": r[7],
            "password": r[8],
            "image_name": r[9]
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
        "competition_id": t[2],
        "open": t[3],
        "registered_participants": t[4],
        "participant_limit": t[5],
        "entry_price": t[6],
        "public": t[7],
        "password": t[8],
        "image_name": t[9]
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
            "home_team_image": r[7],
            "away_team_image": r[8],
            "prediction": {
                "home_goals": r[9],
                "away_goals": r[10]
            } if r[9] is not None else None,
            "referenced": {
                "home_goals": r[11],
                "away_goals": r[12],
                "status": r[13]
            } if r[11] is not None else None,
            "match_type": r[14],
            "overtime_home_goals": r[15],
            "overtime_away_goals": r[16],
            "penalties_home_goals": r[17],
            "penalties_away_goals": r[18],
            "home_team_id": r[19],
            "away_team_id": r[20],
            "round": r[21],
            "round_name": r[22],
            "order_index": r[23]
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

    result = db.fetch_one("""SELECT 1 FROM team as te INNER JOIN team_participations as tp ON tp.team_id = te.id INNER JOIN tournament as t ON t.season_id = tp.season_id WHERE te.id = %s AND t.id = %s""",(data.champion_id, data.tournament_id))

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
    
    # Qualified team verification

    if data.qualified_team_id != None:
        result = db.fetch_one("""SELECT 
                                    match_type,
                                    home_team_id,
                                    away_team_id,
                                    referenced_match 
                                FROM match_ as m 
                                WHERE m.id = %s""",(match_id,))
        
        if result[0] == 'single':
            if data.home_goals > data.away_goals and data.qualified_team_id != result[1]:
                raise HTTPException(status_code=400, detail="Incorrect qualified team.")
            elif data.away_goals > data.home_goals and data.qualified_team_id != result[2]:
                raise HTTPException(status_code=400, detail="Incorrect qualified team.")
            elif data.qualified_team_id != result[1] and data.qualified_team_id != result[2]:
                raise HTTPException(status_code=400, detail="Incorrect qualified team.")
        elif result[0] == 'secondleg':
            firstleg_prediction = db.fetch_one("""SELECT 
                                    home_goals,
                                    away_goals
                                FROM match_prediction 
                                WHERE match_id = %s AND tournament_id = %s AND user_id = %s""",(result[3], tournament_id, user_id))
            
            if firstleg_prediction[0] == None or firstleg_prediction[1] == None:
                if data.home_goals > data.away_goals and data.qualified_team_id != result[1]:
                    raise HTTPException(status_code=400, detail="Incorrect qualified team.")
                elif data.away_goals > data.home_goals and data.qualified_team_id != result[2]:
                    raise HTTPException(status_code=400, detail="Incorrect qualified team.")
                elif data.qualified_team_id != result[1] and data.qualified_team_id != result[2]:
                    raise HTTPException(status_code=400, detail="Incorrect qualified team.")
            else:
                total_home_goals = data.home_goals + firstleg_prediction[1]
                total_away_goals = data.away_goals + firstleg_prediction[0]

                if total_home_goals > total_away_goals and data.qualified_team_id != result[1]:
                    raise HTTPException(status_code=400, detail="Incorrect qualified team.")
                elif total_away_goals > total_home_goals and data.qualified_team_id != result[2]:
                    raise HTTPException(status_code=400, detail="Incorrect qualified team.")
                elif data.qualified_team_id != result[1] and data.qualified_team_id != result[2]:
                    raise HTTPException(status_code=400, detail="Incorrect qualified team.")

    return tr.upsert_match_prediction(tournament_id, match_id, data, user_id)

def get_teams(tournament_id):
    rows = tr.fetch_teams(tournament_id)

    teams = []
    for r in rows:
        teams.append({
            "id": r[0],
            "name": r[1],
            "image_name": r[2]
        })

    return teams

def get_champion_id_prediction(tournament_id, user_id):
    result = tr.get_champion_id_prediction(tournament_id, user_id)
    if result == None:
        return {
            "champion_id": None
        }
    else:
        return {
            "champion_id": result[0]
        }

def isRegistered(user_id, tournament_id):
    db = Database()

    result = db.fetch_one("""SELECT 1 FROM registration WHERE user_id = %s AND tournament_id = %s""",(user_id, tournament_id))

    return result != None