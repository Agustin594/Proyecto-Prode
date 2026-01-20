import match_repo as mr 

def get_all_matches(date):
    rows = mr.fetch_all_matches(date)

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
            "competition_id": r[7],
            "competition_name": r[8]
        })

    return matches

def get_personal_matches(date, user_id):
    rows = mr.fetch_personal_matches(date, user_id)

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
            "competition_id": r[7],
            "competition_name": r[8]
        })

    return matches