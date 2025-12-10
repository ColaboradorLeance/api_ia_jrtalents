import jwt
from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv("SECRET_KEY")

def gerar_token(usuario_id: str, exp_horas: int = 1):
    payload = {
        "sub": usuario_id,
        "exp": datetime.utcnow() + timedelta(hours=exp_horas)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token
