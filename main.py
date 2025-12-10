import os

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI(
    title="JR Talents API",
    version="1.0",
)

security = HTTPBearer()

class JobRequest(BaseModel):
    jobId: str
    titulo: str
    descricao: str
    requisitos: str
    tipoContrato: str
    modalidade: str
    areas: List[str]
    areasEspecificas: List[str]
    areasEspecificasOutros: Optional[str] = None
    habilidadesRequeridas: List[str]

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

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/embeddings/job")
def receber_vaga(job: JobRequest, usuario_id: str = Depends(validateToken)):
    return {
        "mensagem": f"Vaga recebida com sucesso pelo usuário {usuario_id}",
        "job": job
    }
