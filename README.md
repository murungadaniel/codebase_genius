# codebase_genius🧠 Codebase Genius

AI-powered documentation generator for any public GitHub repository, backed by Jac + FastAPI + Gemini 2.5 Flash + Streamlit.

# Overview

Codebase Genius automatically generates high-level, Markdown documentation for any public GitHub repository.
It blends Jac (for workflow orchestration), FastAPI (for backend logic), Gemini 2.5 Flash (for AI-powered summarization), and Streamlit (for the web UI).

The result is an interactive app that can:

Generate structured documentation (overview, structure, key files, etc.)

Store and view the docs locally

Provide a chat interface for quick Q&A about the generated documentation

# Architecture
 codebase_genius/
│
├── BE/                     # Backend (Jac + FastAPI)
│   ├── main.jac            # Entry module for Jac API server
│   ├── walker_codebase_genius.jac  # Jac walker stub (registered endpoint)
│   ├── supervisor.jac      # Basic node definition
│   ├── api.py              # FastAPI backend (Gemini 2.5 Flash logic)
│   ├── outputs/            # Generated Markdown docs
│   └── .env                # Environment variables
│
├── FE/                     # Frontend (Streamlit)
│   ├── app.py              # Main Streamlit app
│   └── components/
│       ├── chat.py         # Simple chat interface
│       └── docs_viewer.py  # Markdown viewer
│
└── README.md               # Project documentation (this file)


#  Installation & Setup
# 1️ Clone the repo
git clone https://github.com/yourusername/codebase_genius.git
cd codebase_genius

# 2️ Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate     # Linux / macOS
# OR
.venv\Scripts\activate        # Windows

# 3️ Install dependencies
pip install -r requirements.txt


If you don’t have a requirements.txt yet, use:

pip install jaclang byllm fastapi uvicorn[standard] streamlit python-dotenv requests

# 4️ Configure environment variables

Create a file named .env inside the BE/ directory:

GEMINI_API_KEY=your_real_gemini_api_key_here
JAC_SERVER_URL=http://localhost:8000
FASTAPI_PORT=8080
JAC_VERBOSE=false


# Gemini API Key:
Obtain one from Google AI Studio
.

# Running the System

You’ll run three terminals (or processes):

# Terminal 1 – Jac API Server
cd BE
jac serve main.jac --port 8000


Expected output:

Jac API Server running on http://0.0.0.0:8000
Available endpoints:
  POST /walker/codebase_genius

#  Terminal 2 – FastAPI Backend
cd BE
python api.py


Expected output:

INFO:     Uvicorn running on http://0.0.0.0:8080

#  Terminal 3 – Streamlit Frontend
cd FE
streamlit run app.py


Then open http://localhost:8501
 in your browser.

#  How It Works

User inputs a GitHub URL in Streamlit.

Frontend sends the URL to the FastAPI /generate endpoint.

Backend constructs a detailed prompt and calls Gemini 2.5 Flash.

Gemini returns structured Markdown documentation.

The docs are saved under BE/outputs/ and displayed in Streamlit.

Users can read or download the docs, and use a lightweight chat panel for guidance.

# Health Check

Jac server: /health verifies that jac serve main.jac is reachable.

Gemini API key: /health reports if the key is configured (but doesn’t block the app).

Example:

curl http://localhost:8080/health
# → {"status": "ok", "gemini_configured": true}

#  Example Output

# Input:

https://github.com/psf/requests


Generated Output (excerpt):

# Codebase Documentation

## Overview
The `requests` library provides an elegant and Pythonic interface for making HTTP requests.

## Repository Structure
- requests/
  - api.py
  - models.py
  - sessions.py
  - utils.py

## Key Files and Responsibilities
- `sessions.py` handles HTTP session persistence.
- `models.py` defines request and response objects.

## How to Run Locally
Install dependencies and import `requests` into any Python 3.7+ project.

## Possible Improvements
- Add type annotations to internal modules.
- Improve connection-pool diagnostics.

# API Endpoints Summary
Method	Endpoint	   Description
GET	   /health Check    backend + Jac connectivity
POST	/generate	   Generate documentation from a GitHub URL

Sample Request:

curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/psf/requests"}'

# Common Issues & Fixes
Issue	Likely Cause	Fix
Backend response not OK	Missing .env or GEMINI_API_KEY	Run load_dotenv() verified, check .env syntax
Jac server not reachable	Forgot to run jac serve main.jac	Start Jac before FastAPI
Empty docs	Invalid Gemini key or model name	Check your Gemini 2.5 Flash key
Streamlit UI not updating	Cached state	Press R or rerun app

