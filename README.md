# Commitment Radar

**A voice-powered accountability assistant that remembers commitments, detects evidence-backed deadline conflicts, and drafts follow-up messages.**

> Status: starter scaffold. The UI, API structure, docs, and tests are included. Omi and Lyzr integrations must be configured with valid account credentials and verified against their current official API documentation before being described as fully operational.

## Product goal

Commitment Radar helps people keep track of things they said they would do. It receives transcript text, extracts candidate commitments, stores searchable memory in Qdrant, compares new statements with earlier commitments, and proposes a follow-up message when there is a plausible conflict.

## Core workflow

1. Receive transcript text (from Omi integration or the clearly labelled manual demo endpoint).
2. Extract candidate commitment(s) and normalize the task, owner, deadline, and original evidence.
3. Store the commitment and searchable text in Qdrant.
4. Retrieve semantically related previous commitments.
5. Use the configured Lyzr agent workflow to review potential conflicts.
6. Return a structured decision with evidence and a suggested message.
7. Display commitments, risks, and agent run details in the dashboard.

## Tech stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React + Vite | Responsive dashboard |
| UI | Plain CSS design tokens + Lucide React | Accessible, consistent interface |
| Backend | Python + FastAPI | REST API, validation, integrations |
| Validation | Pydantic | Validate API payloads and model outputs |
| Vector memory | Qdrant Cloud | Persistent semantic retrieval |
| Agent orchestration | Lyzr | Real agent execution/orchestration |
| Voice source | Omi | Supported transcript/voice integration |
| Tests | pytest + FastAPI TestClient | API and workflow checks |
| Version control | Git + GitHub | Public source repository |
| Hosting target | Render (API) + Vercel or Render Static Site (frontend) | Public demo |

## Repository layout

```text
commitment-radar/
├── backend/
│   ├── app/
│   │   ├── integrations/       # Omi and Lyzr adapters
│   │   ├── services/           # commitment/conflict workflow
│   │   ├── config.py
│   │   ├── main.py
│   │   └── models.py
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── docs/
│   ├── ARCHITECTURE.md
│   ├── UI_UX_DESIGN.md
│   ├── TECH_STACK.md
│   ├── INTEGRATION_CHECKLIST.md
│   ├── TEST_PLAN.md
│   ├── DEPLOYMENT.md
│   └── DEMO_SCRIPT.md
├── .gitignore
├── LICENSE
└── README.md
```

## Run locally

### Prerequisites

- Python 3.11+
- Node.js LTS and npm
- Git
- Qdrant Cloud project and API key
- Lyzr account/API access
- Omi app/account and a supported developer integration route

### 1. Backend

Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --port 8000
```

If PowerShell blocks virtual-environment activation, use a Command Prompt terminal and run:

```bat
.venv\Scripts\activate.bat
```

API docs: `http://127.0.0.1:8000/docs`  
Health check: `http://127.0.0.1:8000/health`

### 2. Frontend

Open a second terminal:

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

Vite will print the local URL (usually `http://localhost:5173`).

## Environment variables

Copy the examples and add your own secrets locally. Never commit `.env` files or paste real keys into screenshots, public issues, or frontend variables.

- `QDRANT_URL`, `QDRANT_API_KEY`: Qdrant Cloud
- `LYZR_API_KEY`, `LYZR_AGENT_ID`: Lyzr agent API details (verify exact API fields/endpoint in your account's current docs)
- `OMI_API_KEY`, `OMI_WEBHOOK_SECRET`: placeholders only; use only if required by the selected Omi integration route
- `FRONTEND_ORIGIN`: allowed frontend origin for CORS
- `DEMO_MODE`: controls clearly labelled local sample behavior

## API endpoints in this scaffold

- `GET /health` — service health
- `GET /api/commitments` — list commitments from the current in-memory demo store
- `POST /api/ingest` — manually ingest transcript text for development/testing
- `POST /api/forget` — remove a commitment from the current demo store by ID

**Important:** this starter uses an in-memory store for the initial end-to-end scaffold. It is not durable across restarts. Qdrant persistence and Lyzr execution are integration tasks to complete and test using valid credentials. Do not claim production persistence until the Qdrant adapter is implemented and tested. Do not claim real Omi capture until a real Omi event reaches the backend. Do not claim Lyzr orchestration until the official API call is verified.

## GitHub first push

Before `git add .`, verify `.gitignore` excludes `.env`, `.venv`, `node_modules`, caches, and build outputs.

```powershell
git init
git branch -M main
git add .
git commit -m "Initial Commitment Radar scaffold"
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

## Deployment overview

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md). Deploy backend and frontend separately, configure secrets in the hosting dashboard, set the frontend API URL, and verify the public end-to-end workflow before recording the demo.

## Project docs

- [Architecture](docs/ARCHITECTURE.md)
- [UI/UX design](docs/UI_UX_DESIGN.md)
- [Tech stack](docs/TECH_STACK.md)
- [Integration checklist](docs/INTEGRATION_CHECKLIST.md)
- [Test plan](docs/TEST_PLAN.md)
- [Deployment guide](docs/DEPLOYMENT.md)
- [5-minute demo script](docs/DEMO_SCRIPT.md)

## Safety and product boundaries

- A detected conflict is a suggestion for human review, not proof that someone broke a promise.
- Always show the source snippets supporting an alert.
- Do not send follow-up messages automatically; draft them for user approval.
- Avoid collecting more transcript content than needed.
- Implement authenticated ownership and access control before using real sensitive conversations with multiple users.
- Treat all sample content as fictional demo data.
