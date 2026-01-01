from database import Database
from sync_match import sync_matches
from sync_competition import sync_competitions
from sync_team import sync_teams

def main():
    db = Database()

    sync_matches(db, 17)

main()