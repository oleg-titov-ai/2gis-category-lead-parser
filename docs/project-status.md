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

- Document canonical formatting of public phone fields while preserving the source-formatted display value; use synthetic country-code, extension, ambiguous-region, and invalid cases to define normalized output and validation status, and never merge listings solely because normalized phone values match.

- Document canonicalization of public email fields while preserving the source-formatted display value; use synthetic casing, surrounding whitespace, internationalized-domain, invalid, and missing cases to define normalized output and validation status, and never merge listings solely because normalized addresses match.

- Document website redirect handling during URL validation without silently changing source provenance; use synthetic same-host, cross-host, loop, and excessive-hop redirects to define the retained source URL, resolved URL status, and validation outcome without contacting real businesses.

- Document source-schema drift handling when pagination responses add, remove, or change the type of a field; use synthetic compatible, unknown-field, missing-required-field, and wrong-type records to define tolerant parsing versus explicit incomplete status without silently coercing business data.

- Document locale-independent parsing and serialization of numeric fields such as coordinates and ratings; use synthetic dot-decimal, comma-decimal, grouped, missing, and invalid values to define accepted input and deterministic output without relying on the operator's locale.

- Document preservation and optional normalization of public opening-hours fields; use synthetic closed, all-day, split-interval, overnight, localized-text, and unknown-timezone cases to retain the source representation, mark parsing confidence, and avoid inventing a timezone or open-now status.

- Document how a changing source total during pagination affects completion status; use synthetic growing, shrinking, and stable page sets to define a snapshot boundary or explicit incomplete marker, retain deduplication, and avoid claiming full coverage from a moving dataset.

- Document latitude/longitude order and range validation for public location fields; use synthetic valid, swapped, out-of-range, missing, and zero-coordinate records to preserve source values, mark invalid geometry explicitly, and avoid silently relocating an organization.

- Document validation of truncated or partially decoded source responses before pagination state advances; use synthetic incomplete JSON, mismatched length, interrupted compression, and valid payloads to retry within bounds, retain the prior checkpoint, and mark output incomplete without duplicating rows.

- Document normalization of HTML entities and Unicode whitespace in public names and addresses; use synthetic non-breaking, narrow, zero-width, repeated, and ordinary spaces to keep display text readable, preserve the original source field for audit, and avoid unstable duplicate keys.

- Document handling of control characters and null bytes in public text fields before storage and export; use synthetic tabs, line breaks, C0 controls, nulls, and ordinary Unicode to preserve permitted formatting, reject unsafe bytes deterministically, and keep CSV row boundaries stable.

- Document cache validation when the source returns `304 Not Modified`; use synthetic present, expired, corrupt, and missing cache entries to reuse only a verified body, perform a bounded unconditional refetch when needed, and avoid advancing pagination from an absent payload.

- Document rejection of successful HTTP responses whose body is HTML, a consent page, or a challenge instead of the expected JSON schema; use synthetic content types and body signatures to avoid caching or parsing the page as business data, retry within bounds, and mark the export incomplete.

- Document handling of unexpected `206 Partial Content` responses for endpoints expected to return complete JSON pages; use synthetic valid full, correctly ranged, mismatched-range, and missing-range bodies to avoid caching partial business data, retry safely, and retain the prior pagination checkpoint.

- Document the scope of source identifiers when the same identifier can appear in different cities or regions; use synthetic same-scope duplicates and cross-scope collisions to define the composite identity, preserve location provenance, and prevent unrelated public listings from being merged into one export row.

- Document handling of source rate limits and HTTP `429` responses during pagination; use synthetic valid, missing, excessive, and malformed retry-delay values to bound backoff, preserve the last completed page checkpoint, avoid duplicate rows, and mark the export incomplete when the retry budget is exhausted.

- Document transport-failure handling for DNS, TLS, connection-reset, and timeout errors during source pagination; use synthetic failures to apply bounded retries, avoid caching an error as a valid empty page, retain the last completed checkpoint, and mark the demonstration export incomplete without duplicating rows.

- Document maximum response-body limits before decoding source pages; use synthetic ordinary, boundary, oversized-declared, oversized-streamed, and compressed-expansion payloads to abort safely, avoid caching partial public data, retain the last completed pagination checkpoint, and mark the export incomplete.

