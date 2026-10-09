import hashlib, math
from typing import Any
from .config import settings

def demo_vector(text: str, dims: int = 64):
    vec = [0.0] * dims
    for token in text.lower().split():
        digest = hashlib.sha256(token.encode()).digest()
        vec[int.from_bytes(digest[:4], "big") % dims] += 1.0 if digest[4] % 2 else -1.0
    norm = math.sqrt(sum(x*x for x in vec)) or 1.0
    return [x/norm for x in vec]

class MemoryStore:
    def __init__(self):
        self.local: list[dict[str, Any]] = []
        self.client = None
        self.models = None
        self.enabled = False
        if settings.qdrant_url and settings.qdrant_api_key:
            try:
                from qdrant_client import QdrantClient, models
                self.client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key, timeout=8)
                self.models = models
                if not self.client.collection_exists(settings.qdrant_collection):
                    self.client.create_collection(collection_name=settings.qdrant_collection,
                        vectors_config=models.VectorParams(size=64, distance=models.Distance.COSINE))
                self.enabled = True
            except Exception as exc:
                print("Qdrant init failed; local demo fallback:", exc)

    def save(self, item_id, text, payload):
        vector = demo_vector(text)
        self.local.append({"id": item_id, "text": text, "payload": payload, "vector": vector})
        if self.enabled:
            self.client.upsert(collection_name=settings.qdrant_collection,
                points=[self.models.PointStruct(id=item_id, vector=vector, payload={**payload, "text": text})])

    def search(self, text, limit=8):
        if self.enabled:
            try:
                hits = self.client.query_points(collection_name=settings.qdrant_collection,
                    query=demo_vector(text), limit=limit, with_payload=True).points
                return [{"id": str(p.id), "text": (p.payload or {}).get("text", ""),
                         "payload": p.payload or {}} for p in hits]
            except Exception as exc:
                print("Qdrant search failed:", exc)
        tokens = set(text.lower().split())
        ranked = sorted(((len(tokens & set(x["text"].lower().split())) / max(1, len(tokens | set(x["text"].lower().split()))), x) for x in self.local), key=lambda z: z[0], reverse=True)
        return [x for score, x in ranked[:limit] if score > 0]

    def clear(self):
        self.local.clear()
        if self.enabled:
            try:
                self.client.delete_collection(settings.qdrant_collection)
                self.client.create_collection(collection_name=settings.qdrant_collection,
                    vectors_config=self.models.VectorParams(size=64, distance=self.models.Distance.COSINE))
            except Exception as exc:
                print("Qdrant clear failed:", exc)

    def status(self):
        return "connected" if self.enabled else "local demo fallback"
