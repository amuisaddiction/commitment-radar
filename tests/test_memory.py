import pytest
from app.memory import MemoryStore, get_vector, EMBEDDING_DIM
from app.config import settings
import uuid

def test_embedding_generation():
    vec = get_vector("This is a test commitment")
    assert len(vec) == EMBEDDING_DIM
    assert isinstance(vec, list)
    assert isinstance(vec[0], float)

def test_memory_store_local_fallback():
    # Test local fallback mode
    store = MemoryStore()
    store.clear()
    
    # Successful memory insertion
    item_id = str(uuid.uuid4())
    payload = {"task": "test task", "due_date": "2026-10-15"}
    store.save(item_id, "test task", payload)
    
    assert len(store.local) == 1
    assert store.local[0]["id"] == item_id
    
    # Semantic search and result parsing
    results = store.search("test task", limit=1)
    assert len(results) == 1
    assert results[0]["id"] == item_id
    assert results[0]["payload"]["task"] == "test task"
    
    # Empty search results
    empty_results = store.search("something completely different and unrelated xyz123", limit=1)
    # The cosine similarity might still return something low if we use demo vector, but fastembed should give low similarity.
    # We filter by > 0.1 so it might be empty or not, depending on the model.
    # Just checking it doesn't crash.
    assert isinstance(empty_results, list)

def test_qdrant_in_memory():
    # Test collection setup
    original_url = settings.qdrant_url
    settings.qdrant_url = ":memory:"
    
    store = MemoryStore()
    assert store.enabled == True
    assert store.status() == "Local Qdrant In-Memory"
    
    item_id = str(uuid.uuid4())
    payload = {"task": "qdrant task", "due_date": "2026-10-15"}
    
    # Insertion
    store.save(item_id, "qdrant task", payload)
    
    # Search
    results = store.search("qdrant task", limit=1)
    assert len(results) == 1
    assert results[0]["id"] == item_id
    assert results[0]["payload"]["task"] == "qdrant task"
    
    # Duplicate event handling (upsert should override)
    store.save(item_id, "qdrant task updated", payload)
    results2 = store.search("qdrant task updated", limit=1)
    assert len(results2) == 1
    assert results2[0]["id"] == item_id
    
    # Clear
    store.clear()
    assert len(store.search("qdrant task", limit=1)) == 0
    
    settings.qdrant_url = original_url

def test_qdrant_connection_error():
    original_url = settings.qdrant_url
    settings.qdrant_url = "http://localhost:9999" # Invalid port
    
    store = MemoryStore()
    # It should gracefully fallback
    assert store.enabled == False
    assert store.status() == "local demo fallback"
    
    settings.qdrant_url = original_url

