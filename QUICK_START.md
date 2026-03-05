# Quick Start: amazon-creators-async

Get up and running with the Amazon Creators API in 5 minutes!

## Requirements
* An approved **Amazon Associates** account.
* A registered application in the **Amazon Creators Console**.
* Your `credential_id`, `credential_secret`, and `partner_tag`.

## 1. Installation

```bash
pip install amazon-creators-async
```

## 2. Basic Setup (FastAPI Example)

Here is how you would use this library inside a modern async framework like FastAPI to prevent thread-blocking while waiting for Amazon's API:

```python
from fastapi import FastAPI
from amazon_creators_async import AmazonCreatorsAsyncClient, Region

app = FastAPI()

# Usually, you'd load these from environment variables (.env)
CREATOR_ID = "amzn1.application..."
CREATOR_SECRET = "amzn1.oa2-cs..."
PARTNER_TAG = "mywebsite-20"

# Note: In production, instantiate this client once on startup (Lifespan event) 
# and share it across requests to reuse the connection pool and rate limiter.
client = AmazonCreatorsAsyncClient(
    credential_id=CREATOR_ID,
    credential_secret=CREATOR_SECRET,
    partner_tag=PARTNER_TAG,
    marketplace="www.amazon.com",
    region=Region.NORTH_AMERICA,
    version="3.1" # Find your version in the Creators Console
)

@app.get("/search/{keyword}")
async def search_amazon(keyword: str):
    response = await client.search_items(
        keywords=keyword,
        item_count=5,
        resources=[
            "itemInfo.title",
            "offersV2.listings.price",
            "images.primary.large"
        ]
    )
    
    # Map the response into a clean JSON output
    results = []
    for item in response.search_result.items:
        title = item.item_info.title.get('displayValue', 'No title') if item.item_info and item.item_info.title else "No title"
        
        price = "Out of Stock"
        if item.offers_v2 and item.offers_v2.listings:
            price = item.offers_v2.listings[0].price.display_amount

        results.append({
            "asin": item.asin,
            "title": title,
            "price": price
        })
        
    return {"results": results}

@app.on_event("shutdown")
async def shutdown_event():
    # Always close the client cleanly
    await client.close()
```

## 3. Parallel Execution (Safe Throttling)

If you need to query multiple distinct ASINs or categories at once, you can safely use `asyncio.gather`.
Our built-in `RateLimiter` ensures you don't violate the 1 TPS limit:

```python
import asyncio

async def parallel_fetch():
    # Assuming `client` is already initialized
    
    # These three calls are fired immediately
    tasks = [
        client.get_items(item_ids=["B07XQXZXJC"], resources=["itemInfo.title"]),
        client.get_items(item_ids=["B08FJMVZX6"], resources=["itemInfo.title"]),
        client.get_items(item_ids=["B09B8VGCR8"], resources=["itemInfo.title"])
    ]
    
    # The client will space them out (1 request per second) automatically!
    results = await asyncio.gather(*tasks)
    return results
```
