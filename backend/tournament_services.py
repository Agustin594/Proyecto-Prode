import tournament_repo as tr

def create_tournament(data):

    ###### VALIDAR CREACIÓN

    return tr.insert(data.competition_id, data.open, data.participant_limit, data.entry_price, data.public)

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