# Async Amazon Creators API (OAuth 2.0)

[![PyPI version](https://img.shields.io/pypi/v/amazon-creators-async.svg)](https://pypi.org/project/amazon-creators-async/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests Passing](https://img.shields.io/badge/Tests-8%2F8%20Passing-brightgreen)](#)
[![Code Quality](https://img.shields.io/badge/Code%20Quality-Pydantic%20Validated-blue)](#)

A modern, high-performance, asynchronous Python wrapper for the **Amazon Creators API** (successor to Product Advertising API 5.0). 

✨ **Production-ready** with full OAuth 2.0 support (v2.x Cognito & v3.x LWA), automatic rate limiting, token refresh, retry logic, and comprehensive input validation using Pydantic v2.

## Features

- ⚡️ **Fully Asynchronous**: Built on `httpx` + `asyncio` for maximum performance and throughput.
- 🔐 **OAuth 2.0 Native**: Automatic token fetching, caching, renewal with concurrent-safe locking. Cognito (v2.x) and LWA (v3.x) auto-negotiation.
- 🚦 **Intelligent Rate Limiting**: Uses `aiolimiter` (default 1 TPS). Respects fractional TPS (e.g., 0.5 TPS = 1 req every 2s). Prevents Amazon account throttling/bans.
- 🔄 **Automatic Retry**: Exponential backoff for network errors (up to 2 retries). Respect `Retry-After` headers on 429 responses. Configurable backoff multiplier.
- 📦 **Pydantic v2 Validation**: Full request/response validation. Rejects invalid ASINs, missing search criteria, empty IDs lists at instantiation (fail-fast).
- 🐪 **Auto CamelCase Mapping**: Write Python `snake_case`, library sends Amazon's `lowerCamelCase` JSON automatically.
- 🛠️ **Full API Coverage**: `SearchItems`, `GetItems`, `GetBrowseNodes`, `GetVariations`.
- 💼 **Production-Ready**: Thread-safe token refresh, resource context managers, comprehensive error handling.

## Installation

```bash
pip install amazon-creators-async
```

## Quick Start

```python
import asyncio
from amazon_creators_async import AmazonCreatorsAsyncClient, Region

async def main():
    async with AmazonCreatorsAsyncClient(
        credential_id="YOUR_APP_ID",
        credential_secret="YOUR_APP_SECRET",
        partner_tag="yourtag-20",       # Your Amazon Associate tag
        marketplace="www.amazon.com",   # Target marketplace domain
        region=Region.NORTH_AMERICA,    # Standard region (includes Brazil)
        version="3.1"                   # Version from your Creator Console
    ) as client:
    
        # 1. Search for products
        search_res = await client.search_items(
            keywords="Mechanical Keyboard",
            item_count=5, # Number of items to return
            resources=[
                "itemInfo.title",
                "offersV2.listings.price",
                "images.primary.large"
            ]
        )
        
        for item in search_res.search_result.items:
            print(f"ASIN: {item.asin}")
            if item.item_info and item.item_info.title:
                print(f"Title: {item.item_info.title.get('displayValue')}")
            
        print("-" * 20)

        # 2. Get specific items by ASIN
        get_res = await client.get_items(
            item_ids=["B07XQXZXJC", "B08FJMVZX6"],
            resources=["itemInfo.features"]
        )
        
        for item in get_res.items_result.items:
             print(f"Features for {item.asin}:")
             if item.item_info and item.item_info.features:
                 for feature in item.item_info.features.get('displayValues', []):
                     print(f" - {feature}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Available Resources
The Amazon API requires you to specify the `resources` you want returned to minimize payload size. We use the updated **lowerCamelCase** format required by v3.x of the API.
Common Examples:
- `itemInfo.title`
- `offersV2.listings.price`
- `images.primary.small`
- `images.variants.large`
- `itemInfo.features`
- `browseNodeInfo.browseNodes`

## Rate Limiting (Throttling)

Amazon imposes strict API limitations. Exceeding them regularly can lead to your account being blocked.
*   **Default Limit**: 1 request per second (TPS).
*   **Library Behavior**: The `AmazonCreatorsAsyncClient` handles this automatically. If you fire 10 requests at once using `asyncio.gather()`, the built-in limiter will process exactly 1 per second. 
*   **Custom Limits**: If your account has a higher tier limit, you can adjust the TPS:
    ```python
    AmazonCreatorsAsyncClient(..., rate_limit_tps=5.0) # For accounts with 5 TPS
    ```

## Authentication Versions

The library automatically negotiates endpoints based on the `version` passed during initialization:
- **v2.x (e.g., "2.1")**: Uses Cognito endpoints with Basic Auth forms.
- **v3.x (e.g., "3.1")**: Uses Login with Amazon (LWA) endpoints with JSON bodies.

## Error Handling

The library provides typed exceptions for easier error recovery:

```python
from amazon_creators_async import (
    AmazonCreatorsAsyncClient, 
    AuthenticationError, 
    RateLimitError, 
    InvalidRequestError,
    APIError
)

async with AmazonCreatorsAsyncClient(...) as client:
    try:
        results = await client.search_items(keywords="laptop")
    except AuthenticationError as e:
        print(f"Token refresh failed: {e}")
    except RateLimitError as e:
        print(f"Hit rate limit (429). Exponential backoff already attempted.")
    except InvalidRequestError as e:
        print(f"Invalid request (400): {e}")
    except APIError as e:
        print(f"API error ({e.status_code}): {e}")
```

**Exception Hierarchy:**
- `AmazonCreatorsException` (base)
  - `AuthenticationError` – OAuth 2.0 token fetch/refresh failed
  - `RateLimitError` – HTTP 429 after max retries
  - `InvalidRequestError` – HTTP 400 (validation typically catches these first)
  - `APIError` – Generic HTTP 5xx, connection errors, or unknown status codes

## Advanced Usage

### Fractional Rate Limits (Low-Frequency Queries)
```python
# For development accounts or 0.5 TPS tier: 1 request every 2 seconds
client = AmazonCreatorsAsyncClient(
    ...,
    rate_limit_tps=0.5  # or any float > 0
)
```

### Custom Retry Strategy
```python
# Increase retries and backoff for unreliable networks
client = AmazonCreatorsAsyncClient(
    ...,
    max_retries=4,              # Total attempts = 5
    retry_backoff_seconds=1.0   # Starts at 1s, doubles each retry
)
```

### Reusing HTTP Connection Pool (FastAPI, etc.)
```python
import httpx
from fastapi import FastAPI

app = FastAPI()
http_client = httpx.AsyncClient(timeout=30.0)

# Share client across requests to reuse TCP connections
amazon_client = AmazonCreatorsAsyncClient(
    ...,
    client=http_client
)

@app.on_event("shutdown")
async def shutdown():
    await amazon_client.close()  # Closes internal HTTP client only if you passed one
    await http_client.aclose()   # Your client
```

## Troubleshooting

| **Issue** | **Cause** | **Solution** |
|-----------|-----------|------------|
| `AuthenticationError: Failed to obtain token` | Invalid credentials or expired app registration | Verify `credential_id`, `credential_secret` in Amazon Creators Console. Ensure `version` matches your console tier. |
| `RateLimitError: Rate limit exceeded` | Fired requests faster than TPS limit. | Increase `rate_limit_tps` if your account tier supports it, or reduce concurrent requests. Library retries automatically with exponential backoff. |
| `InvalidRequestError: Invalid request` | Missing required fields in request. | `ValidationError` is raised by Pydantic before HTTP call. Check that your `search_items()` call has at least one search criterion (keywords, brand, browse_node_id, etc.). |
| `APIError: API Error (500)` | Amazon service temporary outage. | Automatic retry with exponential backoff is applied. If persists, check [Amazon Status Page](https://status.aws.amazon.com). |
| `ModuleNotFoundError: No module named 'aiolimiter'` | Dependencies not installed. | Run `pip install amazon-creators-async[dev]` or `pip install -e .[dev]` if developing. |

## Development & Testing

Install extras:
```bash
pip install amazon-creators-async[dev]  # pytest, pytest-asyncio
```

Run unit tests (no credentials needed):
```bash
pytest tests/ -q
```

Run integration tests (requires `.env` with `AMAZON_CREDENTIAL_ID`, `AMAZON_CREDENTIAL_SECRET`, `AMAZON_PARTNER_TAG`):
```bash
pytest test_client.py test_extra_endpoints.py -q
```

Build & validate distribution:
```bash
python -m build && twine check dist/*
``` 

## Documentation

- 🔗 [Amazon Creators API Official Docs](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction)
- 📖 [Quick Start Guide](QUICK_START.md) – 5-minute setup with FastAPI example
- 🤝 [Contributing Guide](CONTRIBUTING.md) – How to submit PRs and report issues
- 📋 [Full API Reference](https://pypi.org/project/amazon-creators-async/) on PyPI

## Support & Community

- **Report bugs** via [GitHub Issues](https://github.com/ils15/amazon-creators-async/issues)
- **Discuss features** in [GitHub Discussions](https://github.com/ils15/amazon-creators-async)
- **Commercial contact**: `contato@ofertachina.com.br`
- **Website**: [ofertachina.com.br](https://ofertachina.com.br)
- **Check status** of the Amazon Creators API at [AWS Health Dashboard](https://status.aws.amazon.com)

## License

MIT License. See [LICENSE](LICENSE) for full text.

---

**Built with ❤️ for Amazon Associates and content creators**
