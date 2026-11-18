
"""FastAPI backend for the ORVGROUP AI Agent Web App."""

import os
import secrets
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware.sessions import SessionMiddleware

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

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv(
        "SESSION_SECRET",
        "development-only-change-this-secret",
    ),
    same_site="lax",
    https_only=os.getenv("COOKIE_SECURE", "false").lower() == "true",
)

FRONTEND_FILE = Path(__file__).parent / "static" / "index.html"


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=200)


@app.get("/")
def home():
    return FileResponse(FRONTEND_FILE)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/api/login")
@limiter.limit("5/minute")
def login(request: Request, credentials: LoginRequest):
    expected_username = os.getenv("APP_USERNAME")
    expected_password = os.getenv("APP_PASSWORD")

    if not expected_username or not expected_password:
        raise HTTPException(
            status_code=503,
            detail="Login is not configured.",
        )

    username_ok = secrets.compare_digest(
        credentials.username,
        expected_username,
    )
    password_ok = secrets.compare_digest(
        credentials.password,
        expected_password,
    )

    if not (username_ok and password_ok):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password.",
        )

    request.session.clear()
    request.session["authenticated"] = True

    return {"message": "Login successful."}


@app.post("/api/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out."}


@app.post("/api/chat")
@limiter.limit("10/minute")
def chat(request: Request, chat_request: ChatRequest):
    if not request.session.get("authenticated"):
        raise HTTPException(
            status_code=401,
            detail="Please log in to use the agent.",
        )

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
