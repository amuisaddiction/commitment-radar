import pytest
import json
import httpx
from unittest.mock import patch, MagicMock, AsyncMock
from app.lyzr_client import LyzrClient
from app.config import settings

@pytest.fixture
def unconfigured_lyzr(monkeypatch):
    monkeypatch.setattr(settings, "lyzr_api_key", "")
    monkeypatch.setattr(settings, "lyzr_agent_id", "")
    return LyzrClient()

@pytest.fixture
def configured_lyzr(monkeypatch):
    monkeypatch.setattr(settings, "lyzr_api_key", "test_key")
    monkeypatch.setattr(settings, "lyzr_agent_id", "test_agent")
    return LyzrClient()

@pytest.mark.asyncio
async def test_missing_credentials(unconfigured_lyzr):
    res = await unconfigured_lyzr.run("Extractor", "I promise test")
    assert res["mode"] == "local_fallback"
    assert "missing" in res["message"].lower()

@pytest.mark.asyncio
@patch("httpx.AsyncClient.post")
async def test_successful_response(mock_post, configured_lyzr):
    mock_json = {"task": "test", "confidence": 0.9}
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"response": f"```json\n{json.dumps(mock_json)}\n```"}
    mock_resp.raise_for_status.return_value = None
    mock_post.return_value = mock_resp
    
    res = await configured_lyzr.run("Extractor", "I promise test")
    assert res["mode"] == "lyzr"
    assert res["result"]["task"] == "test"

@pytest.mark.asyncio
@patch("httpx.AsyncClient.post")
async def test_malformed_output(mock_post, configured_lyzr):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"response": "This is not JSON at all."}
    mock_resp.raise_for_status.return_value = None
    mock_post.return_value = mock_resp
    
    res = await configured_lyzr.run("Extractor", "I promise test")
    assert res["mode"] == "error"
    assert "malformed" in res["message"].lower()

@pytest.mark.asyncio
@patch("httpx.AsyncClient.post")
async def test_api_error(mock_post, configured_lyzr):
    mock_resp = MagicMock()
    mock_resp.status_code = 500
    mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError("Error", request=MagicMock(), response=mock_resp)
    mock_post.return_value = mock_resp
    
    res = await configured_lyzr.run("Extractor", "I promise test")
    assert res["mode"] == "error"
    assert "500" in res["message"]

@pytest.mark.asyncio
@patch("httpx.AsyncClient.post")
async def test_timeout(mock_post, configured_lyzr):
    mock_post.side_effect = httpx.ReadTimeout("Timeout")
    
    res = await configured_lyzr.run("Extractor", "I promise test")
    assert res["mode"] == "error"
    assert "timeout" in res["message"].lower()
