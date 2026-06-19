# Demo Scenario

This scenario shows the project as a portfolio-ready lead research pipeline.

## Goal

Collect a small batch of companies from a selected 2GIS category, save them to PostgreSQL, prepare enrichment links, and export a CSV report.

Example category:

```text
Металлообработка
```

Example city:

```text
Москва
```

## 1. Start the Project

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Fill `.env` locally. Never commit real secrets.

## 2. Prepare PostgreSQL

```bash
createdb lead_parser_demo_db
psql -d lead_parser_demo_db < sql/001_schema.sql
```

## 3. Run Live Parser

```bash
python src/main.py \
  --city "Москва" \
  --category "Металлообработка" \
  --limit 30 \
  --save-db
```

Expected output:

```text
Parsing finished
Found: 30
Database save:
DB new: 30
DB enrichment sources: 120
```

## 4. Show Enrichment Queue

```bash
python src/main.py --show-enrichment-queue --limit 5
```

Expected output:

```text
company_id: 33
company_name: Example Company
google: https://www.google.com/search?q=...
yandex: https://yandex.ru/search/?text=...
2gis: https://2gis.ru/search/.../firm/...
```

## 5. Add Verified Contact

```bash
python src/main.py \
  --add-contact \
  --company-id 33 \
  --type phone \
  --value "+7XXXXXXXXXX" \
  --source-url "https://source-url.example"
```

## 6. Check Database

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

## 7. Screenshots to Capture

Recommended screenshots:

1. terminal live parser run;
2. terminal enrichment queue;
3. PostgreSQL tables in a database client;
4. README page on GitHub;
5. CSV export folder.
