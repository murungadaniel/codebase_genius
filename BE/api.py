import os
from pathlib import Path

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = (BASE_DIR.parent / "outputs").resolve()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Gemini 2.5 Flash
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)

# Jac server (for basic connectivity check)
JAC_SERVER_URL = os.getenv("JAC_SERVER_URL", "http://localhost:8000")

app = FastAPI(title="Codebase Genius Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    repo_url: str


@app.get("/health")
def health():
    """
    Health check used by the Streamlit frontend.
    - Must return 200 if backend is up and Jac server is reachable.
    - Also reports if Gemini is configured, but does NOT fail on missing key
      (so you don't get blocked by health if you're just testing wiring).
    """
    # Check Jac server
    try:
        r = requests.get(f"{JAC_SERVER_URL}/", timeout=1)
        if r.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail="Jac server reachable but not OK",
            )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Jac server not reachable",
        )

    return {
        "status": "ok",
        "gemini_configured": bool(GEMINI_API_KEY),
    }


def call_gemini_for_docs(repo_url: str) -> str:
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail=(
                "GEMINI_API_KEY not configured on backend. "
                "Set it in your .env file or environment."
            ),
        )

    prompt = f"""
You are Codebase Genius. You are given this public GitHub repository URL:

{repo_url}

Generate high-level, factual Markdown documentation with the following structure:

# Codebase Documentation
## Overview
## Repository Structure
## Key Files and Responsibilities
## How to Run Locally (only if it can be inferred from the repo)
## Possible Improvements

Rules:
- Base your answer only on what would reasonably be visible in the repository (no hallucinated technologies).
- If something is unclear or missing, say so explicitly instead of guessing.
- Keep it concise, clear, and suitable for Generative AI students at the Open University of Kenya.
"""

    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        resp = requests.post(
            GEMINI_API_URL,
            headers=headers,
            params=params,
            json=body,
            timeout=120,
        )
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calling Gemini API: {e}",
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    data = resp.json()
    try:
        candidates = data["candidates"]
        parts = candidates[0]["content"]["parts"]
        text = "".join(part.get("text", "") for part in parts)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unexpected response format from Gemini API.",
        )

    if not text.strip():
        raise HTTPException(
            status_code=500,
            detail="Empty response from Gemini 2.5 Flash.",
        )

    return text


@app.post("/generate")
def generate(req: GenerateRequest):
    repo_url = req.repo_url.strip()
    if not repo_url.startswith("https://github.com/"):
        raise HTTPException(status_code=400, detail="Invalid GitHub URL.")

    docs_markdown = call_gemini_for_docs(repo_url)

    repo_name = (
        repo_url.rstrip("/").split("/")[-1].replace(".git", "") or "codebase"
    )
    out_file = OUTPUT_DIR / f"{repo_name}_docs.md"
    out_file.write_text(docs_markdown, encoding="utf-8")

    return {
        "docs_path": str(out_file.resolve()),
        "repo_url": repo_url,
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("FASTAPI_PORT", "8080"))
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=True)
