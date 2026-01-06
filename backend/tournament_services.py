import tournament_repo as tr

def create_tournament(user_id, data):

    ###### VALIDAR CREACIÓN

    return tr.insert(user_id, data.competition_id, data.participant_limit, data.entry_price, data.public)

def get_tournaments():
    rows = tr.fetch_all()

    tournaments = []
    for r in rows:
        tournaments.append({
            "id": r[0],
            "name": r[1],
            "open": r[2],
            "registered_participants": r[3],
            "participant_limit": r[4],
            "entry_price": r[5],
            "public": r[6]
        })

    return tournaments

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
            "public": r[6]
        })

    return tournaments

def tournament_inscription(user_id, data):
    ##### VALIDAR
    tr.inscription(user_id, data.tournament_id)

def delete_tournament_user(user_id, data):
    #### VALIDAR
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
        "public": t[6]
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

def get_tournament_matches(tournament_id):
    rows = tr.fetch_matches(tournament_id)

    matches = []
    for r in rows:
        matches.append({
            "id": r[0],
            "date": r[1],
            "home_team_name": r[2],
            "away_team_name": r[3],
            "home_goals": r[4],
            "away_goals": r[5]
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