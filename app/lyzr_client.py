import httpx
from .config import settings

AGENT_ROLES = {
    "Extractor": "Extract explicit commitments only. Return task, owner, recipient, due date if unambiguous, confidence, and exact source quote. Never invent facts.",
    "Conflict Checker": "Compare new statements with retrieved prior commitments. Return only evidence-supported possible conflicts and quote both source snippets.",
    "Drafter": "Draft a concise, polite follow-up message asking to clarify or renegotiate a commitment. Never send it or invent facts."
}

class LyzrClient:
    def configured(self):
        return bool(settings.lyzr_api_key and settings.lyzr_agent_id and settings.lyzr_api_base_url)

    async def run(self, role, transcript, prior):
        if not self.configured():
            return {"mode": "local_fallback", "message": "Lyzr is not configured; local rules used. This is not a live Lyzr call."}
        headers = {"Authorization": f"Bearer {settings.lyzr_api_key}", "Content-Type": "application/json"}
        payload = {"agent_id": settings.lyzr_agent_id,
                   "input": {"task": AGENT_ROLES[role], "context": {"transcript": transcript, "prior_commitments": prior}}}
        async with httpx.AsyncClient(timeout=25) as client:
            response = await client.post(settings.lyzr_api_base_url, headers=headers, json=payload)
            response.raise_for_status()
            return {"mode": "lyzr", "result": response.json(), "message": f"{role} executed through configured Lyzr endpoint."}
