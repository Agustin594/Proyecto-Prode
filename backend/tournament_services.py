from tournament_repo import insert

def create_tournament(data):

    ###### VALIDAR CREACIÓN

    return insert(data.competition_id, data.open, data.participant_limit, data.entry_price, data.public)