- Document response-decoding rules when source `Content-Type`, charset, and compression headers disagree with payload bytes; use synthetic valid UTF-8, mislabeled, invalid-sequence, truncated-compression, and unsupported-encoding fixtures to fail explicitly, avoid caching corrupted public data, and retain the pagination checkpoint.

- Document source-endpoint redirect handling during pagination; use synthetic same-host, allowlisted-host, cross-host, loop, downgrade, and excessive-hop redirects to preserve request identity and checkpoints, refuse credential forwarding outside the approved origin, and mark exports incomplete rather than accepting an unexpected body.

- Document JSON parser limits for nesting depth, object-member count, array length, and total scalar count; use synthetic ordinary, boundary, deeply nested, wide, and many-small-value payloads to reject pathological responses before persistence, preserve the last page checkpoint, and mark the export incomplete.

- Document pagination recovery when a source cursor or continuation token expires; use synthetic valid, expired, replayed, malformed, and replaced-token responses to restart only from a documented safe boundary, deduplicate by scoped public identifier, retain the last completed checkpoint, and mark the export incomplete if continuity cannot be proven.

- Document handling of unexpected HTTP `206 Partial Content` responses from source pages; use synthetic valid-full, unsolicited-partial, malformed-range, truncated-range, and repeated-range fixtures to reject incomplete JSON, avoid caching partial public data, retain the last completed checkpoint, and mark the export incomplete.

- Document response-length validation when `Content-Length` disagrees with bytes received; use synthetic exact, shorter, longer, missing, duplicate-header, and compressed-response fixtures to reject truncated or ambiguous JSON, avoid caching partial public data, retain the last completed checkpoint, and mark the export incomplete.

- Document pagination consistency when public source records are inserted, removed, or reordered during a run; use synthetic stable, shifted, duplicated, missing, and changed-sort snapshots to deduplicate by scoped identifier, detect continuity gaps, retain the last proven checkpoint, and mark the export incomplete rather than mixing snapshots silently.

- Document numeric parsing rules for non-finite values, exponential notation, and integers beyond the safe exact range; use synthetic ordinary, boundary, `NaN`, infinity-like, oversized-ID, and precision-loss fixtures to reject ambiguous fields or preserve identifiers as strings, avoid corrupted deduplication, and mark the export incomplete.

- Document spreadsheet-formula injection protection for CSV exports; use synthetic values beginning with `=`, `+`, `-`, `@`, tabs, line breaks, and ordinary text to preserve the original public value in a safe representation, keep row boundaries stable, and verify exports without opening them in a live spreadsheet application.

- Document the CSV byte-level output contract for UTF-8 BOM presence, line endings, final newline, and quoting; use synthetic Unicode, multiline, empty, and boundary records to produce deterministic cross-platform bytes, preserve field content, and verify fixtures without introducing locale-dependent encoding.

- Document validation of public latitude and longitude fields before export; use synthetic valid, boundary, swapped, out-of-range, excessive-precision, null, and non-numeric coordinates to preserve the documented axis order, reject ambiguous locations, avoid false deduplication, and mark affected rows or exports incomplete.

- Document parsing policy for duplicate keys in public JSON objects; use synthetic identical, conflicting, case-variant, nested, boundary-size, and escaped-key fixtures to reject ambiguous records before normalization, avoid parser-dependent last-key-wins behavior, retain the last proven checkpoint, and mark the export incomplete.

- Document handling of bidirectional Unicode controls in public names, addresses, and CSV fields; use synthetic LTR, RTL, mixed-script, isolate, override, unbalanced, and ordinary values to prevent misleading rendered order, preserve auditable source text safely, keep row boundaries stable, and mark ambiguous records incomplete.

- Document source throttling when public endpoints return `429` or rate-limit metadata; use synthetic valid, missing, malformed, excessive, and conflicting `Retry-After` fixtures to apply bounded authoritative delay with jitter, avoid parallel retry storms, retain the last proven checkpoint, and mark the export incomplete if the retry budget expires.

- Document rejection of obsolete folded, oversized, excessive, or ambiguously duplicated HTTP response headers; use synthetic ordinary, `obs-fold`, boundary-size, repeated, conflicting, and mixed-case fixtures to parse deterministically, avoid caching ambiguous public payloads, retain the last proven checkpoint, and mark the export incomplete.

