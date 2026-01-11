from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import security 
from database import Database
import re

router = APIRouter()

class UserCreate(BaseModel):
    name: str
    mail: str
    password: str

@router.post("/register")
def register_user(user: UserCreate):
    db = Database()

    result = db.fetch_one("""SELECT 1 FROM user_ WHERE name = %s""", (user.name,))

    if result:
        raise HTTPException(status_code=400, detail="The user name is already in use.")
    
    result = db.fetch_one("""SELECT 1 FROM user_ WHERE mail = %s""", (user.mail,))

    if result:
        raise HTTPException(status_code=400, detail="The email is already registered.")

    errors = validate_password(user.password)

    if errors:
        return {
            "success": False,
            "errors": errors
        }
    
    ####### VALIDAR MAIL (Mandar código de verificación de 24hs para terminar de registrar la cuenta, dicho email debe existir)

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

def validate_password(password: str):
    errors = []

    if len(password) < 8:
        errors.append("It must have at least 8 characters.")

    if not re.search(r"[A-Z]", password):
        errors.append("It must have an uppercase letter.")

    if not re.search(r"[a-z]", password):
        errors.append("It must have a lowercase letter.")

    if not re.search(r"\d", password):
        errors.append("It must have a number.")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("It must have a special character.")

    return errors