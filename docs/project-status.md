# Project Status

_Last updated: 2026-09-27_

## Current State

The MVP is functional and portfolio-ready.

Implemented:

- company collection by city and category;
- safe demo mode and live 2GIS API mode;
- PostgreSQL persistence;
- parser job history;
- duplicate detection;
- enrichment source queue;
- manually verified contacts;
- CSV export;
- terminal reports;
- setup, security, architecture, and demo documentation.

CSV export keeps canonical source values separate from spreadsheet-safety formatting so deduplication remains stable while spreadsheet output stays safe to review.

A small export regression fixture should cover formula-like text and URL identity together, ensuring spreadsheet escaping cannot affect canonical deduplication keys.

## What Is Working

The current pipeline is:

```text
city + category
      ↓
2GIS API / demo dataset
      ↓
normalization and duplicate checks
      ↓
PostgreSQL
      ↓
enrichment queue
      ↓
manual contact verification
      ↓
CSV export
```

## Current Limitation

Phone, website, and email fields may be unavailable when the connected 2GIS API plan does not include contact data.

The project handles this by preparing enrichment links and supporting manual verification instead of attempting aggressive scraping or bypass techniques.

## Next Practical Milestone

The next useful release should focus on improving the existing project instead of creating a separate duplicate CRM backend.

Priority:

1. add lead status management;
2. add notes for each company;
3. improve CSV import/export flow;
4. add a lightweight dashboard;
5. prepare integration with n8n and external CRM systems;
6. add automated tests for duplicate handling and database writes;
7. add an export regression test confirming spreadsheet escaping runs only after canonicalization and deduplication;
8. add a deterministic export-order regression check: repeated exports of the same canonical demo inputs should have identical row order, quoting, line endings, and CSV bytes.
9. document a dry-run export check that writes only to a temporary output path.

## Portfolio Positioning

This project demonstrates:

- Python application structure;
- PostgreSQL schema design;
- API integration;
- data normalization;
- duplicate prevention;
- enrichment workflow design;
- secure configuration practices;
- business-oriented documentation.

- Record the source date and generating commit beside each portfolio CSV so exported examples remain traceable.

- Verify portfolio CSV files open consistently as UTF-8 and retain deterministic headers without machine-specific metadata.

- Verify source URL normalization is deterministic and preserves distinctions required for contact provenance.

- Verify CSV quoting preserves synthetic values containing commas, quotes, or line breaks during export and re-import.

- Record the demo command parameters and source commit beside each published export so results can be reproduced.

- Document the fields removed from demo exports so portfolio samples remain free of contact data and unstable identifiers.

- Document the deterministic sort order used for demo exports so regenerated portfolio samples produce reviewable diffs.

- Document bounded retry and backoff behavior for source requests without exposing proxy or credential details.

- Document the pagination stop condition and a bounded page limit so demo runs cannot continue indefinitely.

- Document cache lifetime and invalidation rules used by reproducible demo runs.

- Document category-query normalization for whitespace and letter case so equivalent demo inputs remain reproducible.

- Record an output-schema version beside published demo exports so downstream examples remain interpretable.

- Document bounded concurrency and rate-limit handling for reproducible, source-friendly demo runs.

- Validate required export columns before publishing a demo dataset so downstream examples remain reproducible.

- Document how empty search results are represented so exports remain structurally valid and easy to audit.

- Document the audit fields recorded with each export, including query parameters, generation time, and schema version.

- Document how duplicate organizations are identified when source records contain formatting differences in names or addresses.

- Document how interrupted exports are marked so partial files cannot be mistaken for completed datasets.

- Document how source response timestamps are preserved to support freshness checks in exported datasets.

- Document how parser warnings are summarized separately from fatal errors in an export run report.

- Document how exports identify records with missing optional fields without treating them as parser failures.

- Document how category aliases are normalized so repeated runs use consistent query labels.

- Document how malformed source records are counted and reported without exposing raw private contact details.

- Document how request identifiers are recorded to correlate retries without storing full source payloads.

- Document schema validation across paginated responses before records are merged into a completed export.

- Document atomic export publication so validated output replaces prior files only after a run completes successfully.

- Document the row count and checksum recorded after each export is published for integrity verification.

- Document how export integrity metadata is regenerated when a completed dataset is intentionally replaced.

- Document the character encoding and line-ending convention used for portable, reproducible exports.
