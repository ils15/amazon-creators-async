import pytest
import httpx
from pydantic import ValidationError

from amazon_creators_async.client import AmazonCreatorsAsyncClient


class MockResponse:
    def __init__(self, status_code, payload=None, text="", headers=None):
        self.status_code = status_code
        self._payload = payload or {}
        self.text = text
        self.headers = headers or {}

    def json(self):
        return self._payload


class MockHTTPClient:
    def __init__(self, outcomes):
        self._outcomes = list(outcomes)
        self.calls = 0

    async def post(self, *args, **kwargs):
        self.calls += 1
        outcome = self._outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


@pytest.mark.asyncio
async def test_request_retries_network_errors_then_succeeds():
    mock_client = MockHTTPClient(
        [
            httpx.ConnectError("temporary network issue"),
            MockResponse(200, payload={"ok": True}),
        ]
    )
    client = AmazonCreatorsAsyncClient(
        credential_id="id",
        credential_secret="secret",
        partner_tag="tag-20",
        client=mock_client,
        version="3.1",
        max_retries=2,
        retry_backoff_seconds=0.01,
    )

    async def fake_token():
        return "token"

    client._auth_manager.get_valid_token = fake_token

    result = await client._request("searchItems", {"keywords": "keyboard"})
    assert result == {"ok": True}
    assert mock_client.calls == 2


@pytest.mark.asyncio
async def test_get_items_rejects_empty_item_ids():
    client = AmazonCreatorsAsyncClient(
        credential_id="id",
        credential_secret="secret",
        partner_tag="tag-20",
        version="3.1",
    )

    with pytest.raises(ValueError, match="item_ids must contain at least one ASIN"):
        await client.get_items([])

    await client.close()


@pytest.mark.asyncio
async def test_search_items_requires_at_least_one_criterion():
    client = AmazonCreatorsAsyncClient(
        credential_id="id",
        credential_secret="secret",
        partner_tag="tag-20",
        version="3.1",
    )

    with pytest.raises(ValidationError, match="At least one search criterion"):
        await client.search_items(item_count=1)

    await client.close()
