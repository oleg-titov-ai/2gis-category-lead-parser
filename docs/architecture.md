# Architecture

```text
CLI input: city + category + limit
        ↓
Create parser job
        ↓
2GIS collector / demo collector
        ↓
Normalize company data
        ↓
Deduplicate by source + source_company_id or name + city + address
        ↓
Save companies and contacts to PostgreSQL
        ↓
Open-source enrichment
        ↓
CSV export
        ↓
Final terminal report
```

---

## Components

### CLI

Accepts:

- city;
- category;
- limit;
- demo mode / live mode.

### Category Selector

Stores allowed categories in `src/categories.py`.

### 2GIS Collector

For the public repository this is a safe demo collector skeleton.

For production usage, connect an allowed data source or official API locally.

### Database

PostgreSQL stores:

- parser jobs;
- companies;
- contacts;
- enrichment sources.

### Enrichment

Open-source enrichment should only use public company websites and public pages.

Do not collect private personal data.

### Report

The report shows:

- requested limit;
- found companies;
- new companies;
- duplicates;
- companies with phone;
- companies with website;
- companies with email;
- enriched companies;
- CSV path.
