
"""FastAPI backend for the ORVGROUP AI Agent Web App."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from agent.core import run_agent

app = FastAPI(
    title="ORVGROUP AI Agent",
    description="Backend API for the ORVGROUP Autonomous AI Agent.",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)


@app.get("/")
def home():
    return {
        "name": "ORVGROUP AI Agent",
        "status": "online",
        "message": "Welcome to the ORVGROUP AI Agent API.",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/api/chat")
def chat(request: ChatRequest):
    prompt = request.prompt.strip()

    if not prompt:
        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty.",
        )

    try:
        result = run_agent(prompt)
        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail="Agent service is not configured or unavailable.",
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="The agent encountered an internal error.",
        ) from exc
