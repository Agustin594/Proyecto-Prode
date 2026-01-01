from fastapi import FastAPI
from schemas import TorneoCreate
from tournament_services import create_tournament
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/tournament")
def crear_torneo(data: TorneoCreate):
    tournament_id = create_tournament(data)
    return {"tournament_id": tournament_id}