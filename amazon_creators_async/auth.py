import base64
import time
import asyncio
import httpx
from typing import Optional

from .exceptions import AuthenticationError
from .utils import get_auth_endpoint, get_scope


def _safe_error_snippet(text: str, max_len: int = 240) -> str:
    """Return a short single-line snippet for safer exception messages."""
    normalized = " ".join(text.split())
    if len(normalized) > max_len:
        return normalized[:max_len] + "..."
    return normalized

class AuthManager:
    """
    Manages OAuth 2.0 Client Credentials token fetching and caching
    for the Amazon Creators API. Supports both Cognito (v2.x) and LWA (v3.x).
    """
    
    def __init__(
        self, 
        credential_id: str, 
        credential_secret: str, 
        version: str,
        client: Optional[httpx.AsyncClient] = None
    ):
        self.credential_id = credential_id
        self.credential_secret = credential_secret
        self.version = version
        
        # Determine endpoints and scopes
        self.auth_url = get_auth_endpoint(version)
        self.scope = get_scope(version)
        
        # Pass a client if you want to share the connection pool, otherwise we manage our own
        self._client = client or httpx.AsyncClient(timeout=30.0)
        self._owns_client = client is None
        self._token_lock = asyncio.Lock()

        # State for token caching
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0.0

    async def get_valid_token(self) -> str:
        """
        Returns a valid OAuth 2.0 access token. 
        If the current token is missing or expired (with a 60s buffer), it fetches a new one.
        """
        if self._access_token and time.time() < (self._token_expires_at - 60):
            return self._access_token

        # Avoid parallel refreshes from concurrent API calls.
        async with self._token_lock:
            if self._access_token and time.time() < (self._token_expires_at - 60):
                return self._access_token
            return await self._fetch_new_token()

    async def _fetch_new_token(self) -> str:
        """
        Performs the HTTP call to the auth endpoint to get the token.
        Handles both Cognito (form-encoded) and LWA (JSON) versions.
        """
        is_lwa = self.version.startswith("3.")
        
        try:
            if is_lwa:
                # LWA (v3.1+) uses JSON body with credentials inside
                headers = {"Content-Type": "application/json"}
                payload = {
                    "grant_type": "client_credentials",
                    "client_id": self.credential_id,
                    "client_secret": self.credential_secret,
                    "scope": self.scope
                }
                response = await self._client.post(self.auth_url, headers=headers, json=payload)
            else:
                # Cognito (v2.x) uses Basic Auth + form-encoded data
                auth_string = f"{self.credential_id}:{self.credential_secret}"
                encoded_auth = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Basic {encoded_auth}"
                }
                data = {
                    "grant_type": "client_credentials",
                    "scope": self.scope
                }
                response = await self._client.post(self.auth_url, headers=headers, data=data)
            
            if response.status_code != 200:
                snippet = _safe_error_snippet(response.text)
                raise AuthenticationError(
                    f"Failed to obtain token ({self.version}). Status: {response.status_code}. "
                    f"Response preview: {snippet}"
                )

            try:
                payload_data = response.json()
                self._access_token = payload_data["access_token"]
            except (ValueError, KeyError, TypeError) as exc:
                raise AuthenticationError(
                    "Invalid auth response format: missing or malformed access_token"
                ) from exc
            
            # Usually expires in 3600 seconds (1 hour)
            expires_in = payload_data.get("expires_in", 3600)
            self._token_expires_at = time.time() + expires_in
            
            return self._access_token
        except httpx.RequestError as exc:
            raise AuthenticationError(f"HTTP error occurred while requesting auth token: {exc}") from exc

    async def close(self):
        """Close internally managed HTTP client."""
        if self._owns_client:
            await self._client.aclose()
