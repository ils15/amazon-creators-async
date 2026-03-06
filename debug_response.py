import asyncio
import os
import json

from amazon_creators_async import AmazonCreatorsAsyncClient
from amazon_creators_async.utils import Region

def load_env_file():
    if os.path.exists(".env"):
        with open(".env") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    if "#" in v:
                        v = v.split("#", 1)[0]
                    os.environ[k.strip()] = v.strip().strip('"\'')

async def debug():
    load_env_file()
    
    credential_id = os.getenv("AMAZON_CREDENTIAL_ID")
    credential_secret = os.getenv("AMAZON_CREDENTIAL_SECRET")
    partner_tag = os.getenv("AMAZON_PARTNER_TAG")
    version = os.getenv("AMAZON_VERSION", "3.1")

    async with AmazonCreatorsAsyncClient(
        credential_id=credential_id,
        credential_secret=credential_secret,
        partner_tag=partner_tag,
        marketplace="www.amazon.com.br",
        region=Region.NORTH_AMERICA,
        version=version,    
        rate_limit_tps=1.0              
    ) as client:
        
        # Patch the _request method to also print the raw response
        original_request = client._request
        
        async def patched_request(operation, payload):
            result = await original_request(operation, payload)
            print("=" * 80)
            print(f"RAW API RESPONSE for {operation}:")
            print("=" * 80)
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print("=" * 80)
            return result
        
        client._request = patched_request
        
        try:
            print("Testing GetItems...")
            result = await client.get_items(
                item_ids=["B0DCW6W5BK"],
                resources=[
                    "images.primary.small", 
                    "itemInfo.title",
                    "offersV2.listings.price"
                ]
            )
            
            print("\n\nParsed Pydantic Model:")
            print(result.model_dump(exclude_none=True))
            
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug())
