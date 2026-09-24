from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.models import ChatRequest
from app.pipeline import process

load_dotenv()

app = FastAPI(title="Darukaa Earth Biodiversity Intelligence")

# Allow the React frontend to communicate with the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest):
    metrics = (
        req.metrics
        or __import__(
            "app.models",
            fromlist=["EnvironmentalMetrics"]
        ).EnvironmentalMetrics()
    )

    return process(req.session_id, metrics, req.message)