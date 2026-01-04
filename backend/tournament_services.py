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

def get_tournaments_by_id(user_id):
    rows = tr.fetch_by_id(user_id)

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