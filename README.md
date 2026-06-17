# 2GIS Category Lead Parser

Private MVP project for collecting a small number of B2B leads by city and category, saving them to PostgreSQL, enriching them with open sources, and generating a parsing report.

> This project is designed for careful, limited, lawful lead research. Do not use it for aggressive scraping, bypassing anti-bot systems, or collecting private personal data.

---

## 🇬🇧 Short Description

**2GIS Category Lead Parser** helps select a business category and city, collect a limited batch of company contacts, store them in PostgreSQL, enrich the records using open sources, and produce a summary report.

The MVP target is **10 companies per run**.

---

## 🇷🇺 Краткое описание

**2GIS Category Lead Parser** — это MVP-парсер лидов по категории и городу.

Пользователь выбирает город и категорию, система собирает до 10 компаний, сохраняет данные в PostgreSQL, обогащает открытыми источниками и выводит отчёт по результатам.

---

## Core Flow

```text
Select city + category
        ↓
Create parser job
        ↓
Collect company data
        ↓
Normalize and deduplicate
        ↓
Save to PostgreSQL
        ↓
Open-source enrichment
        ↓
Export CSV
        ↓
Print final report
```

---

## MVP Features

- Category selector
- City selector
- Limit of 10 companies per run
- PostgreSQL storage
- Duplicate detection
- Open-source enrichment skeleton
- CSV export
- Terminal report
- Safe demo mode

---

## Tech Stack

- Python
- PostgreSQL
- psycopg
- requests
- BeautifulSoup for company websites only
- CSV export

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

## Example Run

```bash
python src/main.py --city "Москва" --category "Металлообработка" --limit 10
```

Example output:

```text
Parsing finished
City: Москва
Category: Металлообработка
Requested limit: 10
Found: 10
New: 8
Duplicates: 2
With phone: 9
With website: 6
With email: 3
Enriched: 5
CSV exported: exports/leads_demo.csv
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
