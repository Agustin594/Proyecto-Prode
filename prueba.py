from database import Database
from sync_match import sync_matches

def main():
    db = Database()

    sync_matches(db, 7)

main()