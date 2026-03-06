# Tech Context — amazon-creators-async

## Runtime Stack

| Layer | Technology | Version |
|---|---|---|
| Language | Python | 3.8+ |
| HTTP client | `httpx` | >=0.24.0 |
| Validation | `pydantic` | >=2.0.0 |
| Rate limiting | `aiolimiter` | >=1.1.0 |
| Build system | `hatchling` | (latest) |

## Dev Dependencies

| Tool | Purpose |
|---|---|
| `pytest` >=8.0.0 | Test runner |
| `pytest-asyncio` >=0.23.0 | `asyncio_mode = "auto"` for async tests |
| `twine` | PyPI upload + dist validation |
| `build` | `python -m build` → `.whl` + `.tar.gz` |

## Setup Commands

```bash
# Install in editable mode with dev extras
pip install -e '.[dev]'

# Run unit tests
python -m pytest tests/ -q

# Build distribution
python -m build

# Validate distribution
twine check dist/*

# Publish to PyPI (use token from .env)
twine upload dist/* -u __token__ -p <PYPI_TOKEN>
```

## CI/CD (GitHub Actions)

### `tests.yml`
- Trigger: push/PR to `master` or `develop`
- Matrix: Python 3.9, 3.10, 3.11, 3.12
- Steps: checkout → setup Python → `pip install -e '.[dev]'` → `pytest tests/ -q`

### `publish.yml`
- Trigger: push to `master`
- Steps:
  1. Run tests (must pass)
  2. `scripts/bump_version.py` — reads commit message, bumps semver in `pyproject.toml` + `__init__.py`:
     - `feat!:` or `breaking change` → **major** (e.g. `0.1.2` → `1.0.0`)
     - `feat:` / `feat(...)` → **minor**
     - `fix:`/`refactor:`/`perf:` → **patch**
     - Default → patch
  3. `scripts/finalize_changelog.py` — converts `## [Unreleased]` → `## [X.Y.Z] - YYYY-MM-DD`
  4. Commit `chore(release): vX.Y.Z` (skipped by bump script to prevent loop)
  5. `python -m build && twine upload`

## Branching Strategy

- `master` — production releases. Every push triggers publish workflow.
- `develop` — default branch for active development + CI tests.
- Feature branches → PR → `develop` → merge to `master` when ready to release.

## Environment Variables

| Variable | Used By | Purpose |
|---|---|---|
| `AMAZON_CREDENTIAL_ID` | integration tests | OAuth app client ID |
| `AMAZON_CREDENTIAL_SECRET` | integration tests | OAuth app secret |
| `AMAZON_PARTNER_TAG` | integration tests | Associate tracking tag |
| `AMAZON_VERSION` | integration tests | API version (e.g. `"3.1"`) |
| `PYPI_API_TOKEN` | publish.yml | PyPI upload token (GitHub Secret) |

## Repository Layout

```
amazon_creators_async/
├── __init__.py           ← public exports + __version__
├── client.py             ← AmazonCreatorsAsyncClient
├── auth.py               ← AuthManager (Cognito + LWA)
├── limiter.py            ← RateLimiter
├── exceptions.py         ← 5 exception types
├── utils.py              ← Region enum, validators
├── resources.py          ← typed resource string constants
└── models/
    ├── requests.py       ← 4 Pydantic request models
    └── responses.py      ← full response model graph (~20 models)
tests/
├── test_client_unit.py   ← 13 tests (client, request, response, resources)
└── test_auth_limiter_unit.py ← 3 tests (auth, rate limiter)
scripts/
├── bump_version.py       ← CI semver bumper
└── finalize_changelog.py ← CI changelog finalizer
docs/memory-bank/         ← Mnemosyne documentation
.github/workflows/
├── tests.yml
└── publish.yml
```
