# Setup Checklist

## Local Setup

- [ ] Clone repository.
- [ ] Create local `.env` from `.env.example`.
- [ ] Fill local database credentials.
- [ ] Install Python dependencies.
- [ ] Verify setup in a clean virtual environment.
- [ ] Run PostgreSQL schema.
- [ ] Run demo mode.
- [ ] Review CSV export.
- [ ] Confirm the export directory is writable before starting a live collection run.
- [ ] Open the exported CSV in a spreadsheet app and verify UTF-8 text renders correctly.
- [ ] Confirm exported CSV headers match the documented schema before CRM import.
- [ ] Confirm exported CSV columns remain in the documented order before sharing or importing.
- [ ] Repeat the same demo command and confirm the export structure remains consistent.
- [ ] Confirm exported filenames do not expose local usernames or customer names.
- [ ] Confirm the exported row count matches the terminal summary before sharing the file.
- [ ] Verify the CSV delimiter is detected correctly by the target spreadsheet or CRM importer.
- [ ] Verify commas, quotes, and line breaks inside company fields remain intact after CSV export and re-import.
- [ ] Confirm missing optional values export as empty fields rather than literal `None` or `null` strings.
- [ ] Confirm CSV files end with a newline for consistent command-line processing.
- [ ] Reopen a demo export using an explicit UTF-8 import setting and confirm no replacement characters appear.
- [ ] Verify duplicate company IDs do not appear in a single CSV export.
- [ ] Verify exported files use consistent LF line endings before automated import.
- [ ] Confirm an unexpectedly large CSV export is reviewed before sharing or importing.
- [ ] Confirm CSV headers contain no leading or trailing whitespace before import.
- [ ] Confirm the CSV encoding is detected as UTF-8 before handing the file to an automated importer.
- [ ] Review text fields beginning with `=`, `+`, `-`, or `@` before opening exports in spreadsheet software.
- [ ] Verify every exported row has the same number of fields as the header before import.
- [ ] Confirm leading and trailing whitespace in exported text fields is intentional before CRM import.
- [ ] Verify exported URLs use an expected `http` or `https` scheme before sharing the file.
- [ ] Confirm the CSV header contains no duplicate column names before import.
- [ ] Check exported text fields for unexpected control characters before CRM import.
- [ ] Reject zero-byte CSV exports before sharing or importing them.
- [ ] Confirm a new export cannot silently overwrite an unrelated existing CSV file.
- [ ] Record or review the exported file size so truncated or unexpectedly large outputs are caught early.
- [ ] Record a checksum for any CSV handed off for import so transfer corruption can be detected.
- [ ] Record the collection date with each shared export so recipients can assess data freshness.
- [ ] Spot-check the first and last exported records before handing the CSV to another system.
- [ ] Record the CSV schema version with shared exports when downstream imports depend on a fixed column layout.
- [ ] Confirm shared export filenames include a neutral project label and collection date, not customer-identifying text.
- [ ] Confirm CSV header capitalization matches the documented schema before case-sensitive imports.
- [ ] Confirm blank trailing rows are removed before importing a CSV into another system.
- [ ] Confirm the collection timestamp is present and plausible before treating an export as current.
- [ ] Confirm the export collection date is included in any handoff note so stale files are not mistaken for current data.
- [ ] Confirm each shared export identifies the public or demo source used for collection without exposing credentials.
- [ ] Confirm the export age is reviewed before using it for outreach or CRM import.
- [ ] Confirm the source label in the handoff note matches the source recorded in the export metadata.
- [ ] Confirm the export timestamp is not in the future relative to the handoff date.
- [ ] Compare the parsed CSV row count with the expected data-record count after reopening the file.
- [ ] Verify exports contain no completely empty data rows between valid records.
- [ ] Confirm the export timestamp is no older than the freshness window expected by the downstream workflow.
- [ ] Confirm a demo export can be regenerated from documented inputs without manual data edits.
- [ ] Confirm a regenerated demo export preserves the same header and row ordering when the input dataset is unchanged.
- [ ] Record the parser version or source commit alongside a shared demo export so its provenance can be reproduced later.
- [ ] Confirm the documented demo command still reproduces the published sample export after dependency updates.
- [ ] Confirm any shared export handoff note states the expected freshness window so recipients know when to regenerate it.
- [ ] Verify the checksum recorded in the handoff note matches the final CSV after any rename or transfer.
- [ ] Confirm schema version, parser commit, collection date, and checksum refer to the same final CSV artifact before handoff.

## Database Setup

```bash
psql "$DATABASE_URL" -f sql/001_schema.sql
psql "$DATABASE_URL" -f sql/002_demo_data.sql
```

- [ ] Confirm a test backup can be restored before using non-demo data.

## Demo Run

```bash
python src/main.py --city "Москва" --category "Металлообработка" --limit 10 --demo
```

## Before Public Release

- [ ] Remove real exports.
- [ ] Confirm generated demo exports contain no local file paths or operator names.
- [ ] Remove `.env`.
- [ ] Check screenshots.
- [ ] Run secret search.
- [ ] Keep only demo data.