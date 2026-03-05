import asyncio
import httpx
from typing import Optional, Dict, Any, List

from .auth import AuthManager
from .limiter import RateLimiter
from .utils import Region, get_api_endpoint, get_version_for_region, validate_marketplace
from .exceptions import RateLimitError, InvalidRequestError, APIError
from .models.requests import SearchItemsRequest, GetItemsRequest, GetBrowseNodesRequest, GetVariationsRequest
from .models.responses import SearchItemsResponse, GetItemsResponse, GetBrowseNodesResponse, GetVariationsResponse

class AmazonCreatorsAsyncClient:
    """
    Asynchronous client for the Amazon Creators API.
    Handles OAuth 2.0 authentication, rate limiting, and parameter serialization.
    """

    def __init__(
        self,
        credential_id: str,
        credential_secret: str,
        marketplace: str = "www.amazon.com.br",
        partner_tag: str = "",
        region: Region = Region.NORTH_AMERICA,
        version: Optional[str] = None, # Allow explicit version (e.g. 3.1)
        rate_limit_tps: float = 1.0,
        max_retries: int = 2,
        retry_backoff_seconds: float = 0.5,
        client: Optional[httpx.AsyncClient] = None
    ):
        validate_marketplace(marketplace)
        if not partner_tag:
            raise ValueError("partner_tag is required.")

        self.credential_id = credential_id
        self.credential_secret = credential_secret
        self.marketplace = marketplace
        self.partner_tag = partner_tag
        self.region = region
        self.api_version = version or get_version_for_region(region)
        self.endpoint_url = get_api_endpoint(region)
        self.max_retries = max(0, int(max_retries))
        self.retry_backoff_seconds = max(0.1, float(retry_backoff_seconds))
        
        # Async HTTP client
        self._client = client or httpx.AsyncClient(timeout=30.0)
        self._owns_client = client is None

        # Managers
        self._auth_manager = AuthManager(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.api_version,
            client=self._client
        )
        self._limiter = RateLimiter(tps=rate_limit_tps)

    async def _request(self, operation: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Core method to dispatch a request to the Amazon API with Auth & Limiter."""
        url = f"{self.endpoint_url}/{operation}"

        for attempt in range(self.max_retries + 1):
            # 1. Wait for Rate Limiter Capacity.
            await self._limiter.acquire()

            # 2. Get a valid OAuth2 Token (cached or renewed).
            token = await self._auth_manager.get_valid_token()

            # 3. Prepare headers.
            if self.api_version.startswith("3."):
                auth_header = f"Bearer {token}"
            else:
                auth_header = f"Bearer {token}, Version {self.api_version}"

            headers = {
                "Content-Type": "application/json",
                "Authorization": auth_header,
                "x-marketplace": self.marketplace,
                "User-Agent": "amazon_creators_async/0.1.0",
            }

            try:
                response = await self._client.post(url, json=payload, headers=headers)
            except httpx.RequestError as exc:
                if attempt >= self.max_retries:
                    raise APIError(f"Network error: {exc}") from exc
                await asyncio.sleep(self.retry_backoff_seconds * (2 ** attempt))
                continue

            if response.status_code == 200:
                return response.json()

            if response.status_code == 429:
                if attempt >= self.max_retries:
                    raise RateLimitError(f"Rate limit exceeded: {response.text}")
                retry_after = response.headers.get("Retry-After")
                delay = self.retry_backoff_seconds * (2 ** attempt)
                if retry_after:
                    try:
                        delay = max(0.0, float(retry_after))
                    except ValueError:
                        pass
                await asyncio.sleep(delay)
                continue

            if response.status_code == 400:
                raise InvalidRequestError(f"Invalid request: {response.text}")

            if response.status_code in {500, 502, 503, 504} and attempt < self.max_retries:
                await asyncio.sleep(self.retry_backoff_seconds * (2 ** attempt))
                continue

            raise APIError(
                f"API Error ({response.status_code}): {response.text}",
                status_code=response.status_code,
            )

        raise APIError("Unexpected request retry flow termination")

    async def search_items(self, **kwargs) -> SearchItemsResponse:
        """
        Search for items on Amazon using keywords, browse_node_id, brand, etc.
        """
        # Inject defaults if missing
        kwargs.setdefault("marketplace", self.marketplace)
        kwargs.setdefault("partner_tag", self.partner_tag)
        
        # Validate through Pydantic model
        request_obj = SearchItemsRequest(**kwargs)
        
        # Export forcing lowerCamelCase format and removing nulls
        payload = request_obj.model_dump(by_alias=True, exclude_none=True)
        
        data = await self._request("searchItems", payload)
        return SearchItemsResponse(**data)

    async def get_items(self, item_ids: List[str], **kwargs) -> GetItemsResponse:
        """
        Get detailed item information using a batch of ASINs (ItemIds).
        """
        if not item_ids:
            raise ValueError("item_ids must contain at least one ASIN")

        kwargs.setdefault("marketplace", self.marketplace)
        kwargs.setdefault("partner_tag", self.partner_tag)
        kwargs["item_ids"] = item_ids
        
        # Validate through Pydantic model
        request_obj = GetItemsRequest(**kwargs)
        
        # Export forcing lowerCamelCase format and removing nulls
        payload = request_obj.model_dump(by_alias=True, exclude_none=True)
        
        data = await self._request("getItems", payload)
        return GetItemsResponse(**data)

    async def get_browse_nodes(self, browse_node_ids: List[str], **kwargs) -> GetBrowseNodesResponse:
        """
        Get Browse Node details (categories geometry) on Amazon using their IDs.
        """
        kwargs.setdefault("marketplace", self.marketplace)
        kwargs.setdefault("partner_tag", self.partner_tag)
        kwargs["browse_node_ids"] = browse_node_ids
        
        request_obj = GetBrowseNodesRequest(**kwargs)
        payload = request_obj.model_dump(by_alias=True, exclude_none=True)
        
        data = await self._request("getBrowseNodes", payload)
        return GetBrowseNodesResponse(**data)

    async def get_variations(self, asin: str, **kwargs) -> GetVariationsResponse:
        """
        Get all variations (e.g. size, colors) for a given parent ASIN.
        """
        kwargs.setdefault("marketplace", self.marketplace)
        kwargs.setdefault("partner_tag", self.partner_tag)
        kwargs["asin"] = asin
        
        request_obj = GetVariationsRequest(**kwargs)
        payload = request_obj.model_dump(by_alias=True, exclude_none=True)
        
        data = await self._request("getVariations", payload)
        return GetVariationsResponse(**data)


    async def close(self):
        """Close the underlying httpx client if we own it."""
        if self._owns_client:
            await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
