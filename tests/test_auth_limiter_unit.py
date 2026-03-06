import asyncio

import pytest

from amazon_creators_async.auth import AuthManager
from amazon_creators_async.limiter import RateLimiter, limiter_config_from_tps


class MockAuthResponse:
    def __init__(self, payload):
        self.status_code = 200
        self._payload = payload
        self.text = "ok"

    def json(self):
        return self._payload


class MockAuthHTTPClient:
    def __init__(self):
        self.calls = 0

    async def post(self, *args, **kwargs):
        self.calls += 1
        return MockAuthResponse({"access_token": "cached-token", "expires_in": 3600})


@pytest.mark.asyncio
async def test_auth_manager_serializes_concurrent_refreshes():
    mock_client = MockAuthHTTPClient()
    manager = AuthManager(
        credential_id="id",
        credential_secret="secret",
        version="3.1",
        client=mock_client,
    )

    tokens = await asyncio.gather(*[manager.get_valid_token() for _ in range(5)])

    assert tokens == ["cached-token"] * 5
    assert mock_client.calls == 1


def test_limiter_config_supports_fractional_tps():
    max_rate, time_period = limiter_config_from_tps(0.5)
    assert max_rate == 1
    assert time_period == 2.0


def test_rate_limiter_rejects_invalid_tps():
    with pytest.raises(ValueError, match="tps must be greater than 0"):
        RateLimiter(tps=0)
