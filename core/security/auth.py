import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv("SECRET_KEY")
security = HTTPBearer()

def gerar_token(usuario_id: str, exp_horas: int = 1):
    payload = {
        "sub": usuario_id,
        "exp": datetime.utcnow() + timedelta(hours=exp_horas)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def validateToken(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        usuario_id = payload.get("sub")
        if not usuario_id:
            raise HTTPException(status_code=401, detail="Token inválido")
        return usuario_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")