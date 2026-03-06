# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2026-03-06
### Added
- Automated release tooling with `scripts/bump_version.py` and `scripts/finalize_changelog.py`.
- Automatic semantic version synchronization in package metadata (`pyproject.toml` and `amazon_creators_async/__init__.py`).
- `resources.py`: new module with typed string constants for every official resource of all four operations (`SearchItemsResources`, `GetItemsResources`, `GetVariationsResources`, `GetBrowseNodesResources`, flat `Resources` superclass).
- `SearchItemsRequest`: new fields `availability`, `min_reviews_rating` (1–4), `min_saving_percent` (1–99), `properties`.
- `GetItemsRequest`: new field `item_id_type` (default `"ASIN"`).
- Response models: `AvailabilityInfo`, `ConditionInfo`, `DealDetails`, `LoyaltyPoints`, `MerchantInfo`, `SalesRank`, `ItemBrowseNode`, `BrowseNodeInfo`, `WebsiteSalesRank`, `SearchRefinementBin`, `SearchRefinement`, `SearchRefinements`, `VariationSummary`.
- `Listing`: typed `availability` (`AvailabilityInfo`), `condition` (`ConditionInfo`), plus `deal_details`, `loyalty_points`, `merchant_info`, `type` fields.
- `Price`: new `price_per_unit` field (`Money`).
- `ItemInfo`: expanded to all 11 official fields (byLineInfo, classifications, contentInfo, contentRating, externalIds, features, manufactureInfo, productInfo, technicalInfo, title, tradeInInfo).
- `Item`: new `browse_node_info` (`BrowseNodeInfo`) and `parent_asin` fields.
- `SearchResult`: new `search_refinements` field.
- `VariationsResult`: new `variation_summary` field.
- `BrowseNode`: new `sales_rank` field.
- `__init__.py`: exports now include all request models, all response models, all resource classes, and all five exception types.

### Changed
- PyPI publish workflow now runs on `master` pushes/merges with automated build, validation, and publish steps.
- Release pipeline now finalizes changelog entries by converting `## [Unreleased]` into `## [X.Y.Z] - YYYY-MM-DD` during release.
- Test workflow now includes `develop` branch for push and pull request validation.
- Marketplace domain validation was hardened to accept only valid `www.amazon.*` patterns.

### Removed
- **BREAKING**: `merchant` field removed from `SearchItemsRequest`, `GetItemsRequest`, and `GetVariationsRequest` — field is not part of the official Creators API specification.
- **BREAKING**: `offer_count` field removed from `GetVariationsRequest` — field is not part of the official Creators API specification.

### Fixed
- Reduced risk of sensitive data leakage by sanitizing and truncating API/auth error payloads before raising exceptions.
- Removed accidental debug artifact from repository (`debug_response.py`).

## [0.1.1] - 2026-03-05
### Changed
- Standardized project contact metadata to `contato@ofertachina.com.br` and official contact URL.
- Updated README support section with commercial contact and website.
- Improved release metadata consistency for PyPI packaging.

### Fixed
- **CRITICAL**: Corrected Price model to match Amazon Creators API v3.x nested structure
  - Price now correctly parses `money`, `savingBasis`, and `savings` nested objects
  - Added `Money`, `Savings`, and `SavingBasis` Pydantic models for proper type safety
  - Access current price via: `listing.price.money.display_amount` (was: `price.display_amount`)
  - Access savings via: `listing.price.savings.money.display_amount`
  - Old flat structure (`price.amount`, `price.display_amount`) is **removed**
- Added `is_buy_box_winner` and `violates_map` fields to `Listing` model
- Corrected license contact domain from `.com` to `.com.br`.

### Documentation
- Added `PRICE_STRUCTURE.md` with comprehensive price access examples and JSON structure
- Updated README with "Accessing Price Information" section showing nested price usage
- Updated test examples to demonstrate correct price access pattern

## [0.1.0] - 2026-03-05
### Added
- Initial release of the `amazon-creators-async` wrapper.
- Full OAuth 2.0 support (Cognito v2.x and LWA v3.x credentials).
- Native asynchronous core leveraging `httpx`.
- Configurable Rate Limiting defaulting to 1 TPS via `aiolimiter`.
- Complete Pydantic v2 models mapping Python `snake_case` to Amazon API `lowerCamelCase`.
- Endpoints: `search_items`, `get_items`, `get_browse_nodes`, `get_variations`.
- PyPI release metadata (`pyproject.toml`).
- Examples and documentation (README, QUICK_START, CONTRIBUTING).

## [0.2.0] - 2026-03-06
### Changed
- Maintenance release.

