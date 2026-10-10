import re, uuid
from datetime import datetime, timedelta
from app.models import Commitment, Conflict

def due_date(text: str):
    low = text.lower()
    today = datetime.now().date()
    if "tomorrow" in low:
        return (today + timedelta(days=1)).isoformat()
    if "today" in low or "tonight" in low:
        return today.isoformat()
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for idx, day in enumerate(days):
        if re.search(rf"\b{day}\b", low):
            delta = (idx - today.weekday()) % 7 or 7
            return (today + timedelta(days=delta)).isoformat()
    return None

def extract_commitments(transcript: str, source: str = "manual_demo"):
    chunks = re.split(r"(?<=[.!?])\s+|\n+", transcript.strip())
    cues = ("i will", "i'll", "i can", "i promised", "i promise", "need to", "must ", "going to", "i should")
    results = []
    for sentence in chunks:
        sentence = sentence.strip(" .\t")
        low = sentence.lower()
        if len(sentence) < 8 or not any(cue in low for cue in cues):
            continue
        match = re.search(r"\b(?:to|for)\s+([A-Z][a-z]+)\b", sentence)
        results.append(Commitment(
            id=str(uuid.uuid4()), task=sentence, owner="You" if low.startswith(("i will", "i'll", "i promised", "i promise")) else None,
            recipient=match.group(1) if match else None, due_date=due_date(sentence),
            source_text=sentence, source=source, confidence=0.68))
    if not results and re.search(r"[a-zA-Z]", transcript):
        results.append(Commitment(id=str(uuid.uuid4()), task=transcript.strip()[:240],
            source_text=transcript.strip(), source=source, confidence=0.35))
    return results

def detect_conflicts(current: Commitment, previous: list[Commitment]):
    found = []
    keywords = ("invoice", "report", "book", "submit", "call", "meeting", "send", "finish", "deliver")
    for old in previous:
        same_topic = any(k in current.task.lower() and k in old.task.lower() for k in keywords)
        
        travel_current = any(k in current.task.lower() for k in ("travel", "travelling", "traveling", "flight", "unavailable"))
        travel_old = any(k in old.task.lower() for k in ("travel", "travelling", "traveling", "flight", "unavailable"))
        
        availability_clash = (travel_current or travel_old) and current.due_date and old.due_date and current.due_date == old.due_date and not (travel_current and travel_old)
        date_clash = same_topic and current.due_date and old.due_date and current.due_date != old.due_date
        
        if availability_clash:
            found.append(Conflict(
                id=str(uuid.uuid4()), title="Possible schedule risk",
                explanation="This travel or unavailability overlaps with an existing deadline.",
                severity="high",
                current_commitment_id=current.id, related_commitment_id=old.id,
                evidence=[f"New: {current.source_text}", f"Earlier: {old.source_text}"],
                suggested_message="Hi, I have a schedule clash on this day. Could we confirm the deadline and agree on an updated time?"))
        elif same_topic and date_clash:
            found.append(Conflict(
                id=str(uuid.uuid4()), title="Possible deadline conflict",
                explanation="The new statement may conflict with a previously stored commitment.",
                severity="medium",
                current_commitment_id=current.id, related_commitment_id=old.id,
                evidence=[f"New: {current.source_text}", f"Earlier: {old.source_text}"],
                suggested_message="Hi, I may have a timing conflict with this commitment. Could we confirm the deadline and agree on an updated time?"))
    return found
