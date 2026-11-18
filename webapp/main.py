
"""FastAPI backend for the ORVGROUP AI Agent Web App."""

from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from agent.core import run_agent

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="ORVGROUP AI Agent",
    description="Backend API for the ORVGROUP Autonomous AI Agent.",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)

FRONTEND_FILE = Path(__file__).parent / "static" / "index.html"


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)


@app.get("/")
def home():
    return FileResponse(FRONTEND_FILE)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/api/chat")
@limiter.limit("10/minute")
def chat(request: Request, chat_request: ChatRequest):
    prompt = chat_request.prompt.strip()

    if not prompt:
        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty.",
        )

    try:
        return run_agent(prompt)

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
