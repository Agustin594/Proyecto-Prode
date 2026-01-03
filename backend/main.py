from fastapi import FastAPI, Depends
from schemas import TournamentCreate, TournamentRegister
import tournament_services as ts
from fastapi.middleware.cors import CORSMiddleware
from auth import router
from dependencies import get_current_user_id

app = FastAPI()

app.include_router(router, prefix="/auth")

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
def crear_torneo(data: TournamentCreate, user_id:int = Depends(get_current_user_id)):
    tournament_id = ts.create_tournament(user_id, data)
    return {"tournament_id": tournament_id}

@app.get("/tournament")
def get_tournaments():
    return ts.get_tournaments()

@app.post("/tournament/register")
def inscription(data: TournamentRegister, user_id:int = Depends(get_current_user_id)):
    tournament_id = ts.tournament_inscription(user_id, data)
    return {"tournament_id": tournament_id}

@app.get("/tournament/my")
def get_tournaments_by_id(user_id:int = Depends(get_current_user_id)):
    return ts.get_tournaments_by_id(user_id)