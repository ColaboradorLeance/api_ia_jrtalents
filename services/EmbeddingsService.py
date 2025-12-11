from typing import List, Dict, Any
from domain.schemas import JobRequest

from sentence_transformers import SentenceTransformer, util

class ExternalMLClient:
    def __init__(self):
        self.model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')

    def generate_embedding(self, data: Dict[str, Any]) -> List[float]:
        job_text = self.job_values_to_text(data)
        return self.model.encode(job_text).toList()


    def job_values_to_text(job_dict: dict) -> str:
        partes = []

        for value in job_dict.values():
            if value is None:
                continue
            if isinstance(value, list):
                partes.append(", ".join(map(str, value)))
            else:
                partes.append(str(value))
        return "\n".join(partes)


#
class EmbeddingsService:
    def __init__(self, ml_client: ExternalMLClient):
        self.ml_client = ml_client

    def process_vaga(self, job: JobRequest) -> dict:
        job_desc = job.dict(include={"descricao", "requisitos"})
        embedding_vector_desc = self.ml_client.generate_embedding(job_desc)

        job_habilidade = job.dict(include={"habilidadesRequeridas"})
        embedding_vector_habilidade = self.ml_client.generate_embedding(job_habilidade)

        job_areas = job.dict(include={"areas", "areasEspecificas", "areasEspecificasOutros"})
        embedding_area = self.ml_client.generate_embedding(job_areas)


        return {
            "status": "Processado e Embedding Gerado",
            "jobId": job.jobId,
            "embedding_descricao": embedding_vector_desc,
            "embedding_habilidade": embedding_vector_habilidade,
            "embedding_area": embedding_area,
        }