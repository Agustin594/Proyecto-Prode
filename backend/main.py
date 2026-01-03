from fastapi import FastAPI
from schemas import TorneoCreate
import tournament_services as ts
from fastapi.middleware.cors import CORSMiddleware
from auth import router

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
def crear_torneo(data: TorneoCreate):
    tournament_id = ts.create_tournament(data)
    return {"tournament_id": tournament_id}

@app.get("/tournament")
def get_tournaments():
    return ts.get_tournaments()