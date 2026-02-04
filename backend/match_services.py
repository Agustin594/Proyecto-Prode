import match_repo as mr
from datetime import datetime, timedelta

IMPORTANT_TEAMS = ["Atlético Madrid", "Liverpool", "Real Madrid", "Barcelona", "River Plate"
                   "Boca Juniors", "Juventus", "Milan", "Inter", "FC Bayern München", "Manchester United"
                   "Manchester City", "Chelsea", "Arsenal", "Tottenham Hotspur", "Paris Saint-Germain"
                   "Flamengo", "Palmeiras", "Argentina", "Brazil", "Germany", "Spain", "Italy",
                   "England", "France", "Uruguay"]

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
            "competition_name": r[8],
            "home_team_image": r[9],
            "away_team_image": r[10],
            "competition_image_name": r[11],
            "overtime_home_goals": r[12],
            "overtime_away_goals": r[13],
            "penalties_home_goals": r[14],
            "penalties_away_goals": r[15]
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
            "competition_name": r[8],
            "home_team_image": r[9],
            "away_team_image": r[10],
            "competition_image_name": r[11],
            "overtime_home_goals": r[12],
            "overtime_away_goals": r[13],
            "penalties_home_goals": r[14],
            "penalties_away_goals": r[15]
        })

    return matches

def get_important_matches():
    rows = mr.fetch_important_matches()

    matches = []
    for r in rows:
        match = ({
            "id": r[0],
            "date": r[1],
            "home_team_name": r[2],
            "away_team_name": r[3],
            "home_goals": r[4],
            "away_goals": r[5],
            "status": r[6],
            "competition_id": r[7],
            "competition_name": r[8],
            "home_team_image": r[9],
            "away_team_image": r[10],
            "competition_image_name": r[11],
            "overtime_home_goals": r[12],
            "overtime_away_goals": r[13],
            "penalties_home_goals": r[14],
            "penalties_away_goals": r[15]
        })

        match["points"] = calculate_match_points(match)
        matches.append(match)

    top_matches = sorted(
        matches,
        key=lambda m: m["points"],
        reverse=True
    )[:5]

    return top_matches

def get_calendar_matches(month, year, user_id):
    rows = mr.fetch_calendar_matches(month, year, user_id)

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
            "competition_name": r[8],
            "home_team_image": r[9],
            "away_team_image": r[10],
            "competition_image_name": r[11]
        })

    return matches

def calculate_match_points(match):
    points = 0

    # ejemplos de criterios
    if match["status"] == "inprogress":
        points += 40
    else:
        now = datetime.now()

        difference = (match["date"].date() - now.date()).days

        if difference == 0:
            points += 30        
        elif difference == 1:
            points += 20        
        elif 2 <= difference <= 3:
            points += 10           

    if match["competition_name"] in ["UEFA Champions League", "Premier League", "FIFA World Cup", "CONMEBOL Libertadores", "LaLiga", "Brasileirão Betano", "EURO", "Copa América"]:
        points += 30

    if match["home_team_name"] in IMPORTANT_TEAMS and match["away_team_name"] in IMPORTANT_TEAMS:
        points += 50
    elif match["home_team_name"] in IMPORTANT_TEAMS or match["away_team_name"] in IMPORTANT_TEAMS:
        points += 15

    return points