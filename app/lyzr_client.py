import httpx
import json
from app.config import settings

AGENT_ROLES = {
    "Extractor": "Extract explicit commitments only. Return a JSON array of objects with keys: 'task', 'owner', 'recipient', 'due_date' (ISO or null), 'source_text', 'confidence' (float 0-1). Never invent facts. ONLY RETURN JSON.",
    "Conflict Checker": "Compare the new transcript with retrieved prior commitments. Return a JSON array of conflict objects with keys: 'title', 'explanation', 'severity' (high/medium/low), 'related_task' (from prior), 'evidence' (list of 2 strings). ONLY RETURN JSON.",
    "Drafter": "Draft a concise, polite follow-up message asking to clarify or renegotiate a commitment. Return JSON object with key 'suggested_message'. ONLY RETURN JSON.",
    "Fulfillment Planner": "Determine if the commitment involves lifestyle activities. Return a JSON object with keys: 'category' (e.g. 'urn:entity:place' for dining, 'urn:entity:movie' for films) and 'keywords'. If none, return empty JSON. ONLY RETURN JSON."
}

class LyzrClient:
    def configured(self):
        return bool(settings.lyzr_api_key and settings.lyzr_agent_id)

    async def run(self, role, transcript, prior=None):
        if not self.configured():
            return {"mode": "local_fallback", "message": "Lyzr API key or agent ID missing. Local fallback used.", "result": None}
        
        prompt = f"Role Instructions:\n{AGENT_ROLES.get(role, '')}\n\nTranscript:\n{transcript}\n"
        if prior:
            prompt += f"\nContext (Prior Commitments):\n{json.dumps(prior)}\n"
            
        url = settings.lyzr_api_base_url or "https://agent-prod.studio.lyzr.ai/v3/inference/chat/"
        headers = {"x-api-key": settings.lyzr_api_key, "Content-Type": "application/json"}
        payload = {
            "user_id": "commitment-radar-user",
            "agent_id": settings.lyzr_agent_id,
            "session_id": "radar-session",
            "message": prompt
        }
        
        try:
            async with httpx.AsyncClient(timeout=25) as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                
                response_text = data.get("response") or data.get("message") or data.get("output") or ""
                if isinstance(response_text, dict):
                    return {"mode": "lyzr", "result": response_text, "message": f"{role} executed."}
                
                if "```json" in response_text:
                    json_str = response_text.split("```json")[1].split("```")[0].strip()
                elif "```" in response_text:
                    json_str = response_text.split("```")[1].strip()
                else:
                    json_str = response_text.strip()
                
                try:
                    parsed = json.loads(json_str) if json_str else {}
                    return {"mode": "lyzr", "result": parsed, "message": f"{role} executed."}
                except json.JSONDecodeError:
                    return {"mode": "error", "message": "Malformed Lyzr JSON output.", "result": None}
                    
        except httpx.RequestError as exc:
            return {"mode": "error", "message": f"Lyzr request failed: {exc}", "result": None}
        except httpx.HTTPStatusError as exc:
            return {"mode": "error", "message": f"Lyzr HTTP error {exc.response.status_code}", "result": None}
        except Exception as exc:
            return {"mode": "error", "message": f"Lyzr exception: {exc}", "result": None}
