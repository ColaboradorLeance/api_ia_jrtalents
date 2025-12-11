from fastapi import APIRouter, Depends, status
from typing import Generator
from domain.schemas import JobRequest
from core.security.auth import validateToken
from services.EmbeddingsService import EmbeddingsService, ExternalMLClient

def get_ml_client() -> Generator[ExternalMLClient, None, None]:
    ml_client = ExternalMLClient()
    try:
        yield ml_client
    finally:
        pass


def get_embeddings_service(
    ml_client: ExternalMLClient = Depends(get_ml_client)) -> EmbeddingsService:
    service = EmbeddingsService(ml_client=ml_client)
    return service

router = APIRouter(
    prefix="/embeddings",
    tags=["Embeddings"],
)

@router.post(
    "/job",
    status_code=status.HTTP_202_ACCEPTED,
)
def receber_vaga(
        job_in: JobRequest,
        usuario_id: str = Depends(validateToken),
        service: EmbeddingsService = Depends(get_embeddings_service),
):

    resultado = service.process_vaga(job=job_in)

    return {
        "mensagem": f"Processamento da vaga {resultado['jobId']} iniciado com sucesso.",
         "embedding_descricao": resultado["embedding_descricao"],
         "embedding_habilidade": resultado["embedding_habilidade"],
          "embedding_area": resultado["embedding_area"]
    }