- Document rejection of ambiguous HTTP message framing when `Transfer-Encoding`, `Content-Length`, chunk boundaries, or trailers conflict; use synthetic valid-chunked, dual-length, malformed-chunk, premature-end, unexpected-trailer, and oversized-body fixtures to avoid request-smuggling-style ambiguity, cache no partial public payload, retain the last proven checkpoint, and mark the export incomplete.

- Document handling of unexpected `Set-Cookie` responses from public source endpoints; use synthetic absent, session, persistent, duplicate, oversized, cross-domain, and malformed cookie fixtures to avoid storing or replaying unneeded state, preserve stateless pagination, cache no credential-bearing response metadata, and mark authentication-dependent behavior unsupported.

- Document cache-age decisions when public responses include `Date`, `Age`, `Cache-Control`, or `Expires` headers; use synthetic fresh, stale, conflicting, malformed, missing, and clock-skewed fixtures to derive one bounded freshness result, avoid reusing unverifiable bodies, retain the last proven pagination checkpoint, and mark the export incomplete when validation fails.

- Document handling of HTTP informational responses before the final public payload; use synthetic `100 Continue`, `102 Processing`, `103 Early Hints`, repeated-1xx, missing-final, and conflicting-final fixtures to ignore non-final metadata safely, accept exactly one validated terminal response, cache no hints as content, and retain the last proven checkpoint.

- Document cache-variant validation for HTTP `Vary` and content-negotiated public responses; use synthetic absent, supported-header, wildcard, malformed, compressed, language-dependent, and conflicting variants to key cached bodies by the validated request dimensions, avoid cross-variant reuse, retain the last proven checkpoint, and mark the export incomplete when variant identity is ambiguous.

- Document bounded handling of HTTP redirects from public source endpoints; use synthetic absolute, relative, same-origin, cross-origin, loop, excessive-hop, downgrade, and malformed-location fixtures to resolve targets deterministically, avoid forwarding sensitive headers, cache only the validated terminal response, retain the last proven checkpoint, and mark the export incomplete on ambiguity.

- Document conditional cache validation with `ETag`, weak validators, and `Last-Modified`; use synthetic strong-match, weak-match, changed-body, conflicting-validator, malformed-date, missing-cache, and unexpected-304 fixtures to send only appropriate conditions, reuse only a verified body, retain the last proven checkpoint, and mark the export incomplete when validation is ambiguous.

- Document TLS certificate and hostname validation for public source endpoints; use synthetic valid-chain, expired, not-yet-valid, hostname-mismatch, unknown-authority, intercepted, and clock-skew fixtures to fail closed without custom trust bypasses, cache no response from an unverified peer, retain the last proven checkpoint, and mark the export incomplete.

- Document public-endpoint DNS and resolved-address validation before each connection and redirect; use synthetic public, loopback, private, link-local, IPv4-mapped, resolution-change, and rebinding fixtures to reject non-public destinations, avoid forwarding request metadata across trust boundaries, cache no unverified response, retain the last proven checkpoint, and mark the export incomplete.

- Document rejection of source URLs containing userinfo, embedded credentials, fragments, or ambiguous Unicode hostnames; use synthetic ordinary, username-only, username-password, empty-userinfo, fragment, IDN, confusable, and percent-encoded fixtures to canonicalize only safe public targets, avoid credential propagation, cache no ambiguous response, and retain the last proven checkpoint.

- Document handling of HTTP `Content-Location` metadata on validated public responses; use synthetic absent, same-URL, relative, same-origin, cross-origin, credential-bearing, malformed, and conflicting values to treat it as non-authoritative unless explicitly supported, avoid changing pagination or cache identity silently, retain the last proven checkpoint, and mark ambiguous exports incomplete.

- Document minimization of outbound HTTP `Referer` and `Origin` headers for public source requests; use synthetic absent, same-origin, cross-origin, redirect, proxy, and client-default cases to send only explicitly required non-sensitive metadata, avoid leaking query inputs or internal URLs, preserve deterministic request behavior, and retain the last proven checkpoint on rejection.

- Document deterministic `Accept`, `Accept-Language`, and charset negotiation for public source requests; use synthetic supported, unsupported, wildcard, reordered, locale-specific, conflicting-content-type, and missing-charset fixtures to request one reviewed representation, reject ambiguous decoding, keep cache variants separate, retain the last proven checkpoint, and mark incomplete exports clearly.

