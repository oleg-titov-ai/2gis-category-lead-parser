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
- [ ] Open the exported CSV in a spreadsheet app and verify UTF-8 text renders correctly.
- [ ] Confirm exported CSV headers match the documented schema before CRM import.

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