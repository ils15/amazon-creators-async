# Notes & ADR Index

| ID | Title | Date | File |
|---|---|---|---|
| NOTE0001 | Remove undocumented API fields (merchant, offer_count) | 2026-03-06 | NOTE0001-remove-undocumented-fields.md |

---

## NOTE0001 — Remove Undocumented API Fields

**Date**: 2026-03-06  
**Decision**: Remove `merchant` from `SearchItemsRequest`, `GetItemsRequest`, `GetVariationsRequest`, and `offer_count` from `GetVariationsRequest`.  
**Reason**: These fields do not appear in the official Amazon Creators API documentation. Keeping undocumented fields risks unexpected API behavior and misleads users.  
**Verification**: Checked official docs via Playwright on `affiliate-program.amazon.com`. No test regression (unit tests don't use these fields).
