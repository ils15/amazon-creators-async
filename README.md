# Async Amazon Creators API (OAuth 2.0)

[![PyPI version](https://badge.fury.io/py/amazon-creators-async.svg)](https://badge.fury.io/py/amazon-creators-async)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/amazon-creators-async.svg)](https://pypi.org/project/amazon-creators-async/)

A modern, high-performance, asynchronous Python wrapper for the **Amazon Creators API** (the replacement for the old Product Advertising API 5.0). 

It fully supports the new **OAuth 2.0** authentication flow, including `v3.1` (Login with Amazon - LWA) credentials, and handles the strict rate limitations automatically to protect your account.

## Features

- ⚡️ **Fully Asynchronous**: Built directly on `httpx` and `asyncio` for maximum performance.
- 🔐 **OAuth 2.0 Native**: Automatic token fetching, caching, and renewal before expiration. Supports Cognito (v2.x) and LWA (v3.x).
- 🚦 **Built-in Rate Limiting**: Uses `aiolimiter` to ensure you never exceed Amazon's 1 TPS (Transactions Per Second) limit by default, preventing `429 TooManyRequests` bans.
- 📦 **Pydantic Validation**: Full request and response validation using Pydantic v2.
- 🐪 **Auto CamelCase mapping**: You write Pythonic `snake_case`, the library talks to Amazon in their required `lowerCamelCase`.
- 🛠️ **Full API Coverage**: `SearchItems`, `GetItems`, `GetBrowseNodes`, and `GetVariations`.

## Installation

```bash
pip install amazon-creators-async
```

## Quick Start

```python
import asyncio
from amazon-creators-async import AmazonCreatorsAsyncClient, Region

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

## Documentation
- [Amazon Creators API Official Docs](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction)
- [Quick Start Guide](QUICK_START.md)
- [Contributing](CONTRIBUTING.md)

## License
MIT License. See [LICENSE](LICENSE) for details.
