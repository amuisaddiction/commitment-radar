from fastapi import HTTPException, Request
from .config import settings

def extract_transcript(payload: dict):
    candidates = [payload.get("transcript"), payload.get("text"), payload.get("summary")]
    if isinstance(payload.get("data"), dict):
        candidates.append(payload["data"].get("transcript"))
    if isinstance(payload.get("conversation"), dict):
        candidates.append(payload["conversation"].get("transcript"))
    for value in candidates:
        if isinstance(value, str) and value.strip():
            return value.strip()
    raise HTTPException(status_code=422, detail="Transcript field not found. Adapt app/omi.py to the actual Omi payload.")

async def verify_webhook(request: Request):
    if settings.omi_webhook_secret and request.headers.get("x-omi-webhook-secret", "") != settings.omi_webhook_secret:
        raise HTTPException(status_code=401, detail="Invalid Omi webhook secret")
