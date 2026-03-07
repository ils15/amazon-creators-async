# GitHub Copilot Instructions — amazon-creators-async-api

## Project Overview
Async Python wrapper for the new Amazon Creators API (OAuth 2.0).
Target: Python 3.8+, `httpx`-based, zero blocking I/O, Pydantic v2 validation.
Published on PyPI as `amazon-creators-async-api`.

---

## Architecture

```
amazon_creators_async_api/
├── client.py        # AmazonCreatorsAsyncClient — main entry point
├── auth.py          # OAuth 2.0 token handling (v2.x Cognito + v3.x LWA)
├── limiter.py       # Token-bucket RateLimiter (aiolimiter)
├── resources.py     # Endpoint resource/path constants
├── exceptions.py    # AmazonCreatorsException hierarchy
├── utils.py         # Region enum, helpers
└── models/
    ├── requests.py  # Pydantic v2 request models (SearchItems, GetItems, …)
    └── responses.py # Pydantic v2 response models
```

---

## Code Conventions

1. **All I/O is async** — never use blocking calls (`requests`, `time.sleep`, open without `aiofiles`, etc.)
2. **Type hints everywhere** — all functions must be annotated; use `from __future__ import annotations` at module top if needed
3. **Pydantic v2 models** — never return raw `dict`; always return a typed model from `models/`
4. **Errors** — raise specific exceptions from `exceptions.py`, never bare `except Exception`
5. **No hardcoded credentials** — use env vars or client constructor params
6. **Rate limiting** — always route requests through `limiter.py` (default: 1 TPS)
7. **Commit messages** — follow conventional format: `type(scope): description`
   - Valid types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`
   - Example: `feat(client): add GetVariations endpoint`

---

## Supported Endpoints

| Method | Resource |
|---|---|
| `search_items()` | `SearchItems` |
| `get_items()` | `GetItems` |
| `get_browse_nodes()` | `GetBrowseNodes` |
| `get_variations()` | `GetVariations` |

---

## Authentication

| Version | Flow |
|---|---|
| v2.x | AWS Cognito (client_credentials) |
| v3.x | Login with Amazon (LWA) |

Both handled transparently in `auth.py` with async token refresh and lock.

---

## Testing Rules

- Test runner: `pytest tests/ -q`
- Tests must be **fully async** (`pytest-asyncio`, `asyncio_mode = "auto"`)
- **No live API calls** — mock all HTTP using `httpx` mock or `pytest-mock`
- Every new endpoint method needs at least one success test and one error test

---

## Branch Strategy

```
develop  ──── day-to-day development
    │
    └── auto PR ──► master ──► CI bump + PyPI publish
```

- Develop on `develop` or feature branches merged into `develop`
- Only `master`-merges trigger PyPI releases
- The auto-PR bot reads the diff and classifies the change type automatically
  (no commit-message format required — AI reads the diff itself)

---

## Semantic Versioning (AI-driven, via auto-PR title)

When you push to `develop`, `auto-pr.yml` reads the actual **code diff** and asks
gpt-4o-mini to classify the change. The result is embedded in the auto-generated
PR title (e.g. `✨ feat: add GetVariations endpoint`). When that PR is merged
(squash-merge) to `master`, the PR title becomes the commit message and
`scripts/bump_version.py` reads it to decide the version bump.

> No conventional commit format is required in your push commits.
> The AI sets the type; the PR title is what drives the version bump.

| Classified type | Version bump | Publishes to PyPI |
|---|---|---|
| `breaking` | MAJOR | Yes |
| `feat` | MINOR | Yes |
| `fix` / `refactor` | PATCH | Yes |
| `docs` (only docs/tests changed) | — | No (no PR opened) |

---

## When Generating Code

- Prefer `async with httpx.AsyncClient() as client:` patterns
- Reuse `AmazonCreatorsAsyncClient` internal HTTP methods — do not create raw HTTP calls
- When adding a model, add it to `models/__init__.py` re-exports
- Tests go in `tests/test_client_unit.py` or `tests/test_auth_limiter_unit.py`

---

## Agent Ecosystem

Agents are defined in `.github/agents/`. Use them in Copilot Chat with `@agent-name`.

| Agent | Role | When to use |
|---|---|---|
| `@zeus` | Orchestrator | Start here for any new feature or epic |
| `@athena` | Planner | Design a feature — produces a TDD plan, never writes code |
| `@hermes` | Backend | Implement Python/async code (endpoints, models, utils) |
| `@iris` | GitHub ops | Open PRs, create releases, manage branches and issues |
| `@temis` | Reviewer | Code review, security check, coverage validation |
| `@apollo` | Discovery | Codebase exploration, docs research |
| `@mnemosyne` | Memory/Docs | Update CHANGELOG, README, memory bank |
| `@hephaestus` | Hotfix | Emergency fixes directly to master |
| `@ra` | Infra/CI | GitHub Actions, Docker, deployment scripts |
| `@maat` | Data/DB | Data models, schema, serialization |

### Release flow with agents

```
# 1. Push to develop (normal push)
#    → auto-pr.yml creates PR develop → master automatically
#    → @iris can also create the PR manually if needed

# 2. To plan a new feature before starting:
@athena plan: <describe the feature>

# 3. To open / update the release PR manually:
@iris create PR from develop to master for release

# 4. To review the PR before merging:
@temis review PR #<number>
```
