from typing import List
from huggingface_hub import InferenceClient
from domain.schemas import JobRequest
from dotenv import load_dotenv
import numpy as np
import os

load_dotenv()
hf_token = os.environ.get("HF_TOKEN")

client = InferenceClient(
    provider="sambanova",
    api_key=hf_token,
)

class ExternalMLClient:
    def generate_embedding(self, job_dict: dict) -> List[float]:
        text = self.job_values_to_text(job_dict)
        embedding_vector =  client.feature_extraction(
            text,
            model="intfloat/e5-mistral-7b-instruct",
        )
        if isinstance(embedding_vector, np.ndarray):
            embedding_vector = embedding_vector.tolist()
        return embedding_vector


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
