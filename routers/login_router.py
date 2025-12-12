from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.security.auth import gerar_token

router = APIRouter(
    tags=["Login"],
)

class LoginRequest(BaseModel):
    usuario: str
    senha: str

@router.post("/login")
def login(data: LoginRequest):
    if data.usuario != "borajunior" or data.senha != "1234":
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = gerar_token(data.usuario)
    return {"access_token": token, "token_type": "bearer"}
