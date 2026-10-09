# Deployment Guide

Deploy only after local tests pass.

## Backend: Render

1. Push the repository to GitHub.
2. Create a Render Web Service and connect the repository.
3. Set the root directory to `backend`.
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add required environment variables in Render's dashboard (never commit secrets).
7. Deploy and test `/health` and `/docs`.
8. Update `FRONTEND_ORIGIN` to the actual frontend origin.
9. Verify the deployed API's health status and error logs.

## Frontend: Vercel or Render Static Site

1. Connect the same GitHub repository.
2. Set root directory to `frontend`.
3. Build command: `npm install && npm run build`
4. Output directory: `dist`
5. Set `VITE_API_BASE_URL` to the deployed backend base URL.
6. Redeploy after setting environment variables.
7. Test the public frontend and browser console.

## Before recording the demo

- Confirm provider credentials are set on the backend.
- Confirm CORS permits the deployed frontend.
- Test the real Omi → backend → Qdrant → Lyzr → UI workflow.
- Ensure no API secrets appear in frontend bundles or logs.
- Confirm the demo does not rely on hidden local state.
- If a provider is not integrated, label that clearly rather than claiming success.

## Rollback

Keep a known-good commit. If a new deployment breaks the demo, redeploy the last tested commit and re-run the acceptance checklist.
