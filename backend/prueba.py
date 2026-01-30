from database import Database
from sync_match import sync_matches
from sync_competition import sync_competitions
from sync_team import sync_teams
from sync_season import sync_season

def main():
    db= Database()

    competitions = [1, 7, 8, 16, 17, 23, 34, 35, 133, 155, 325, 384]

    current_competitions = [7, 8, 17, 23, 34, 35, 155, 325, 384]

    for competition in competitions:
        sync_matches(db, competition)

def main2():
    db= Database()

    sync_matches(db, 17) 

main()