import httpx
from .config import settings

class QlooClient:
    def __init__(self):
        self.base_url = "https://hackathon.api.qloo.com"
        self.api_key = getattr(settings, 'qloo_api_key', None)

    def is_configured(self) -> bool:
        return bool(self.api_key)

    async def get_recommendations(self, entity_type: str, tags: list[str] = None):
        """
        Get Qloo recommendations using the Insights API.
        entity_type should be one of the supported URNs, e.g. "urn:entity:place"
        """
        if not self.is_configured():
            return {"error": "Qloo API key not configured.", "status": "unavailable"}

        headers = {"X-Api-Key": self.api_key}
        params = {"filter.type": entity_type}
        
        # This is a simplified call since we don't have valid tag IDs yet.
        # In a complete flow, we would search for tag IDs first.
        
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(f"{self.base_url}/v2/insights", headers=headers, params=params)
                
                if response.status_code == 401:
                    return {"error": "Invalid Qloo API key.", "status": "unavailable"}
                
                response.raise_for_status()
                return {"status": "ok", "data": response.json()}
        except httpx.RequestError as exc:
            return {"error": f"Request failed: {exc}", "status": "error"}
        except httpx.HTTPStatusError as exc:
            return {"error": f"HTTP error {exc.response.status_code}", "status": "error"}

