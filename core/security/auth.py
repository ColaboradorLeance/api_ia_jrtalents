import os
from datetime import datetime, timedelta
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do .env

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY or SECRET_KEY.strip() == "":
    raise RuntimeError(
        "SECRET_KEY não definida! Defina a variável de ambiente SECRET_KEY no Vercel ou localmente."
    )

security = HTTPBearer()

def gerar_token(usuario_id: str, exp_horas: int = 1) -> str:
    payload = {
        "sub": usuario_id,
        "exp": datetime.utcnow() + timedelta(hours=exp_horas)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    print("Token recebido no validate_token:", token)
    if not token:
        raise HTTPException(status_code=401, detail="Token ausente")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        usuario_id = payload.get("sub")
        if not usuario_id:
            raise HTTPException(status_code=401, detail="Token inválido(usuário)")
        return usuario_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido(JWT Problema)")
