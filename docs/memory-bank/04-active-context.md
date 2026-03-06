# Active Context

## Current Focus

Promoting `amazon-creators-async` from **Beta (v0.1.2)** to **Stable (v1.0.0)**.

**Status:** In implementation → waiting for CI publish pipeline to confirm v1.0.0 on PyPI.

## Recent Decisions

### 2026-03-06 — Remove undocumented fields
Removed `merchant` from all request models and `offer_count` from `GetVariationsRequest`. These fields are not part of the official Amazon Creators API specification. Verified no test regression.

### 2026-03-06 — 100% API field coverage (v0.1.2)
Added all missing request fields (`availability`, `min_reviews_rating`, `min_saving_percent`, `properties`, `item_id_type`) and response models (`AvailabilityInfo`, `ConditionInfo`, `DealDetails`, `LoyaltyPoints`, `MerchantInfo`, `BrowseNodeInfo`, `SearchRefinements`, `VariationSummary`, etc.). Created `resources.py` with typed string constants for all operations.

### 2026-03-06 — v1.0.0 promotion criteria
Verified: 16/16 tests pass, 100% API coverage, CI/CD working, Pydantic v2 fully typed. Remaining tasks: fix badge, remove Beta classifier, document Resources module, fix hardcoded User-Agent, initialize `docs/memory-bank/`.

## Blockers

None. All blockers resolved.

## Next Action

Commit all v1.0.0 prep changes with `feat!:` prefix to trigger CI major bump `0.1.2 → 1.0.0`.