- Document safe handling of compressed HTTP responses from public sources; use synthetic identity, gzip, unsupported-encoding, truncated-stream, checksum-error, compression-bomb, and nested-encoding fixtures to allow only reviewed encodings, enforce compressed and expanded size limits, reject ambiguous decoding, retain the last proven checkpoint, and mark incomplete exports clearly.

- Document crash-safe cleanup of temporary HTTP response bodies before parsing or export; use synthetic complete, partial, oversized, interrupted, retry, stale-temp, and concurrent-worker fixtures to stage data in a bounded private location, publish only validated output atomically, remove abandoned artifacts safely, retain the last proven checkpoint, and expose no request data in filenames.

- Document deterministic chunking for exports that exceed a reviewed row or byte limit; use synthetic empty, exact-boundary, multi-chunk, oversized-record, interrupted, resumed, and duplicate-page fixtures to keep headers and ordering stable, publish only complete chunks atomically, preserve deduplication across boundaries, retain the last proven checkpoint, and mark partial export sets clearly.

- Document a non-sensitive export manifest for each completed export set; use synthetic empty, single-file, multi-chunk, resumed, schema-changed, checksum-mismatch, and missing-chunk fixtures to record schema version, file ordering, row counts, byte sizes, and content hashes without source URLs or request data, publish the manifest only after all chunks validate, and mark incomplete sets clearly.

- Document pagination-completeness checks for public source collection; use synthetic empty, single-page, duplicate-page, missing-page, overlapping-page, cursor-loop, reordered, and terminal-page fixtures to preserve deterministic deduplication, detect silent gaps, bound requests, retain the last proven checkpoint, and mark incomplete exports clearly without exposing source query details.

- Document a source-policy review before enabling collection from a public endpoint; use synthetic allowed, disallowed, ambiguous, changed-policy, rate-limited, authentication-required, and unavailable-policy cases to record the reviewed access basis and request limits without bypassing controls, issuing live probes, storing policy text unnecessarily, or exposing source query details.

- Document deterministic address normalization for deduplication without overwriting the public source value; use synthetic abbreviation, punctuation, whitespace, Unicode-normalization, building-unit, ambiguous, and missing-field fixtures to store a separate reviewed comparison key, preserve the original export text, avoid inventing address components, retain stable ordering, and mark uncertain matches explicitly.

- Document deterministic phone-number normalization for deduplication without replacing the public source value; use synthetic international, national, extension, punctuation, leading-zero, invalid, and missing cases to store a separate reviewed comparison key, avoid guessing country codes, preserve the original export text, prevent false merges, retain stable ordering, and mark uncertain matches explicitly.

- Document deterministic website-URL canonicalization for deduplication without replacing the public source value; use synthetic scheme, host-case, default-port, trailing-slash, fragment, tracking-parameter, international-domain, and invalid cases to store a separate reviewed comparison key, avoid following redirects or guessing equivalence, preserve original export text, prevent false merges, and mark uncertain matches explicitly.

- Document versioned category-taxonomy mapping when a public source renames, merges, or splits categories; use synthetic unchanged, renamed, merged, split, retired, conflicting, and unknown-version fixtures to preserve the original source category, store one reviewed canonical mapping separately, avoid silently reclassifying prior exports, keep deduplication stable, and mark unresolved records clearly.

- Document preservation of source-provided geocoding confidence or accuracy metadata in exports; use synthetic high, low, missing, contradictory, stale, out-of-range, and text-only location cases to keep the original value separate from normalized coordinates, avoid inventing precision or acceptance thresholds, preserve stable deduplication keys, and mark uncertain locations explicitly.

- Document preservation of source-provided parent-organization and branch identifiers for multi-location businesses; use synthetic standalone, two-branch, renamed-branch, moved-branch, duplicate-name, missing-parent, and conflicting-parent fixtures to keep each public location distinct, avoid inferring chain membership from names alone, preserve source identifiers separately, and mark unresolved relationships explicitly.

- Document rating-scale and review-count semantics for public listing exports; use synthetic unrated, single-review, low-count, high-count, changed-scale, missing-count, and contradictory records to preserve source values separately, avoid treating ratings from different scales as equivalent, prevent unsupported ranking claims, and mark incomplete evidence explicitly.

- Document typed handling of public messenger and social-contact fields in exports; use synthetic website, email, Telegram, WhatsApp, generic-messenger, malformed, duplicate, and unknown-provider records to preserve the source label and value separately, avoid coercing one provider into another, prevent contact fields from becoming deduplication keys, and mark unsupported types explicitly.

