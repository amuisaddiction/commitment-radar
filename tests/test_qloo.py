
import pytest
import httpx
from app.qloo import QlooClient
from app.config import settings

@pytest.mark.asyncio
async def test_qloo_not_configured():
    client = QlooClient()
    client.api_key = None
    res = await client.get_recommendations('urn:entity:place')
    assert res['status'] == 'unavailable'

@pytest.mark.asyncio
async def test_qloo_mock_response(monkeypatch):
    client = QlooClient()
    client.api_key = 'fake'
    class MockResponse:
        status_code = 200
        def json(self): return {'entities': [{'name':'Mock Place'}]}
        def raise_for_status(self): pass
    async def mock_get(*args, **kwargs): return MockResponse()
    monkeypatch.setattr(httpx.AsyncClient, 'get', mock_get)
    res = await client.get_recommendations('urn:entity:place')
    assert res['status'] == 'ok'
    assert res['data']['entities'][0]['name'] == 'Mock Place'

