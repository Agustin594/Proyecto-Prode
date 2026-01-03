from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import security 
from database import Database

router = APIRouter()

class UserCreate(BaseModel):
    name: str
    mail: str
    password: str

@router.post("/register")
def register_user(user: UserCreate):
    db = Database()

    password_hash = security.hash_password(user.password)

    user_id = db.fetch_one(
        "INSERT INTO user_ (name, mail, password) VALUES (%s, %s, %s) RETURNING id",
        (user.name, user.mail, password_hash)
    )[0]

    token = security.create_access_token(user_id)

    return {"access_token": token, "token_type": "bearer"}

class UserLogin(BaseModel):
    mail: str
    password: str

@router.post("/login")
def login(user: UserLogin):
    db = Database()

    result = db.fetch_one(
        "SELECT id, password FROM user_ WHERE mail = %s",
        (user.mail,)
    )

    if not result:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    if not security.verify_password(user.password, result[1]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token = security.create_access_token(result[0])

    return {"access_token": token, "token_type": "bearer"}