- Document postal-code handling as text with explicit country context in public listing exports; use synthetic leading-zero, alphanumeric, spaced, localized, missing, conflicting-country, and malformed records to preserve the source value, avoid numeric coercion or unsupported reformatting, keep postal codes out of deduplication keys, and mark validation uncertainty explicitly.

- Document administrative-area hierarchy in public address exports; use synthetic country, region, city, district, municipality, missing-level, conflicting-level, and renamed-area records to preserve each source component separately, avoid flattening distinct levels into one label, keep stable source identifiers where available, and mark unresolved hierarchy explicitly without inferring geography from free text.

- Document preservation of source-language codes and original localized labels in public exports; use synthetic single-language, translated, mixed-language, missing-code, unsupported-code, changed-label, and conflicting-locale records to retain original text separately from any reviewed normalized label, avoid guessing language from script alone, keep deduplication stable, and mark uncertain mappings explicitly.

- Document separate handling of public legal, trade, brand, and short organization names when a source provides them; use synthetic identical, distinct, renamed, missing-legal, missing-brand, conflicting, and mixed-language records to preserve each source field, choose a reviewed display label without overwriting originals, avoid name-only deduplication, and mark unresolved conflicts explicitly.

- Document address subpremise fields such as entrance, floor, unit, suite, or office when provided by a public listing source; use synthetic separate, combined, localized, missing, conflicting, renamed, and malformed records to preserve each source component without guessing a canonical address, keep display formatting distinct from deduplication, avoid treating access details as contact data, and mark unresolved structure explicitly.

- Document public accessibility attributes such as wheelchair entrance, accessible restroom, elevator, or step-free access when a listing source provides them; use synthetic explicit-yes, explicit-no, unknown, partial, conflicting, renamed, and stale records to preserve each source claim and timestamp separately, avoid inferring accessibility from category or photos, keep the fields out of deduplication keys, and mark uncertainty clearly.

- Document public payment-option fields such as cash, card, transfer, or contactless payment when a listing source provides them; use synthetic supported, unsupported, conditional, mixed, localized, conflicting, and stale records to preserve each source claim separately, avoid inferring acceptance from category or brand, keep payment options out of deduplication keys, and mark conditions or uncertainty explicitly.

- Document public service-area or delivery-zone fields separately from a branch's physical address; use synthetic same-area, multi-area, radius, polygon-label, city-list, missing, conflicting, and stale records to preserve the source representation without inventing geometry, avoid treating service coverage as a branch location or deduplication key, and mark uncertainty or unsupported shapes explicitly.

- Document public reservation, appointment, or online-booking links separately from general website URLs; use synthetic valid, redirected, localized, duplicate, tracking-parameter, unsupported-scheme, conflicting, and stale records to preserve the source URL and reviewed normalized form, avoid following links during parsing, keep booking URLs out of deduplication keys, and mark validation status explicitly.

- Document public price-range or average-check fields with explicit currency and source context; use synthetic exact-range, open-ended, localized-format, missing-currency, changed-currency, conflicting, promotional, and stale records to preserve raw and reviewed normalized values separately, avoid inferring currency from location alone, keep price fields out of deduplication keys, and mark uncertainty explicitly.

- Document public parking attributes such as on-site, street, paid, free, accessible, or time-limited parking when a listing source provides them; use synthetic explicit, conditional, multiple-option, localized, unknown, conflicting, and stale records to preserve each source claim and condition separately, avoid inferring availability from maps or category, keep parking fields out of deduplication keys, and mark uncertainty explicitly.

- Document public amenity flags such as Wi-Fi, restroom, outdoor seating, pet-friendly access, or takeaway when a listing source provides them; use synthetic explicit-yes, explicit-no, conditional, multiple, localized, unknown, conflicting, and stale records to preserve each source claim independently, avoid inferring amenities from reviews or category, keep flags out of deduplication keys, and mark uncertainty clearly.

- Document sanitization of public business-description text and markup from listing sources; use synthetic plain-text, allowed-line-break, HTML-like, script-like, malformed-entity, oversized, localized, and conflicting records to preserve the original source value separately from a reviewed display-safe form, avoid executing or following embedded content, keep descriptions out of deduplication keys, and mark truncation or rejection explicitly.

