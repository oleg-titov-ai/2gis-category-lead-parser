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

## Export maintenance checklist

The checks below are pending verification guidance, separate from the portfolio capabilities listed above. Record synthetic fixture inputs, observed results, and the generating commit for completed checks; do not present untested export behavior as guaranteed.

- Record the source date, demo command parameters, and generating source commit beside each portfolio CSV so examples remain traceable and reproducible; use synthetic parameters without credentials or private query values.

- Verify portfolio CSV files open consistently as UTF-8 and retain deterministic headers without machine-specific metadata.

- Verify source URL normalization is deterministic and preserves distinctions required for contact provenance.

- Verify CSV quoting preserves synthetic values containing commas, quotes, or line breaks during export and re-import; include a field containing all three, compare parsed values rather than raw line counts, and verify an embedded line break does not become an extra record.

- Document the fields removed from demo exports so portfolio samples remain free of contact data and unstable identifiers.

- Document the deterministic sort order used for demo exports so regenerated portfolio samples produce reviewable diffs.

- Document bounded retry and backoff behavior for source requests without exposing proxy or credential details.

- Document the pagination stop condition and a bounded page limit so demo runs cannot continue indefinitely.

- Document cache lifetime, cache-key inputs, and invalidation triggers using synthetic fresh, expired, and missing entries; record the fixture snapshot version separately from cache age so reproducible demos do not silently mix old cached records with refreshed pages.

- Document category-query normalization for whitespace and letter case so equivalent demo inputs remain reproducible; use synthetic leading, trailing, repeated-space, mixed-case, and non-Latin examples to define canonical query labels, cache keys, and audit values while preserving the original display input separately.

- Record an output-schema version beside published demo exports so downstream examples remain interpretable.

- Document bounded concurrency and rate-limit handling for reproducible, source-friendly demo runs.

- Validate required export columns before publishing a demo dataset so downstream examples remain reproducible.

- Document a successful zero-result export with synthetic empty input: preserve required CSV headers or the documented empty JSON structure, record zero rows and completed status, and distinguish it from source failure or interrupted pagination without inserting placeholder organizations.

- Document the audit fields recorded with each export, including query parameters, generation time, and schema version.

- Document how duplicate organizations are identified when source records contain formatting differences in names or addresses.

- Document how interrupted exports are marked so partial files cannot be mistaken for completed datasets.

- Document how source response timestamps are preserved to support freshness checks in exported datasets; use synthetic source-provided, receipt-only, missing, and invalid timestamps to define normalized UTC fields, provenance, age calculation, and an unknown-freshness marker without substituting export time for source time.

- Document how parser warnings are summarized separately from fatal errors in an export run report; use synthetic optional-field, malformed-record, and page-level failures to define category counts, exit status, completion marker, and redacted examples without including raw contact details or source payloads.

- Document how exports identify records with missing optional fields without treating them as parser failures; use synthetic absent, empty, and malformed optional values to define exported null representation, warning counts, and schema-valid completion while keeping required-field failures separate.

- Document how category aliases are normalized so repeated runs use consistent query labels.

- Document how malformed source records are counted and reported without exposing raw private contact details.

- Document how request identifiers are recorded to correlate retries without storing full source payloads; use synthetic initial, retried, and paginated requests to distinguish run, page, and attempt identifiers, specify retention and redaction, and verify logs correlate failures without URL query values or contact data.

- Document schema validation across pages using a synthetic second page with a missing required field or changed field type; define rejection or quarantine rules and mark the export incomplete when required validation fails, preserving the previous verified output instead of silently dropping invalid rows.

- Document atomic export publication so validated output replaces prior files only after a run completes successfully; use synthetic success, validation-failure, and interruption cases to specify temporary-output naming and promotion, verifying failed runs leave the previous verified export and its integrity metadata unchanged.

- Document the row count and checksum recorded after each export is published for integrity verification; use a synthetic completed export to define the checksum algorithm, byte scope, metadata format, and verification command, with mismatched or missing metadata marking the artifact unverified rather than silently regenerating evidence.

- Document how export integrity metadata is regenerated when a completed dataset is intentionally replaced.

- Document the character encoding and line-ending convention used for portable, reproducible exports; state the encoding, byte-order-mark policy, and newline sequence for each format, then round-trip synthetic non-ASCII text and embedded line breaks to verify preserved values without using real listings.

- Document locale-independent formatting for numbers, dates, and delimiters in reproducible exports; compare synthetic decimal values and timestamps under two locale settings, state the numeric precision and date format, and verify CSV delimiters and parsed values remain unchanged without real listing data.

- Document locale-independent text collation so export ordering remains stable across operating systems; name the comparison algorithm and version where applicable, then use synthetic accented and mixed-script names to verify identical order across supported environments, marking untested combinations explicitly.

