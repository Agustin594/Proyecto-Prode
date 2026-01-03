from pydantic import BaseModel

class TournamentCreate(BaseModel):
    competition_id: int
    participant_limit: int
    entry_price: int
    public: bool

class TournamentRegister(BaseModel):
    tournament_id: int