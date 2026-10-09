from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from datetime import datetime, timezone
import uuid
from .config import settings
from .models import IngestRequest
from .commitments import extract_commitments, detect_conflicts
from .memory import MemoryStore
from .lyzr_client import LyzrClient
from .omi import extract_transcript, verify_webhook

app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
memory, lyzr = MemoryStore(), LyzrClient()
commitments, conflicts, logs = [], [], []
frontend = Path(__file__).resolve().parent.parent / "frontend"

def log(step, status, message, details=None):
    logs.insert(0, {"id": str(uuid.uuid4()), "step": step, "status": status,
        "message": message, "details": details or {}, "created_at": datetime.now(timezone.utc).isoformat()})
    del logs[100:]

@app.get("/", response_class=HTMLResponse)
def home():
    return (frontend / "index.html").read_text(encoding="utf-8")

@app.get("/styles.css")
def styles():
    return FileResponse(frontend / "styles.css", media_type="text/css")

@app.get("/app.js")
def javascript():
    return FileResponse(frontend / "app.js", media_type="application/javascript")

@app.get("/api/health")
def health():
    return {"status":"ok", "app":settings.app_name, "memory":memory.status(),
            "lyzr":"configured" if lyzr.configured() else "not configured",
            "omi_webhook_secret_set":bool(settings.omi_webhook_secret)}

@app.get("/api/commitments")
def get_commitments():
    return list(reversed(commitments[-100:]))

@app.get("/api/conflicts")
def get_conflicts():
    return list(reversed(conflicts[-100:]))

@app.get("/api/logs")
def get_logs():
    return logs[:60]

@app.post("/api/ingest")
async def ingest(request: IngestRequest):
    transcript = request.transcript.strip()
    log("Transcript intake", "success", f"Transcript received from {request.source}.", {"characters":len(transcript)})
    prior_records = memory.search(transcript, limit=10)
    prior = [x["payload"] for x in prior_records if x.get("payload", {}).get("kind") == "commitment"]
    for role in ("Extractor", "Conflict Checker", "Drafter"):
        try:
            result = await lyzr.run(role, transcript, prior)
            mode = result.get("mode", "unknown")
            log(role, "success" if mode == "lyzr" else "fallback", result.get("message", f"{role} stage"), {"mode":mode})
        except Exception as exc:
            log(role, "error", f"Lyzr call failed: {exc}")
    extracted = extract_commitments(transcript, request.source)
    created = []
    for item in extracted:
        old_models = []
        for p in prior:
            try:
                from .models import Commitment
                old_models.append(Commitment(**p))
            except Exception:
                pass
        created.extend(detect_conflicts(item, old_models))
        payload = item.model_dump(mode="json")
        payload["kind"] = "commitment"
        commitments.append(payload)
        memory.save(item.id, item.task, payload)
    for c in created:
        conflicts.append(c.model_dump(mode="json"))
        log("Conflict checker", "alert", c.title, {"evidence":c.evidence})
    log("Memory write", "success" if memory.status()=="connected" else "fallback",
        "Stored in Qdrant." if memory.status()=="connected" else "Local demo memory used; configure Qdrant Cloud before submission.",
        {"memory_status":memory.status(), "saved":len(extracted)})
    return {"ok":True, "commitments":[x.model_dump(mode="json") for x in extracted],
            "conflicts":[x.model_dump(mode="json") for x in created],
            "memory_status":memory.status(), "lyzr_status":"configured" if lyzr.configured() else "fallback"}

@app.post("/api/omi/webhook")
async def omi_webhook(request: Request):
    await verify_webhook(request)
    payload = await request.json()
    transcript = extract_transcript(payload)
    return await ingest(IngestRequest(transcript=transcript, source="omi_webhook"))

@app.post("/api/forget")
async def forget(request: Request):
    body = await request.json()
    if body.get("confirmation") != "FORGET":
        raise HTTPException(status_code=400, detail='Send {"confirmation":"FORGET"} to confirm deletion.')
    commitments.clear(); conflicts.clear(); logs.clear(); memory.clear()
    log("Privacy", "success", "Memory cleared by user request.")
    return {"ok":True, "message":"Memory cleared"}
