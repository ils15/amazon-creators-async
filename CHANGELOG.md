# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-03-05
### Changed
- Standardized project contact metadata to `contato@ofertachina.com.br` and official contact URL.
- Updated README support section with commercial contact and website.
- Improved release metadata consistency for PyPI packaging.

### Fixed
- Corrected license contact domain from `.com` to `.com.br`.

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
