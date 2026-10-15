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

- Document locale-independent formatting for numbers, dates, and delimiters in reproducible exports.

- Document locale-independent text collation so export ordering remains stable across operating systems.

- Document integrity verification for compressed exports, including checks before publication and after extraction.

- Document deterministic handling of null, empty, and missing values so regenerated exports produce stable diffs.

- Document collision-resistant export naming when multiple reproducible runs complete within the same time window.

- Document deterministic field ordering for CSV and JSON exports when the public export schema is extended.

- Document checkpoint-safe retry behavior when the map provider returns rate-limit responses during a demo export.

- Document checkpoint recovery when a pagination cursor expires before a rate-limited demo collection finishes.

- Document source-attribution and license metadata included with each portfolio-safe demonstration export.

- Document coordinate precision in demonstration exports to avoid implying accuracy beyond the source data.

- Document deterministic duplicate handling when the same listing appears on multiple paginated result pages.

- Document Unicode normalization for business names before deterministic duplicate detection and export sorting.

- Document UTC ISO-8601 export timestamps so artifacts remain comparable across operator timezones and locales.

- Document stable handling of listings whose category label changes between paginated source responses.

- Document how unavailable contact fields are distinguished from intentionally redacted values in demonstration exports.

- Document stable export ordering when the source changes result ranking between otherwise identical requests.

- Document CSV encoding and delimiter guarantees so demonstration exports open consistently across locales.

- Document source provenance fields for each demonstration export without exposing request credentials or private metadata.

- Document deterministic sorting of non-Latin business names without relying on the operator's system locale.

- Document an explicit incomplete-export marker when pagination stops before all expected source pages are processed; use a synthetic interrupted page sequence to specify the completion flag and processed-page count, distinguishing partial results from a successful zero-row export.

- Document canonical website URL normalization before duplicate detection and deterministic export; use synthetic URLs to specify treatment of host casing, trailing slashes, and query parameters, including distinct paths that must not be merged.

- Document deterministic address-component normalization while preserving the source-formatted address for display.

- Document export row-count summaries so incomplete or unexpectedly filtered demonstration results are visible; reconcile synthetic input, duplicate, filtered, and exported counts using mutually exclusive categories, with a separate completion flag for unfinished pagination.

- Document consistent treatment of temporarily closed and permanently closed listings in demonstration exports; use synthetic open, temporarily closed, permanently closed, and unknown-status records to specify expected inclusion and exported status values.

- Document the deduplication preference when one business appears in multiple categories with conflicting metadata; add a synthetic two-category example with the same source identifier and specify the expected retained fields, category provenance, and single exported row.
