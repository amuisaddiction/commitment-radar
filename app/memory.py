import hashlib, math
from typing import Any
from app.config import settings

try:
    from fastembed import TextEmbedding
    # Load the lightweight BAAI embedding model
    embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    EMBEDDING_DIM = 384
except ImportError:
    embedding_model = None
    EMBEDDING_DIM = 64
    print("fastembed not installed. Falling back to demo embeddings.")

def get_vector(text: str):
    if embedding_model:
        # Generate real embedding using fastembed
        return list(embedding_model.embed([text]))[0].tolist()
    else:
        # Fallback to pseudo-random demo vector if fastembed isn't available
        vec = [0.0] * EMBEDDING_DIM
        for token in text.lower().split():
            digest = hashlib.sha256(token.encode()).digest()
            vec[int.from_bytes(digest[:4], "big") % EMBEDDING_DIM] += 1.0 if digest[4] % 2 else -1.0
        norm = math.sqrt(sum(x*x for x in vec)) or 1.0
        return [x/norm for x in vec]

class MemoryStore:
    def __init__(self):
        self.local: list[dict[str, Any]] = []
        self.client = None
        self.models = None
        self.enabled = False
        self.mode = "local demo fallback"
        
        # If QDRANT_URL is set, we attempt to connect (either Cloud or Local)
        if settings.qdrant_url:
            try:
                from qdrant_client import QdrantClient, models
                
                # If qdrant_url is ':memory:' or a local path, api_key is optional
                kwargs = {"url": settings.qdrant_url, "timeout": 10}
                if settings.qdrant_api_key:
                    kwargs["api_key"] = settings.qdrant_api_key
                elif not (settings.qdrant_url == ":memory:" or settings.qdrant_url.startswith("http")):
                    kwargs = {"path": settings.qdrant_url}
                elif settings.qdrant_url == ":memory:":
                    kwargs = {"location": ":memory:"}
                    
                self.client = QdrantClient(**kwargs)
                self.models = models
                
                # Check collection and create with appropriate dimension
                if not self.client.collection_exists(settings.qdrant_collection):
                    self.client.create_collection(
                        collection_name=settings.qdrant_collection,
                        vectors_config=models.VectorParams(size=EMBEDDING_DIM, distance=models.Distance.COSINE)
                    )
                self.enabled = True
                
                if "cloud.qdrant.io" in settings.qdrant_url.lower():
                    self.mode = "Qdrant Cloud Connected"
                elif settings.qdrant_url == ":memory:":
                    self.mode = "Local Qdrant In-Memory"
                else:
                    self.mode = "Local Qdrant Connected"
            except Exception as exc:
                print(f"Qdrant init failed ({settings.qdrant_url}); falling back to local demo mode. Error: {exc}")
        else:
            print("Qdrant credentials not configured. Using local dictionary fallback.")

    def save(self, item_id, text, payload):
        vector = get_vector(text)
        self.local.append({"id": item_id, "text": text, "payload": payload, "vector": vector})
        
        if self.enabled:
            try:
                self.client.upsert(
                    collection_name=settings.qdrant_collection,
                    points=[self.models.PointStruct(id=item_id, vector=vector, payload={**payload, "text": text})]
                )
            except Exception as exc:
                print(f"Qdrant write failed: {exc}")

    def search(self, text, limit=8):
        vector = get_vector(text)
        
        if self.enabled:
            try:
                hits = self.client.query_points(
                    collection_name=settings.qdrant_collection,
                    query=vector, limit=limit, with_payload=True
                ).points
                return [{"id": str(p.id), "text": (p.payload or {}).get("text", ""),
                         "payload": p.payload or {}} for p in hits if p.score > 0.1]
            except Exception as exc:
                print(f"Qdrant search failed: {exc}")
        
        # Fallback local search using cosine similarity on generated vectors
        def cosine_sim(v1, v2):
            dot = sum(a*b for a, b in zip(v1, v2))
            norm1 = math.sqrt(sum(a*a for a in v1))
            norm2 = math.sqrt(sum(b*b for b in v2))
            return dot / (norm1 * norm2) if norm1 and norm2 else 0.0

        ranked = []
        for x in self.local:
            sim = cosine_sim(vector, x["vector"])
            ranked.append((sim, x))
            
        ranked.sort(key=lambda z: z[0], reverse=True)
        return [x for score, x in ranked[:limit] if score > 0.1]

    def clear(self):
        self.local.clear()
        if self.enabled:
            try:
                self.client.delete_collection(settings.qdrant_collection)
                self.client.create_collection(
                    collection_name=settings.qdrant_collection,
                    vectors_config=self.models.VectorParams(size=EMBEDDING_DIM, distance=self.models.Distance.COSINE)
                )
            except Exception as exc:
                print(f"Qdrant clear failed: {exc}")

    def status(self):
        return self.mode
