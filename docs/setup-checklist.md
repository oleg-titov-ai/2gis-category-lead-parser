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