- Document public menu, catalog, or price-list URLs separately from a business's general website and booking links; use synthetic valid, localized, PDF, redirected, tracking-parameter, unsupported-scheme, conflicting, and stale records to preserve the source URL and reviewed normalized form, avoid following or downloading linked content during parsing, keep these URLs out of deduplication keys, and mark validation status explicitly.

- Document public brand, franchise, or network affiliation separately from a branch's legal and display names; use synthetic independent, franchisee, shared-brand, renamed-brand, multiple-brand, missing, conflicting, and stale records to preserve each source claim and identifier separately, avoid merging branches solely because they share a brand, keep affiliation out of primary deduplication keys, and mark uncertainty explicitly.

- Document public delivery or online-ordering links separately from general websites, menus, and booking URLs; use synthetic first-party, marketplace, localized, redirected, tracking-parameter, unsupported-scheme, conflicting, and stale records to preserve the source URL and reviewed normalized form, avoid following links or placing orders during parsing, keep ordering links out of deduplication keys, and mark validation status explicitly.

- Document source-provided relocation relationships between a moved listing and its previous or successor branch record; use synthetic unchanged, moved-once, moved-twice, stale-predecessor, duplicate-successor, conflicting-link, missing-target, and reopened-old-location cases to preserve each public source identifier and address separately, avoid merging records from name similarity alone, keep relocation metadata out of primary deduplication keys, and mark unresolved chains explicitly.

- Document public category hierarchy and primary-versus-secondary category fields from listing sources; use synthetic single-category, parent-child, multiple-secondary, moved-category, duplicate-label, missing-parent, conflicting-primary, and stale records to preserve source identifiers and localized labels separately, avoid inferring hierarchy from text alone, keep categories out of primary deduplication keys, and mark unresolved relationships explicitly.

- Document source-provided sponsored, promoted, or advertising status separately from ordinary listing content; use synthetic organic, sponsored, promoted-category, expired-campaign, conflicting-flags, missing-label, duplicate-record, and stale records to preserve the source claim and observation time explicitly, avoid treating prominence as quality or verification, keep promotional state out of deduplication keys, and prevent it from changing ranking silently.

- Document source-provided claimed, verified, or owner-confirmed listing badges separately from factual business fields; use synthetic unclaimed, claimed, verified, expired, conflicting-badges, missing-label, duplicate-record, and stale records to preserve the exact source claim and observation time, avoid treating a badge as proof that every field is current, keep verification state out of deduplication keys, and mark uncertainty explicitly.

- Document public photo, rating, and review-count summary fields as time-bound source observations rather than verified quality measures; use synthetic zero, positive, missing, decreased, reset, conflicting, promoted, and stale records to preserve each raw value with its observation time and reviewed normalized type, avoid fetching individual media or reviews, keep counts out of deduplication and ranking keys, and mark uncertainty explicitly.

- Document public transit references such as nearest station, stop name, route label, or walking-distance text when a listing source provides them; use synthetic explicit, multiple-options, localized, distance-only, missing, conflicting, relocated, and stale records to preserve each source claim separately, avoid geocoding or inferring accessibility from names alone, keep transit fields out of deduplication keys, and mark uncertainty explicitly.

- Document payment-method claims such as cash, bank card, online payment, or invoice only when a listing source states them; use synthetic explicit, multiple-method, localized, ambiguous-icon, missing, conflicting, recently-changed, and stale records to preserve each source claim and observation time separately, avoid inferring acceptance from category or branding, keep payment fields out of deduplication keys, and mark uncertainty explicitly.

- Document appointment or reservation requirements only when a listing source states them; use synthetic required, recommended, walk-in-accepted, channel-specific, localized, missing, conflicting, and recently-changed records to preserve the exact source claim and observation time separately, avoid inferring availability from category or opening hours, keep booking fields out of deduplication keys, and mark uncertainty explicitly.

- Document minimum-order and price-threshold claims only when a listing source states them; use synthetic fixed-amount, category-specific, delivery-only, localized-currency, range, missing, conflicting, and recently-changed records to preserve the exact source text, normalized currency when explicit, and observation time separately, avoid estimating affordability or acceptance, keep commercial thresholds out of deduplication keys, and mark uncertainty explicitly.

