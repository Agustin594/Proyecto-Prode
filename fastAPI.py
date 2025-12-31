from fastapi import FastAPI
from schemas import TorneoCreate
from tournament_services import create_tournament

app = FastAPI()

@app.post("/tournament")
def crear_torneo(data: TorneoCreate):
    tournament_id = create_tournament(data)
    return {"tournament_id": tournament_id}