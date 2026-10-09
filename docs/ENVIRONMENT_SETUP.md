# Environment Setup

## Backend

Create `backend/.env` from `.env.example` and add secrets locally.

```dotenv
APP_NAME=Commitment Radar API
ENVIRONMENT=development
DEMO_MODE=true
FRONTEND_ORIGIN=http://localhost:5173
QDRANT_URL=
QDRANT_API_KEY=
QDRANT_COLLECTION=commitments
LYZR_API_KEY=
LYZR_AGENT_ID=
OMI_API_KEY=
OMI_WEBHOOK_SECRET=
```

Some Omi fields may not be needed depending on the supported integration route. Do not add invented credentials or guess the vendor's auth scheme.

## Frontend

Create `frontend/.env` from `.env.example`:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Frontend environment variables are public to browser users. Never put Qdrant or Lyzr secrets in frontend variables.
