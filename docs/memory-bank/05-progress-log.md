# Progress Log

---

## 2026-03-06 — v0.1.2: 100% API Coverage

**Completed:**
- Analyzed official Amazon Creators API docs for all 4 operations via Playwright
- Added missing `SearchItemsRequest` fields: `availability`, `min_reviews_rating` (1–4), `min_saving_percent` (1–99), `properties`
- Added `item_id_type` to `GetItemsRequest`
- Removed undocumented `merchant` field from all request models
- Removed undocumented `offer_count` from `GetVariationsRequest`
- Rewrote `models/responses.py` with 13 new models for full API response graph
- Created `resources.py` typed string constants (SearchItemsResources, GetItemsResources, GetVariationsResources, GetBrowseNodesResources, Resources)
- Updated `__init__.py` to export all public symbols
- Expanded unit tests from 3 → 16 (added coverage for all new fields + resource constants)
- Fixed CI `.gitignore` bug that was excluding `tests/` folder
- Published v0.1.2 to PyPI via automated pipeline

**Branch**: master, commit `0ab8574`

---

## 2026-03-05 — v0.1.1: Price Model Fix + Infrastructure

**Completed:**
- Fixed critical Price model to match Amazon Creators API v3.x nested structure (`money`, `savingBasis`, `savings` objects)
- Added `Money`, `Savings`, `SavingBasis` Pydantic models
- Set up GitHub Actions CI/CD: `tests.yml` (matrix 3.8–3.12) + `publish.yml` (semver bump + PyPI + GitHub Release)
- Created `scripts/bump_version.py` and `scripts/finalize_changelog.py`
- Hardened marketplace domain validation
- Published v0.1.1 to PyPI

---

## 2026-03-04 — v0.1.0: Initial Release

**Completed:**
- Initial async client with OAuth 2.0 (Cognito v2.x + LWA v3.x)
- Rate limiting (1 TPS default, configurable)
- Retry logic with exponential backoff
- Pydantic v2 request/response models for all 4 operations
- Published v0.1.0 to PyPI

---

## 2026-03-06 — v1.0.0: Stable Release

**Completed:**
- Removed Beta classifier → Production/Stable
- Fixed test badge (8/8 → 16/16)
- Documented Resources constants in README
- Fixed hardcoded User-Agent in client.py
- Fixed package name in `_pkg_version()` and PyPI version check
- Added GitHub Release automation (CHANGELOG notes + dist artifacts)
- Fixed CI import verification step (wrong module name)
- Initialized `docs/memory-bank/`
- Published via `feat!:` major bump `0.1.2 → 1.0.0`
