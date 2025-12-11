from fastapi import FastAPI
from dotenv import load_dotenv
from routers.embeddings_router import router as embeddings_router

load_dotenv()

app = FastAPI(
    title="JR Talents API",
    version="1.0",
    description="API para serviços de talentos e geração de embeddings de vagas.",
)

@app.get("/")
def home():
    return {"status": "ok", "app": app.title, "version": app.version}

# Inclui rotas
app.include_router(embeddings_router)
