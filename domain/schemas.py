from pydantic import BaseModel
from typing import List, Optional

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