- Document delivery or service-area claims only when a listing source states them; use synthetic named-district, radius-text, postal-code-list, map-link-only, localized, missing, conflicting, and recently-changed records to preserve the exact source claim and observation time separately, avoid geocoding or inferring coverage from an address, keep service-area fields out of deduplication keys, and mark uncertainty explicitly.

- Document spoken or supported service languages only when a listing source states them; use synthetic single-language, multiple-language, localized-name, interpreter-available, interface-only, missing, conflicting, and recently-changed records to preserve the exact source claim and observation time separately, avoid inferring staff fluency from reviews or location, keep language fields out of deduplication keys, and mark uncertainty explicitly.

- Document temporary or seasonal closure claims only when a listing source states them; use synthetic renovation, holiday, seasonal, emergency, reopening-date, open-again, missing, and conflicting records to preserve the exact source wording and observation time separately, avoid converting uncertainty into permanent closure, keep closure fields out of identity and deduplication keys, and require a fresh source observation before clearing a prior status.

- Document branch, parent-organization, and chain relationships only when a listing source states them; use synthetic headquarters, branch, franchise, shared-brand-only, relocated-branch, missing-parent, conflicting, and recently-changed records to preserve each source claim and observation time separately, avoid inferring legal ownership from names or logos, keep relationship fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document age restrictions or audience limits only when a listing source states them; use synthetic explicit-minimum, adult-only, guardian-required, event-specific, localized, missing, conflicting, and recently-changed records to preserve the exact source wording and observation time separately, avoid inferring restrictions from category, imagery, or reviews, keep restriction fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document online consultations or remote-service availability only when a listing source states it; use synthetic video, phone, chat, asynchronous, appointment-only, localized, missing, conflicting, and recently-changed records to preserve the exact source claim and observation time separately, avoid inferring remote availability from a website or category alone, keep service-mode fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document price ranges, average checks, or starting-price claims only when a listing source states them; use synthetic exact-range, from-price, average-check, category-specific, localized-currency, missing, conflicting, and recently-changed records to preserve the exact source wording, explicit currency, and observation time separately, avoid estimating affordability or converting currencies silently, keep price fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document stated service duration, preparation time, or expected wait only when a listing source provides it; use synthetic exact-duration, range, queue-dependent, appointment-specific, delivery-only, localized-unit, missing, conflicting, and recently-changed records to preserve the exact source wording and observation time separately, avoid predicting live wait from static text, keep timing fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document entrance, floor, intercom, or landmark instructions only when a listing source states them; use synthetic street-entrance, courtyard, floor-suite, intercom, accessible-entrance, temporary-route, missing, conflicting, and recently-changed records to preserve the exact source wording and observation time separately, avoid inferring access from map geometry or photos, keep navigation fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document temporary relocation and return-to-original-address claims only when a listing source states them; use synthetic moved-temporarily, reopening-date, shared-premises, old-address-still-active, missing-date, conflicting, recently-changed, and permanent-move records to preserve exact source wording and observation time separately, avoid predicting a return date, keep relocation fields out of identity and deduplication keys, retain both addresses with provenance, and mark uncertainty explicitly.

- Document parking availability, fees, validation, or vehicle restrictions only when a listing source states them; use synthetic free, paid, validated, customer-only, height-limited, time-limited, unavailable, conflicting, and recently-changed records to preserve exact source wording and observation time separately, avoid inferring parking from map imagery, keep parking fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document loyalty programs, membership discounts, cashback, or stamp-card claims only when a listing source states them; use synthetic free-membership, paid-tier, app-required, limited-time, branch-specific, discontinued, conflicting, and recently-changed records to preserve exact source wording and observation time separately, avoid calculating savings or inferring eligibility, keep loyalty fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document accepted insurance plans or reimbursement claims only when a listing source states them; use synthetic named-plan, public-program, reimbursement-only, referral-required, branch-specific, expired, conflicting, and recently-changed records to preserve exact source wording and observation time separately, avoid inferring coverage or eligibility, keep insurance fields out of identity and deduplication keys, avoid storing patient information, and mark uncertainty explicitly.

