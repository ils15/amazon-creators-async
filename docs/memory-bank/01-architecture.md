# Architecture — amazon-creators-async

## High-Level Design

```
User Code
    │
    ▼
AmazonCreatorsAsyncClient          ← orchestrator (client.py)
    ├── AuthManager                ← OAuth 2.0 token lifecycle (auth.py)
    │       ├── v2.x: AWS Cognito (Basic Auth form POST)
    │       └── v3.x: Login with Amazon — LWA (JSON POST)
    ├── RateLimiter                ← aiolimiter token bucket (limiter.py)
    ├── Pydantic Request Models    ← models/requests.py (serialization + validation)
    ├── httpx.AsyncClient          ← shared HTTP connection pool
    └── Pydantic Response Models   ← models/responses.py (parsing + validation)
```

## Request Lifecycle

```
client.search_items(keywords="laptop", ...)
    │
    ├─ 1. Build SearchItemsRequest (Pydantic validates, serializes snake_case → lowerCamelCase)
    ├─ 2. client._request("searchItems", payload)
    │       ├─ a. await RateLimiter.acquire()   (blocks until TPS slot available)
    │       ├─ b. await AuthManager.get_valid_token()   (returns cached or refreshed token)
    │       ├─ c. httpx POST to endpoint/{operation}
    │       ├─ d. On success (200): parse response JSON → SearchItemsResponse
    │       └─ e. On error: raise typed exception + exponential backoff retry
    └─ Returns SearchItemsResponse
```

## Authentication Flow

```
AuthManager.get_valid_token()
    │
    ├── Token valid? → return cached token
    │
    └── Token expired?
            ├── Acquire asyncio.Lock  (prevents parallel refresh stampedes)
            ├── Re-check (another coroutine may have refreshed while we waited)
            ├── Fetch new token:
            │       ├── v2.x: POST to Cognito /oauth2/token with Basic Auth + form body
            │       └── v3.x: POST to LWA /auth/o2/token with JSON body
            ├── Cache token + expiry - 60 s buffer
            └── Release Lock
```

## Module Boundaries

| Module | Responsibility | External deps |
|---|---|---|
| `client.py` | Orchestrate request/response, retry, error mapping | httpx, pydantic |
| `auth.py` | Token fetch + refresh + caching, async-safe lock | httpx |
| `limiter.py` | TPS enforcement, fractional rate support | aiolimiter |
| `models/requests.py` | Pydantic input models, validators, camelCase aliasing | pydantic |
| `models/responses.py` | Pydantic output models, full API response graph | pydantic |
| `resources.py` | Typed string constants for `resources` parameter | — |
| `exceptions.py` | Exception hierarchy (5 types) | — |
| `utils.py` | Region enum, endpoint mapping, marketplace validator | — |

## Error Mapping

| HTTP Status | Exception Class |
|---|---|
| 400 | `InvalidRequestError` |
| 401 / 403 | `AuthenticationError` |
| 429 | `RateLimitError` |
| 5xx / network | `APIError` |
| Any | `AmazonCreatorsException` (base) |
