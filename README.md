# AI Resume ATS Analyzer

## Objective
An AI-powered resume analysis tool that evaluates a resume against a specific 
job description — producing an ATS compatibility score, keyword gap analysis, 
a tailored professional summary, and AI-rewritten bullet points, with built-in 
safeguards against AI-generated fabrication.

## Live Demo
- Frontend: https://ai-resume-ats-analyze-1.onrender.com
- Backend API docs: https://ai-resume-ats-analyze.onrender.com/docs

## Tech Stack (Phase 1)
**Language & Core:** Python, OOP principles
**NLP:** spaCy (keyword extraction), pdfplumber & python-docx (document parsing)
**AI/LLM:** Google Gemini 3.6 Flash API, prompt engineering with explicit 
anti-fabrication and anti-genericness constraints
**Backend:** FastAPI, Uvicorn
**Frontend:** Streamlit
**Infrastructure:** Docker (multi-container architecture), Docker networking, 
Git/GitHub, Render (CI/CD via auto-deploy on push)

## Architecture
The application is split into two independently containerized services:

- **Backend** (`/backend`) — a FastAPI service exposing a single `/analyze` 
  endpoint. The pipeline runs: document text extraction → text normalization 
  and section detection → JD keyword extraction (spaCy) → exact-match ATS 
  scoring → rule-based resume health checks (contact info, section coverage, 
  length) → AI-powered bullet rewriting and profile summary generation via 
  Gemini, gated by a code-level vagueness filter that runs before any bullet 
  reaches the LLM.
- **Frontend** (`/frontend`) — a Streamlit interface for uploading a resume, 
  pasting a job description, and viewing results.

Both services run in separate Docker containers, communicating over a shared 
Docker network locally, and as independently deployed Render services in 
production. The backend URL is injected via an environment variable 
(`BACKEND_URL`), allowing the same codebase to run unmodified across local 
Python, local Docker, and cloud deployment.

## Notable Engineering Decisions & Challenges
- **Deterministic safety over prompt trust alone:** LLM instructions aren't 
  reliably followed 100% of the time. Rather than relying solely on prompt 
  wording to prevent fabrication, a code-level vagueness detector filters out 
  bullets too thin to honestly rewrite *before* they reach Gemini — a 
  deterministic check as a second layer of defense, not just a prompt request.
- **Environment-portable design:** the same application code runs correctly 
  across three environments (plain local Python, local Docker containers, 
  and Render cloud deployment) purely through environment variable 
  configuration — no code branching required.
- **Graceful degradation against third-party failures:** the Gemini API call 
  is wrapped in explicit error handling, so a transient upstream outage 
  (encountered live during development — a real `503` from Gemini) returns a 
  clear fallback message instead of crashing the entire endpoint.
- **Debugging a full deployment pipeline solo:** resolved real issues across 
  the stack — Docker container networking and DNS resolution, dynamic port 
  binding (`$PORT`) on cloud platforms, environment variable misconfiguration, 
  and exact-match vs. substring-match logic bugs in section detection.

## Known Limitations (Phase 1)
- Keyword matching is currently exact-substring based (e.g., "ML" will not 
  match "machine learning") — semantic matching via sentence embeddings is 
  planned for Phase 2.
- Vagueness detection uses a heuristic (word count + known filler phrases), 
  which may not catch every edge case.
- Deployed on Render's free tier — services spin down after inactivity, 
  causing a cold-start delay (~30–60s) on the first request after idle time.

## Planned (Phase 2+)
- Semantic keyword matching using sentence embeddings and cosine similarity, 
  replacing/augmenting exact-substring matching.
- (Stretch) A lightweight agentic layer for multi-step resume improvement.

## Running Locally

# Prerequisites

Ensure you have the following installed:
* **Git**
* **Python 3.x**

### 1. Clone the Repository

Open your terminal and run the following command to clone the project:

```bash
git clone <https://github.com/baghelrashmi04/ai-resume-ats-analyzer>
cd <ai-resume-ats-analyzer>
```

### 2. Configure Environment Variables

The backend requires a Gemini API key to function. 

1. Navigate to the `backend/` directory.
2. Create a new file named `.env`.
3. Add your API key to the file:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Setup and Run the Backend

Open a **new terminal window** and run the following commands to install dependencies and start the backend server:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
python main.py             # Replace with your actual backend entry file (e.g., app.py)
```

### 4. Setup and Run the Frontend

Open a **second terminal window** to run the frontend service concurrently:

```bash
cd frontend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
python main.py             # Replace with your actual frontend entry file
```