- Document deposits, prepayment, cancellation fees, or refundable-hold requirements only when a listing source states them; use synthetic fixed-deposit, percentage, refundable, nonrefundable, appointment-only, recently-waived, conflicting, and recently-changed records to preserve exact source wording and observation time separately, avoid calculating totals or inferring terms, keep payment-policy fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document hearing-assistance, sign-language, captioning, or other communication-accessibility claims only when a listing source states them; use synthetic hearing-loop, interpreter-by-request, captioned-service, text-contact, appointment-required, unavailable, conflicting, and recently-changed records to preserve exact source wording and observation time separately, avoid inferring accessibility from category or photos, keep these fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document service guarantees, warranties, free-redo, or satisfaction claims only when a listing source states them; use synthetic time-limited, product-only, service-only, conditional, branch-specific, discontinued, conflicting, and recently-changed records to preserve exact source wording and observation time separately, avoid evaluating enforceability or inferring coverage, keep guarantee fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document air conditioning, outdoor seating, private rooms, or similar venue-amenity claims only when a listing source states them; use synthetic available, seasonal, reservation-only, shared-space, temporarily-unavailable, branch-specific, conflicting, and recently-changed records to preserve exact source wording and observation time separately, avoid inferring amenities from photos or reviews, keep amenity fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document smoking, vaping, smoke-free, or designated-area policies only when a listing source states them; use synthetic fully-smoke-free, outdoor-only, designated-room, event-specific, age-restricted, temporarily-changed, conflicting, and recently-updated records to preserve exact source wording and observation time separately, avoid inferring policy from category, photos, or reviews, keep policy fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document pet-friendly, service-animal, restricted-area, or no-pets policies only when a listing source states them; use synthetic pets-allowed, outdoor-only, carrier-required, size-limited, service-animals-only, temporary-restriction, conflicting, and recently-changed records to preserve exact source wording and observation time separately, avoid inferring policy from category, photos, or reviews, keep policy fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document gift-card, voucher, certificate, or stored-value claims only when a listing source states them; use synthetic available, digital-only, physical-only, branch-limited, expiry-stated, temporarily-unavailable, conflicting, and recently-changed records to preserve exact source wording and observation time separately, avoid inferring redemption terms or monetary value, keep offer fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document dress-code, footwear, protective-equipment, or other visitor-attire requirements only when a listing source states them; use synthetic formal, casual, protective-gear, venue-supplied, event-specific, temporarily-relaxed, conflicting, and recently-changed records to preserve exact source wording and observation time separately, avoid inferring requirements from category, photos, or reviews, keep policy fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document reservation, cancellation, no-show, or advance-booking policies only when a listing source states them; use synthetic walk-in, reservation-required, deposit-backed, free-cancellation, deadline-limited, no-show-fee, conflicting, and recently-changed records to preserve exact source wording and observation time separately, avoid inferring enforceability or calculating fees, keep policy fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document high chairs, changing tables, play areas, stroller access, or other child-friendly facility claims only when a listing source states them; use synthetic available, age-limited, reservation-only, temporarily-unavailable, branch-specific, seasonal, conflicting, and recently-changed records to preserve exact source wording and observation time separately, avoid inferring suitability or safety from category, photos, or reviews, keep facility fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document delivery, pickup, curbside, or takeaway availability only when a listing source states it; use synthetic delivery-only, pickup-only, both, area-limited, minimum-order-stated, temporarily-unavailable, branch-specific, conflicting, and recently-changed records to preserve exact source wording and observation time separately, avoid inferring coverage, price, or timing, keep fulfillment fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document waitlist, virtual-queue, walk-in, or callback-queue policies only when a listing source states them; use synthetic no-waitlist, in-person-only, app-required, callback-available, capacity-limited, temporarily-disabled, branch-specific, conflicting, and recently-changed records to preserve exact source wording and observation time separately, avoid predicting wait times or inferring priority, keep queue fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document quiet-hour, low-sensory, reduced-lighting, or similar visitor-accommodation claims only when a listing source states them; use synthetic scheduled, request-only, room-specific, event-specific, temporarily-unavailable, branch-specific, conflicting, and recently-changed records to preserve exact source wording and observation time separately, avoid inferring medical suitability, accessibility, or noise levels from category, photos, or reviews, keep accommodation fields out of identity and deduplication keys, and mark uncertainty explicitly.

- Document electric-vehicle charging, bicycle charging, or other customer charging-station claims only when a listing source states them; use synthetic available, connector-limited, customer-only, paid, temporarily-unavailable, branch-specific, conflicting, and recently-changed records to preserve exact source wording and observation time separately, avoid inferring compatibility, price, power, or availability from category, photos, or reviews, keep charging fields out of identity and deduplication keys, and mark uncertainty explicitly.
