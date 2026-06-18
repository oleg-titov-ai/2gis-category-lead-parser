# 2GIS Category Lead Parser

Portfolio-ready MVP for collecting a small batch of B2B company leads by city and category, saving them to PostgreSQL, preparing open-source enrichment links, manually verifying contacts, and exporting CSV reports.

> This project is designed for careful, limited, lawful lead research. Do not use it for aggressive scraping, bypassing anti-bot systems, collecting private personal data, or scraping search engine result pages.

---

## 🇬🇧 Short Description

**2GIS Category Lead Parser** helps select a business category and city, collect up to **30 companies per run** through the 2GIS API, store them in PostgreSQL, prepare enrichment sources, manually verify contacts, and produce a summary report.

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
│   ├── legal-notes.md
│   ├── setup-checklist.md
│   ├── security.md
│   └── screenshots/
│       └── .gitkeep
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
│   └── .gitkeep
├── screenshots/
│   └── .gitkeep
└── tests/
    └── .gitkeep
```

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
