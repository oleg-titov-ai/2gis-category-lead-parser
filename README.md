# 2GIS Category Lead Parser

Portfolio-ready MVP for collecting B2B company leads by city and category, saving them to PostgreSQL, preparing enrichment links, manually verifying contacts, and exporting CSV reports.

> Designed for careful, limited lead research. The public repository intentionally avoids aggressive scraping, captcha bypassing, private data collection, cookies, proxy rotation, and scraping search engine result pages.

---

## Business Problem

Small B2B teams often need a quick way to collect a focused list of companies from a specific city and business category, then prepare that list for manual or API-based enrichment.

Typical manual workflow:

```text
search category manually
copy companies into a spreadsheet
check duplicates
open search links
verify contacts
prepare outreach list
```

This project turns that workflow into a structured mini-pipeline.

---

## Solution

**2GIS Category Lead Parser** collects up to **30 companies per run** from the 2GIS API, stores them in PostgreSQL, creates enrichment source links, supports manual contact verification, and exports CSV files.

```text
2GIS API
  ↓
normalized company records
  ↓
PostgreSQL
  ↓
enrichment queue
  ↓
verified contacts
  ↓
CSV / CRM-ready workflow
```

---

## 🇷🇺 Краткое описание

**2GIS Category Lead Parser** — это портфолио-MVP для B2B lead research.

Пользователь выбирает город и категорию, система собирает до **30 компаний за запуск**, сохраняет данные в PostgreSQL, создаёт очередь обогащения через открытые источники, позволяет вручную подтверждать контакты и выгружает CSV.

---

## Core Flow

```text
Select city + category
        ↓
Collect companies from 2GIS API
        ↓
Normalize and deduplicate
        ↓
Save to PostgreSQL
        ↓
Prepare enrichment sources
        ↓
Manual contact verification
        ↓
Export CSV + terminal report
```

---

## MVP Features

- City + category selection
- Live 2GIS API mode
- Safe demo mode
- Limit of 30 companies per run
- Configurable request delay, default 1 second
- PostgreSQL storage
- Parser job history
- Duplicate detection
- Enrichment source queue
- Manual verified contacts
- CSV export
- Terminal report

---

## Tech Stack

- Python
- PostgreSQL
- psycopg
- requests
- BeautifulSoup for company websites only
- CSV export
- 2GIS API

---

## Repository Structure

```text
2gis-category-lead-parser/
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── docs/
│   ├── architecture.md
│   ├── database-schema.md
│   ├── demo-scenario.md
│   ├── enrichment-strategy.md
│   ├── legal-notes.md
│   ├── roadmap.md
│   ├── setup-checklist.md
│   ├── security.md
│   └── screenshots/
├── sql/
│   ├── 001_schema.sql
│   ├── 002_demo_data.sql
│   └── 003_queries.md
├── src/
│   ├── main.py
│   ├── config.py
│   ├── db.py
│   ├── categories.py
│   ├── parser_2gis.py
│   ├── enrich.py
│   ├── report.py
│   └── exporter.py
├── exports/
├── screenshots/
└── tests/
```

---

## Documentation

- [Architecture](docs/architecture.md)
- [Database Schema](docs/database-schema.md)
- [Demo Scenario](docs/demo-scenario.md)
- [Enrichment Strategy](docs/enrichment-strategy.md)
- [Roadmap](docs/roadmap.md)
- [Setup Checklist](docs/setup-checklist.md)
- [Security](docs/security.md)
- [Legal Notes](docs/legal-notes.md)

---

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Put your real 2GIS API key into `.env` locally only:

```text
DGIS_API_KEY=YOUR_LOCAL_2GIS_API_KEY
```

Never commit `.env`.

---

## PostgreSQL Setup

Create local database:

```bash
createdb lead_parser_demo_db
psql -d lead_parser_demo_db < sql/001_schema.sql
```

---

## Demo Run

```bash
python src/main.py --city "Москва" --category "Металлообработка" --limit 3 --demo
```

---

## Live 2GIS Run

Collect 30 real companies with a configured 1 second delay between API calls:

```bash
python src/main.py \
  --city "Москва" \
  --category "Металлообработка" \
  --limit 30 \
  --save-db
```

Example output:

```text
Parsing finished
City: Москва
Category: Металлообработка
Requested limit: 30

Found: 30
New: 30
Duplicates: 0
With phone: 0
With website: 0
With email: 0
Enriched: 0
CSV exported: exports/leads_demo.csv

Database save:
Job ID: 1
DB new: 30
DB duplicates: 0
DB enrichment sources: 120
```

Phone and website fields may be empty when the API key does not have access to 2GIS contact fields. In that case the project prepares enrichment sources and supports manual contact verification.

---

## Show Enrichment Queue

```bash
python src/main.py --show-enrichment-queue --limit 5
```

This prints search links for manual/API-based enrichment:

```text
company_id: 33
company_name: Example Company
google: https://www.google.com/search?q=...
yandex: https://yandex.ru/search/?text=...
2gis: https://2gis.ru/search/.../firm/...
```

---

## Add Manually Verified Contact

```bash
python src/main.py \
  --add-contact \
  --company-id 33 \
  --type phone \
  --value "+7XXXXXXXXXX" \
  --source-url "https://source-url.example"
```

Supported contact types:

```text
phone
website
email
```

---

## Screenshots

Recommended screenshots for portfolio presentation:

```text
1. Live parser terminal run
2. Enrichment queue terminal output
3. PostgreSQL tables in a database client
4. GitHub README page
5. CSV export folder
```

Place screenshots in:

```text
docs/screenshots/
```

---

## Useful SQL Checks

```bash
psql -d lead_parser_demo_db \
  -c "SELECT 'companies' AS table_name, COUNT(*) FROM companies
      UNION ALL
      SELECT 'parser_jobs', COUNT(*) FROM parser_jobs
      UNION ALL
      SELECT 'enrichment_sources', COUNT(*) FROM enrichment_sources
      UNION ALL
      SELECT 'company_contacts', COUNT(*) FROM company_contacts
      UNION ALL
      SELECT 'job_companies', COUNT(*) FROM job_companies;"
```

```bash
psql -d lead_parser_demo_db \
  -c "SELECT c.id, c.name, cc.contact_type, cc.value, cc.source_url, cc.is_verified
      FROM company_contacts cc
      JOIN companies c ON c.id = cc.company_id
      ORDER BY cc.id DESC;"
```

---

## Security

Never commit:

- real API keys;
- `.env` files;
- real leads export;
- private user data;
- production webhook URLs;
- database dumps;
- cookies or session headers.

Use `.env.example` with placeholders only.

---

## Notes

This project intentionally avoids scraping search engine result pages. For production auto-enrichment, connect a permitted search API or a paid 2GIS API plan with contact field permissions.