- Document integrity verification for compressed exports, including checks before publication and after extraction; use synthetic valid and corrupted archives to compare file counts and content checksums, refusing publication on mismatch while preserving the previous verified artifact.

- Document deterministic handling of null, empty, and missing values so regenerated exports produce stable diffs; use synthetic null, empty-string, absent-key, zero, and false cases to define CSV and JSON representations without collapsing valid zero or false values into missing data.

- Document collision-resistant export naming when multiple reproducible runs complete within the same time window; use two synthetic runs with the same timestamp to specify unique output paths and no-overwrite behavior, keeping run identity in filenames separate from deterministic export contents.

- Document deterministic field ordering for CSV and JSON exports when the public export schema is extended; use synthetic records with shuffled input keys to define CSV column order and serialized JSON key order, checking existing field positions and schema-version handling without implying JSON consumers depend on key order.

- Document checkpoint-safe retry behavior when the map provider returns rate-limit responses during a demo export; use synthetic throttled responses to specify bounded backoff, unchanged page checkpoints until success, and explicit incomplete status when retries are exhausted without duplicating exported rows.

- Document checkpoint recovery when a pagination cursor expires before a rate-limited demo collection finishes; use a synthetic expired-cursor response to define restart or abort behavior, retain deduplication state, and mark incomplete output explicitly without repeatedly retrying the invalid cursor.

- Document source-attribution and license metadata included with each portfolio-safe demonstration export; define provenance and permission-reference fields using a clearly labelled synthetic example, marking unknown terms as unverified rather than implying a provider endorsement or redistribution permission.

- Document coordinate precision in demonstration exports to avoid implying accuracy beyond the source data; use synthetic positive, negative, and missing coordinate cases to define rounding and null representation, retaining no more decimal precision than the source supplies and never substituting zero for missing values.

- Document deterministic duplicate handling when the same listing appears on multiple paginated result pages; replay synthetic pages containing one repeated source identifier in reversed order to define field precedence and verify one exported row with consistent duplicate counts.

- Document Unicode normalization for business names before deterministic duplicate detection and export sorting; use synthetic composed and decomposed equivalents to specify the comparison form while preserving original display text, and verify equal normalized names alone never merge distinct source identifiers.

- Document UTC ISO-8601 export timestamps so artifacts remain comparable across operator timezones and locales; define the timestamp's meaning and precision, then serialize one synthetic instant from two timezone settings to verify identical UTC output with an explicit Z suffix.

- Document stable handling of listings whose category label changes between paginated source responses; use a synthetic repeated source identifier with two category labels to define label precedence and provenance while verifying the listing remains a single export row.

- Document how unavailable contact fields are distinguished from intentionally redacted values in demonstration exports; use synthetic present, unavailable, and redacted cases to specify value and status representation so a redacted field cannot be mistaken for a confirmed absence.

- Document stable export ordering when the source changes result ranking between otherwise identical requests; use two synthetic inputs with swapped source ranks to define deterministic sort keys and verify byte-equivalent row order without sourced business records.

- Document CSV encoding and delimiter guarantees so demonstration exports open consistently across locales; define encoding, delimiter, header, and BOM policy, then round-trip a synthetic non-Latin row containing a delimiter and line break without using sourced business data.

- Document source provenance fields for each demonstration export without exposing request credentials or private metadata; define provider, retrieval timestamp, category, page reference, and schema version fields, and show them with a synthetic row that omits tokens and sensitive query parameters.

- Document deterministic sorting of non-Latin business names without relying on the operator's system locale; define normalization, case handling, and a stable tie-break key, then compare synthetic Cyrillic and Latin fixtures under two locale settings while preserving original display names.

- Document an explicit incomplete-export marker when pagination stops before all expected source pages are processed; use a synthetic interrupted page sequence to specify the completion flag and processed-page count, distinguishing partial results from a successful zero-row export.

- Document canonical website URL normalization before duplicate detection and deterministic export; use synthetic URLs to specify treatment of host casing, trailing slashes, and query parameters, including distinct paths that must not be merged.

- Document deterministic address-component normalization while preserving the source-formatted address for display; use synthetic examples with whitespace, missing components, and distinct building numbers to specify normalized output without merging different premises.

- Document export row-count summaries so incomplete or unexpectedly filtered demonstration results are visible; reconcile synthetic input, duplicate, filtered, and exported counts using mutually exclusive categories, with a separate completion flag for unfinished pagination.

- Document consistent treatment of temporarily closed and permanently closed listings in demonstration exports; use synthetic open, temporarily closed, permanently closed, and unknown-status records to specify expected inclusion and exported status values.

- Document the deduplication preference when one business appears in multiple categories with conflicting metadata; add a synthetic two-category example with the same source identifier and specify the expected retained fields, category provenance, and single exported row.
