# Components — amazon-creators-async

## `AmazonCreatorsAsyncClient` (client.py)

**Role**: Top-level entry point. Instantiated once per app; thread-safe and coroutine-safe.

**Constructor params**:
| Param | Type | Default | Description |
|---|---|---|---|
| `credential_id` | str | required | OAuth app client ID |
| `credential_secret` | str | required | OAuth app secret |
| `marketplace` | str | `www.amazon.com.br` | Target domain (validated against `www.amazon.*`) |
| `partner_tag` | str | required | Associate tracking tag |
| `region` | Region | NORTH_AMERICA | AWS region enum |
| `version` | str | auto | `"2.x"` or `"3.x"` from Creators Console |
| `rate_limit_tps` | float | 1.0 | Requests per second |
| `max_retries` | int | 2 | Max retry attempts per request |
| `retry_backoff_seconds` | float | 0.5 | Initial backoff delay (doubles each retry) |
| `client` | httpx.AsyncClient | auto | Inject external HTTP client (for connection pooling) |

**Methods**: `search_items()`, `get_items()`, `get_variations()`, `get_browse_nodes()`, `close()`, async context manager `__aenter__`/`__aexit__`.

---

## `AuthManager` (auth.py)

**Role**: Obtains and caches OAuth 2.0 bearer tokens. Handles both v2.x (Cognito) and v3.x (LWA).

**Key behavior**:
- Tokens cached in memory with `expires_at - 60s` buffer
- `asyncio.Lock` prevents concurrent refresh storms  
- Token type auto-detected from `version` string

---

## `RateLimiter` (limiter.py)

**Role**: Enforces TPS limits using `aiolimiter.AsyncLimiter`.

**Key behavior**:
- Converts user TPS (e.g. `0.5`) to `period = 1.0 / tps` seconds
- Raises `ValueError` for `tps <= 0`
- `acquire()` is async; suspends coroutine until slot is available

---

## Request Models (models/requests.py)

All subclass `BaseModel` with `alias_generator` for `snake_case` → `lowerCamelCase`.

| Model | Operation | Key fields |
|---|---|---|
| `SearchItemsRequest` | SearchItems | keywords, browse_node_id, brand, availability, min_reviews_rating (1–4), min_saving_percent (1–99), item_count, properties |
| `GetItemsRequest` | GetItems | item_ids (list), item_id_type (default "ASIN") |
| `GetVariationsRequest` | GetVariations | asin, variation_count, variation_page |
| `GetBrowseNodesRequest` | GetBrowseNodes | browse_node_ids (list) |

---

## Response Models (models/responses.py)

Full graph of Pydantic models covering every field in the official API:

```
SearchItemsResponse
  └── search_result: SearchResult
        ├── items: List[Item]
        │     ├── item_info: ItemInfo  (11 fields: title, features, classifications, ...)
        │     ├── offers_v2: OffersV2
        │     │     └── listings: List[Listing]
        │     │           ├── price: Price (money, savings, saving_basis, price_per_unit)
        │     │           ├── availability: AvailabilityInfo
        │     │           ├── condition: ConditionInfo
        │     │           ├── deal_details: DealDetails
        │     │           ├── loyalty_points: LoyaltyPoints
        │     │           └── merchant_info: MerchantInfo
        │     ├── browse_node_info: BrowseNodeInfo
        │     │     └── browse_nodes: List[ItemBrowseNode]  (recursive via ancestor)
        │     └── parent_asin: str
        └── search_refinements: SearchRefinements

GetVariationsResponse
  └── variations_result: VariationsResult
        ├── items: List[Item]
        └── variation_summary: VariationSummary

GetBrowseNodesResponse
  └── browse_nodes_result: BrowseNodesResult
        └── browse_nodes: List[BrowseNode]
              ├── sales_rank: List[SalesRank]
              └── ancestor: BrowseNode (recursive)
```

---

## Resource Constants (resources.py)

Typed string constants. One class per operation + `Resources` flat superclass:

- `SearchItemsResources` — ~30 constants
- `GetItemsResources` — same ItemInfo/Offers/Images set
- `GetVariationsResources` — adds `VARIATION_SUMMARY_*`
- `GetBrowseNodesResources` — browse node specific
- `Resources` — inherits all of the above (flat namespace)

---

## Exceptions (exceptions.py)

```
AmazonCreatorsException (base)
  ├── AuthenticationError   — token fetch/refresh failure
  ├── RateLimitError        — HTTP 429 after retries
  ├── InvalidRequestError   — HTTP 400
  └── APIError              — HTTP 5xx, network, or unknown
```

---

## Utils (utils.py)

- `Region` enum: `NORTH_AMERICA`, `EUROPE`, `FAR_EAST`
- `get_api_endpoint(region)` → base URL string
- `validate_marketplace(domain)` → raises ValueError if not `www.amazon.*`
- `get_version_for_region(region)` → default API version string per region
