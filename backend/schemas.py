from pydantic import BaseModel

class TorneoCreate(BaseModel):
    competition_id: int
    open: bool
    participant_limit: int
    entry_price: int
    public: bool