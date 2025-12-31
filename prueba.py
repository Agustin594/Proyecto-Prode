from database import Database
from sync_match import sync_matches
from sync_competition import sync_competitions

def main():
    db = Database()

    sync_matches(db, 7)

main()