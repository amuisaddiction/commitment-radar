from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from datetime import datetime, timezone
import uuid
from app.config import settings
from app.models import IngestRequest, FulfillmentSuggestion, Commitment, Conflict
from app.commitments import extract_commitments, detect_conflicts
from app.memory import MemoryStore
from app.lyzr_client import LyzrClient
from app.qloo import QlooClient
from app.omi import extract_transcript, verify_webhook

app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
memory, lyzr, qloo = MemoryStore(), LyzrClient(), QlooClient()
commitments, conflicts, suggestions, logs = [], [], [], []
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
            "lyzr":"Live Lyzr" if lyzr.configured() else "Local Fallback",
            "qloo":"Live Qloo" if getattr(settings, 'qloo_api_key', '') else "Local Fallback",
            "omi_webhook_secret_set":bool(settings.omi_webhook_secret)}

@app.get("/api/commitments")
def get_commitments():
    return list(reversed(commitments[-100:]))

@app.get("/api/conflicts")
def get_conflicts():
    return list(reversed(conflicts[-100:]))

@app.get("/api/suggestions")
def get_suggestions():
    return list(reversed(suggestions[-100:]))

@app.get("/api/logs")
def get_logs():
    return logs[:60]

@app.post("/api/ingest")
async def ingest(request: IngestRequest):
    transcript = request.transcript.strip()
    log("Transcript intake", "success", f"Transcript received from {request.source}.", {"characters":len(transcript)})
    
    prior_records = memory.search(transcript, limit=10)
    prior = [x["payload"] for x in prior_records if x.get("payload", {}).get("kind") == "commitment"]
    
    # 1. Extractor
    extracted = []
    extractor_res = await lyzr.run("Extractor", transcript, prior)
    if extractor_res.get("mode") == "lyzr" and isinstance(extractor_res.get("result"), list):
        log("Extractor", "success", "Lyzr extracted commitments")
        for item in extractor_res["result"]:
            try:
                c = Commitment(
                    id=str(uuid.uuid4()), task=item.get("task", ""), owner=item.get("owner"),
                    recipient=item.get("recipient"), due_date=item.get("due_date"),
                    source_text=item.get("source_text", transcript), source=request.source,
                    confidence=float(item.get("confidence", 0.8))
                )
                extracted.append(c)
            except Exception as e:
                pass
    else:
        log("Extractor", "fallback", "Lyzr unavailable or failed. Using local fallback extraction.")
        extracted = extract_commitments(transcript, request.source)

    created_conflicts = []
    created_suggestions = []
    
    session_models = []
    for item in extracted:
        old_models = []
        for p in prior:
            try:
                old_models.append(Commitment(**p))
            except Exception:
                pass
        old_models.extend(session_models)
        session_models.append(item)
                
        # 2. Conflict Checker
        conflict_res = await lyzr.run("Conflict Checker", transcript, prior)
        if conflict_res.get("mode") == "lyzr" and isinstance(conflict_res.get("result"), list) and len(conflict_res["result"]) > 0:
            log("Conflict Checker", "alert", "Lyzr detected conflicts")
            for conf in conflict_res["result"]:
                try:
                    c = Conflict(
                        id=str(uuid.uuid4()), title=conf.get("title", "Conflict"),
                        explanation=conf.get("explanation", ""), severity=conf.get("severity", "medium"),
                        current_commitment_id=item.id, related_commitment_id=conf.get("related_task_id", ""),
                        evidence=conf.get("evidence", [])
                    )
                    created_conflicts.append(c)
                except Exception:
                    pass
        else:
            local_conflicts = detect_conflicts(item, old_models)
            if local_conflicts:
                log("Conflict Checker", "alert", "Local fallback detected conflicts")
            created_conflicts.extend(local_conflicts)
            
        # 3. Drafter
        if created_conflicts:
            drafter_res = await lyzr.run("Drafter", transcript, prior)
            if drafter_res.get("mode") == "lyzr" and isinstance(drafter_res.get("result"), dict):
                log("Drafter", "success", "Lyzr drafted follow-up message")
                for c in created_conflicts:
                    c.suggested_message = drafter_res["result"].get("suggested_message", "")
        
        # 4. Fulfillment Planner
        planner_res = await lyzr.run("Fulfillment Planner", transcript, prior)
        cat = None
        if planner_res.get("mode") == "lyzr" and isinstance(planner_res.get("result"), dict):
            cat = planner_res["result"].get("category")
            if cat and cat != "none":
                log("Fulfillment Planner", "info", f"Lyzr identified lifestyle category: {cat}")
            else:
                cat = None
        else:
            low = item.task.lower()
            if any(k in low for k in ["dinner", "lunch", "restaurant", "eat", "cafe"]):
                cat = "urn:entity:place"
            elif any(k in low for k in ["movie", "film", "cinema"]):
                cat = "urn:entity:movie"
            if cat:
                log("Fulfillment Planner", "fallback", f"Local fallback identified category: {cat}")
            
        if cat:
            qloo_res = await qloo.get_recommendations(cat)
            if qloo_res["status"] == "ok":
                entities = qloo_res["data"].get("entities", [])
                items = [{"name": e.get("name"), "description": e.get("description")} for e in entities[:3]]
                if items:
                    sug = FulfillmentSuggestion(
                        id=str(uuid.uuid4()), commitment_id=item.id, category=cat, items=items,
                        explanation="Qloo cultural intelligence suggests these based on your commitment."
                    )
                    created_suggestions.append(sug)
                    log("Qloo Client", "success", f"Fetched {len(items)} recommendations", {"category": cat})
            else:
                log("Qloo Client", "error", qloo_res.get("error", "Qloo API error"), {"status": qloo_res["status"]})
                created_suggestions.append(FulfillmentSuggestion(
                    id=str(uuid.uuid4()), commitment_id=item.id, category=cat, items=[],
                    explanation="Qloo integration is not configured or unavailable. Recommendations skipped.", status="unavailable"
                ))

        payload = item.model_dump(mode="json")
        payload["kind"] = "commitment"
        commitments.append(payload)
        memory.save(item.id, item.task, payload)
        
    for c in created_conflicts:
        conflicts.append(c.model_dump(mode="json"))
        
    for s in created_suggestions:
        suggestions.append(s.model_dump(mode="json"))
        
    log("Memory write", "success" if "Connected" in memory.status() else "fallback",
        "Stored in Qdrant." if "Connected" in memory.status() else "Local memory used; configure Qdrant Cloud before submission.",
        {"memory_status":memory.status(), "saved":len(extracted)})
        
    return {"ok":True, "commitments":[x.model_dump(mode="json") for x in extracted],
            "conflicts":[x.model_dump(mode="json") for x in created_conflicts],
            "suggestions":[x.model_dump(mode="json") for x in created_suggestions],
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
    commitments.clear(); conflicts.clear(); suggestions.clear(); logs.clear(); memory.clear()
    log("Privacy", "success", "Memory cleared by user request.")
    return {"ok":True, "message":"Memory cleared"}
