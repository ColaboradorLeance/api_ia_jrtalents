from typing import List, Dict, Any
from domain.schemas import JobRequest
import os
import requests

HUGGINGFACE_API_URL = "https://router.huggingface.co/hf-inference/pipeline/feature-extraction/sentence-transformers/paraphrase-MiniLM-L6-v2"
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")

class ExternalMLClient:
    def generate_embedding(self, job_dict: dict) -> List[float]:
        text = self.job_values_to_text(job_dict)
        
        headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
        
        response = requests.post(
            HUGGINGFACE_API_URL,
            headers=headers,
            json={"inputs": text, "options": {"wait_for_model": True}}
        )
        
        if response.status_code != 200:
            raise Exception(f"Hugging Face API error: {response.text}")
        
        return response.json()

    @staticmethod
    def job_values_to_text(job_dict: dict) -> str:
        partes = []
        for value in job_dict.values():
            if not value:
                continue
            if isinstance(value, list):
                partes.append(", ".join(value))
            else:
                partes.append(str(value))
        return "\n".join(partes)


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
