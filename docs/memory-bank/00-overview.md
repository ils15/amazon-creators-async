# Project Overview — amazon-creators-async

## What Is This?

`amazon-creators-async` is a production-ready asynchronous Python wrapper for the **Amazon Creators API** (the OAuth 2.0-based successor to the Product Advertising API 5.0).

It is published on PyPI and maintained by **OfertaChina** (`contato@ofertachina.com.br`).

## Purpose

Enables Python developers and Amazon Associates to query the Amazon Creators API — searching products, fetching item details, exploring browse nodes, and retrieving product variations — in a fully async, type-safe, rate-limited manner.

## Current Version

| Field | Value |
|---|---|
| PyPI package | `amazon-creators-async` |
| Latest PyPI | `0.1.2` (promoted to `1.0.0` stable next) |
| Status | Production/Stable (after v1.0.0 release) |
| License | MIT |
| Python | 3.8+ |

## Supported Operations

| Operation | Client Method | Description |
|---|---|---|
| SearchItems | `client.search_items()` | Full-text and faceted product search |
| GetItems | `client.get_items()` | Fetch one or more ASINs by ID |
| GetVariations | `client.get_variations()` | Product variations for a parent ASIN |
| GetBrowseNodes | `client.get_browse_nodes()` | Taxonomy/category tree navigation |

## Key Differentiators

- Fully async (`httpx` + `asyncio`) — no thread blocking
- Type-safe: Pydantic v2 models for all requests and responses
- 100% API field coverage — matches official Creators API docs exactly
- Typed resource constants (`SearchItemsResources`, etc.) for IDE autocomplete
- Automatic OAuth 2.0 — Cognito (v2.x) and LWA (v3.x) auto-negotiation
- Rate limiting (1 TPS default, configurable) with fractional TPS support
- Exponential backoff retry (2 retries, 0.5 s initial delay)
