from database import Database
from sync_match import sync_matches
from sync_competition import sync_competitions
from sync_team import sync_teams
from passlib.context import CryptContext

def main():
    pwd_context = CryptContext(schemes=["bcrypt"])

    hash = pwd_context.hash("123456")
    print(hash)

    print(pwd_context.verify("123456", hash))

main()