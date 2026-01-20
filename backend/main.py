from fastapi import FastAPI, Depends, Query
from schemas import TournamentCreate, TournamentRegister, SpecialPrediction, MatchPrediction, TournamentDelete
import tournament_services as ts
import match_services as ms
from fastapi.middleware.cors import CORSMiddleware
from auth import router
from dependencies import get_current_user_id
from datetime import date

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
def crear_tournament(data: TournamentCreate, user_id:int = Depends(get_current_user_id)):
    tournament_id = ts.create_tournament(user_id, data)
    return {"tournament_id": tournament_id}

@app.get("/tournament")
def get_tournaments(user_id:int = Depends(get_current_user_id)):
    return ts.get_tournaments(user_id)

@app.get("/tournament/my")
def get_tournaments_by_user_id(user_id:int = Depends(get_current_user_id)):
    return ts.get_tournaments_by_user_id(user_id)

@app.get("/tournament/competitions")
def get_competitions():
    return ts.get_competitions()

@app.get("/tournament/{tournament_id}")
def get_tournament_by_id(tournament_id: int):
    return ts.get_tournament_by_id(tournament_id)

@app.get("/tournament/{tournament_id}/standings")
def get_tournament_standings(tournament_id: int):
    return ts.get_tournament_standings(tournament_id)

@app.get("/tournament/{tournament_id}/matches")
def get_tournament_matches(tournament_id: int, user_id:int = Depends(get_current_user_id)):
    return ts.get_tournament_matches(tournament_id, user_id)

@app.get("/tournament/{tournament_id}/scorers")
def get_tournament_scorers(tournament_id: int):
    return ts.get_tournament_scorers(tournament_id)

@app.get("/tournament/{tournament_id}/inscription")
def get_inscription(tournament_id: int, user_id:int = Depends(get_current_user_id)):
    return ts.get_inscription(tournament_id, user_id)

@app.get("/tournament/{tournament_id}/teams")
def get_teams(tournament_id: int):
    return ts.get_teams(tournament_id)

@app.get("/tournament/{tournament_id}/prediction")
def get_special_prediction(tournament_id: int, user_id:int = Depends(get_current_user_id)):
    return ts.get_champion_id_prediction(tournament_id, user_id)

@app.put("/tournament/{tournament_id}/prediction")
def upadate_special_prediction(data: SpecialPrediction, user_id:int = Depends(get_current_user_id)):
    return ts.update_special_prediction(data, user_id)

@app.put("/tournament/{tournament_id}/match/{match_id}/prediction")
def upadate_match_prediction(tournament_id: int, match_id: int, data: MatchPrediction, user_id:int = Depends(get_current_user_id)):
    return ts.update_match_prediction(tournament_id, match_id, data, user_id)

@app.post("/tournament/register")
def inscription(data: TournamentRegister, user_id:int = Depends(get_current_user_id)):
    tournament_id = ts.tournament_inscription(user_id, data)
    return {"tournament_id": tournament_id}

@app.delete("/tournament/register")
def delete(data: TournamentDelete, user_id:int = Depends(get_current_user_id)):
    tournament_id = ts.delete_tournament_user(user_id, data)
    return {"tournament_id": tournament_id} 

@app.get("/matches")
def get_all_matches(date: date = Query(...)):
    return ms.get_all_matches(date)

@app.get("/matches/personal")
def get_personal_matches(date: date = Query(...), user_id:int = Depends(get_current_user_id)):
    return ms.get_personal_matches(date, user_id)