from typing import List
from domain.schemas import JobRequest

class ExternalMLClient:
    def call_model_api(self, data: JobRequest) -> List[float]:
        print(f"DEBUG: Chamando API de Machine Learning para {data.jobId}.")
        return [0.123, -0.456, 0.789]


class EmbeddingsService:
    def __init__(self, ml_client: ExternalMLClient):
        self.ml_client = ml_client

    def processar_vaga_e_gerar_embedding(self, job: JobRequest, usuario_id: str) -> dict:
        embedding_vector = self.ml_client.call_model_api(job)
        print(f"INFO: Vetor de dimensão {len(embedding_vector)} gerado para o usuário {usuario_id}.")

        return {
            "status": "Processado e Embedding Gerado",
            "jobId": job.jobId,
            "usuario_id": usuario_id,
            "embedding_dimensao": len(embedding_vector)
        }