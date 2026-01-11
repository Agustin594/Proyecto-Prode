from pydantic import BaseModel

class TournamentCreate(BaseModel):
    competition_id: int
    participant_limit: int
    entry_price: int
    public: bool
    password: str

class TournamentRegister(BaseModel):
    tournament_id: int
    password: str

class TournamentDelete(BaseModel):
    tournament_id: int

class SpecialPrediction(BaseModel):
    tournament_id: int
    champion_id: int

class MatchPrediction(BaseModel):
    home_goals: int
    away_goals: int